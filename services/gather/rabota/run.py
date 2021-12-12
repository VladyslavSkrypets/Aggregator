import os
import re
import time
import logging
import random
import datetime
import itertools
import dateparser
from typing import Union
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from services.gather.database import db_insert_many, init_db, Job
from .config import LOG_FOLDER, SITE_SERP_URL, LAST_PAGE, BATCH_SIZE, JOB_URL

WORKERS = 5
lock = Lock()
db = init_db()

if LOG_FOLDER not in os.listdir(os.path.dirname(__file__)):
    os.mkdir(os.path.join(os.path.dirname(__file__), LOG_FOLDER))

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), LOG_FOLDER,
                                          f'{datetime.datetime.today().date()}.txt'),
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s\t:  %(message)s',
                    datefmt='%d.%m.%Y-%H:%M:%S')


def get_response(url: str) -> Union[bytes, str]:
    try:
        time.sleep(random.uniform(0.01, 1))
        r = requests.get(url, timeout=60)
        return r.content
    except Exception as e:
        logging.error(f"Got error during getting response\nError = {e}")
        return ''


def create_serps_pool() -> list:
    return [f'{SITE_SERP_URL}{page_num}' for page_num in range(1, LAST_PAGE + 1)]


def parse_job(job_card: BeautifulSoup) -> dict:
    tag = job_card.find('a', attrs={'class': re.compile(r'ga_listing')})
    company = job_card.find('a', attrs={'class': re.compile(r'company-profile-name')}).text
    salary = job_card.find('span', attrs={'class': re.compile(r'salary')}).text
    region = job_card.find('span', attrs={'class': re.compile(r'location')}).text
    posted_at = job_card.find('div', attrs={'class': re.compile(r'publication-time')}).text
    description = job_card.find('div', attrs={'class': re.compile(r'card-description')}).text
    job_url = f"{JOB_URL}{tag.get('href')}"

    return {
        'url': job_url,
        'title': tag.text,
        'company': company,
        'job_type': 'Full time',
        'salary': salary.replace('\xa0', ' '),
        'region': region,
        'posted_at': dateparser.parse(posted_at) + datetime.timedelta(milliseconds=100),
        'remote_type': '',
        'description': description + '  MORE ON rabota.ua'
    }


def get_jobs_from_serp(serp_link: str):
    try:
        soup = BeautifulSoup(get_response(serp_link), 'html.parser')
        job_cards = soup.find_all(
            'article', attrs={'class': re.compile(r'card')}
        )
        return [Job(**job) for job in map(parse_job, job_cards)]
    except Exception as e:
        logging.error(f"Error in jobs_cards parsing = {e}")


def main():
    logging.info("Start parse Rabota.UA")
    serps = create_serps_pool()
    for idx in range(0, len(serps), BATCH_SIZE):
        with Pool(WORKERS) as pool:
            jobs = list(
                itertools.chain(
                    *pool.map(get_jobs_from_serp, serps[idx: idx + BATCH_SIZE])
                )
            )
        db_insert_many(db, [job for job in jobs if job is not None], lock)
        logging.info(f"Stored {len(jobs)} jobs!")


if __name__ == '__main__':
    main()
