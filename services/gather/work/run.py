import re
import os
import time
import logging
import itertools
import datetime
import requests
import random
from typing import List, Union, Dict
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from services.gather.database import db_insert_many, init_db, Job
from .config import API_SERP_URL, SITE_SERP_URL, JOB_URL, BATCH_SIZE, LOG_FOLDER


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


def get_last_page_number() -> int:
    try:
        soup = BeautifulSoup(get_response(SITE_SERP_URL), 'html.parser')
        pages_range = re.findall(r"\d+", soup.find('span', attrs={'class', 'text-default'}).text)
        last_page = max(map(int, pages_range))
        logging.info(f"Got last number of page = {last_page}")
        return last_page
    except Exception as e:
        logging.error(f"Got error during getting last page number\nError = {e}")
        return 0


def parse_job(job_card: BeautifulSoup) -> dict:
    tag = job_card.find('a', attrs={'href': re.compile(r'/ru/jobs/\d+')})
    job_url = f"{JOB_URL}{tag.get('href')}"
    additional_info = get_job_page_info(job_url)
    return {
        'url': job_url,
        'title': tag.text,
        **additional_info
    }


def get_jobs_from_serp(serp_link: str) -> Union[List[dict], None]:
    try:
        soup = BeautifulSoup(get_response(serp_link), 'html.parser')
        job_cards = soup.find_all(
            'div', attrs={'class': re.compile(r'card card-hover card-visited wordwrap job-link.*')}
        )
        return [Job(**job) for job in map(parse_job, job_cards)]
    except Exception as e:
        logging.error(f"Error in jobs_cards parsing = {e}")


def create_serps_pool() -> List[str]:
    last_page = get_last_page_number()
    return [API_SERP_URL.format(page_num) for page_num in range(1, last_page + 1)]


def get_job_page_info(job_link: str) -> Dict:
    soup = BeautifulSoup(get_response(job_link), 'html.parser')
    salary, region, company, description = [''] * 4
    try:
        salary = soup.find(
            'span', attrs={'title': 'Зарплата'}
        ).next_sibling.text
    except Exception as e:
        logging.error(f"Can not parse salary field\nError = {e}")
    try:
        company = soup.find(
            'a', attrs={'href': re.compile(r'/ru/jobs/by-company/\d*')}
        ).next_sibling.text
    except Exception as e:
        logging.error(f"Can not parse company field\nError = {e}")
    try:
        region = soup.find(
            'span', attrs={'title': 'Адрес работы'}
        ).next_sibling.text
    except Exception as e:
        logging.error(f"Can not parse region field\nError = {e}")

    description = soup.find('div', attrs={'id': 'job-description'})
    return {
        'region': region.strip(),
        'job_type': 'Full time',
        'remote_type': '',
        'posted_at': datetime.datetime.utcnow(),
        'company': company.strip(),
        'salary': salary.strip(),
        'description': str(description).strip()
    }


if __name__ == '__main__':
    logging.info("Start parse WORK.UA")
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




