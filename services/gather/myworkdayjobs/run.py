import os
import re
import logging
import datetime
import itertools

import pandas as pd
import requests
from typing import Union, Tuple
from multiprocessing import Pool, Lock
from services.gather.database import init_db, Company, Job, db_insert_one, db_insert_many
from .utils.helpers import (split_url, get_jobs_count, records_expired, remove_expire_jobs,
                            date_parser, parse_remote_type)
from .schemas.schemas import company_schema
from .config import SHEET_URL, LOG_FOLDER, JSON_SERP_URL

WORKERS = 5
MAX_SERPS_INSERT = 10
lock = Lock()
db = init_db()

if LOG_FOLDER not in os.listdir(os.path.dirname(__file__)):
    os.mkdir(os.path.join(os.path.dirname(__file__), LOG_FOLDER))

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), LOG_FOLDER,
                                          f'{datetime.datetime.today().date()}.txt'),
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s\t:  %(message)s',
                    datefmt='%d.%m.%Y-%H:%M:%S')


def store_company_info(company_name: str, start_url: str) -> None:
    start_serp_number = 0
    domain, serp_category = split_url(start_url)
    serp_json_url = JSON_SERP_URL.format(domain, serp_category, start_serp_number)
    jobs_count = get_jobs_count(serp_json_url)
    if jobs_count:
        company_data = {
            "company_name": company_name,
            "serp_json_url": serp_json_url,
            "domain": domain,
            "serp_category": serp_category,
            "jobs_count": jobs_count
        }
        db_insert_one(db, Company, company_data, lock)
        logging.info(f"Saved company info for {start_url} in Table.Company")


def get_jobs_serps_json(record: dict) -> list:
    jobs_per_page = 50
    jobs_count, domain = record.get('jobs_count'), record.get('domain')
    return [[domain, record.get('company_name'),
             JSON_SERP_URL.format(domain, record.get('serp_category'), j_count)]
            for j_count in range(0, jobs_count, jobs_per_page)]


def parse_jobs_links(domain: str, comp_name: str, serp_link: str) -> list:
    try:
        response = requests.get(serp_link.strip(), timeout=60)
        jobs_list = response.json().get('body').get('children')[0].get('children')[0].get(
            'listItems')

        jobs_link = [{'company_name': comp_name,
                      'url': f"https://{domain}{job.get('title').get('commandLink')}"}
                     for job in jobs_list]

        return parse_job(jobs_link)
    except Exception as e:
        logging.error(f"Can't parse jobs links in {parse_jobs_links.__name__} !\nError = {e}")
        return []


def parse_job_info(job_data: dict, extra_info: dict) -> Union[dict, None]:
    try:
        region, description, jobtype, updated = [""] * 4  # number of fields
        title = re.sub(r"<.*?>", "", job_data.get("body").get("children")[0].get("text"))
        region_desc_container = job_data.get("body").get("children")[1].get("children")[0].get(
            "children")

        for child_elem in region_desc_container:
            if child_elem.get("ecid") == "labeledImage.LOCATION":
                region += child_elem.get("imageLabel") + " "
            if child_elem.get("ecid") == "richTextArea.jobPosting.jobDescription":
                description = child_elem.get("value")
        type_date_container = job_data.get("body").get("children")[1].get("children")[1].get(
            "children")
        for child_elem in type_date_container:
            if child_elem.get("widget") == "labeledImage":
                if child_elem.get("ecid") == "labeledImage.POSTED_DATE":
                    updated = child_elem.get("imageLabel")
            if child_elem.get("widget") == "labeledImage":
                if child_elem.get("ecid") == "labeledImage.JOB_TYPE":
                    jobtype = child_elem.get("imageLabel")

        published_at = date_parser(updated)
        remote_type = parse_remote_type(region)
        return {
            "url": extra_info['url'],
            "title": title,
            "region": region,
            "company": extra_info['company_name'],
            "remote_type": remote_type,
            "job_type": jobtype,
            "posted_at": published_at,
            "description": description
        }
    except AttributeError:
        logging.error(f"Can not get field from json")
    except Exception as e:
        logging.error(f"Can not parse job json \nError = {e}")


def get_job_info(job_dict: dict) -> Union[Tuple[dict, dict], None]:
    try:
        response = requests.get(job_dict['url'].strip(), headers={
            "Accept": "application/json,application/xml"
        }, timeout=60)

        return response.json(), job_dict
    except Exception as e:
        logging.error(f"Can not get job json from request \nError = {e}")


def parse_job(job_info_list: list) -> list:
    exist_urls = set(
        map(
            lambda record: record.url,
            db.query(Job).filter(
                Job.url.in_([job['url'] for job in job_info_list])
            )
        )
    )
    new_jobs = [job for job in job_info_list if job['url'] not in exist_urls]
    dirty_jobs_info = filter(lambda info: info is not None, map(get_job_info, new_jobs))
    jobs = filter(lambda job: job is not None, itertools.starmap(parse_job_info, dirty_jobs_info))

    return [Job(**job) for job in jobs]


if __name__ == '__main__':
    print("START PARSE MyWorkDayJobs")
    last_record_date = db.query(
        Company.expire_at
    ).order_by(Company.expire_at).first()
    if last_record_date is None or records_expired(*last_record_date):

        db.query(Company).delete()
        db.commit()
        remove_expire_jobs(db, Job)

        columns = pd.read_csv(SHEET_URL)
        sheet_info = zip(columns['force_company'], columns['start_url'])
        with Pool(WORKERS) as pool:
            pool.starmap(store_company_info, sheet_info)

    comp_data = company_schema.dump(db.query(Company).all())

    with Pool(WORKERS) as pool:
        total_serps = list(itertools.chain(*pool.map(get_jobs_serps_json, comp_data)))

    for idx in range(0, len(total_serps), MAX_SERPS_INSERT):
        with Pool(WORKERS) as pool:
            total_jobs = list(
                itertools.chain(*pool.starmap(
                    parse_jobs_links, total_serps[idx: idx + MAX_SERPS_INSERT]
                ))
            )
        db_insert_many(db, total_jobs, lock)
        logging.info(f"Stored {len(total_jobs)} jobs!")
