import re
import dateparser
import requests
import datetime
from itertools import chain
from bs4 import BeautifulSoup
from multiprocessing import Pool, Lock
from services.gather.database import db_insert_many, init_db, Job

lock = Lock()
db = init_db()

job_page_url = 'https://happymonday.ua'
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; J00bleb0t/2.0; Windows NT 6.1; WOW64; +http://j00ble.0rg/j00ble-b0t) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'
}


def get_page(url: str) -> str:
    r = requests.get(url, headers=headers, timeout=60)
    return r.text


def make_soup(page_html: str):
    soup = BeautifulSoup(page_html, 'html.parser')
    return soup


def parse_job_data(job_url: str) -> dict:
    job_page = get_page(job_url)
    job_page_soup = make_soup(job_page)
    job_title = job_page_soup.find('h1', attrs={'class': 'js__post-title'}).text
    job_url = job_page_soup.find('h1', attrs={'class': 'js__post-title'}).get('data-link')
    job_region, job_type = job_page_soup.findAll('div', attrs={'class': 'single-vacancy__meta-location'})
    job_description = job_page_soup.find('div', attrs={'class': re.compile('single-vacancy__text main-text.*')})
    job_updated = job_page_soup.find('b', string=re.compile('Опубліковано.*')).next_sibling
    try:
        job_company = job_page_soup.find(re.compile(r"\D+"), attrs={"class": "single-vacancy__meta-place"}).text
    except Exception as e:
        print(e)
        job_company = ''
    return {
        'title': job_title,
        'url': f"{job_page_url}{job_url}",
        'company': job_company.strip(),
        'region': job_region.text.strip(),
        'job_type': job_type.text.strip() if job_type is not None else '',
        'description': str(job_description).replace('\n', ''),
        'posted_at': dateparser.parse(job_updated.strip()) + datetime.timedelta(milliseconds=500),
        'salary': '',
        'remote_type': '1' if (job_type.text.strip() if job_type is not None else '') == 'Remote' else '0'
    }


def create_serps() -> list:
    last_page = 20
    page_url = 'https://happymonday.ua/jobs-search/page/'
    return [f'{page_url}{page_num}' for page_num in range(1, last_page)]


def get_jobs_urls(page_html: str) -> list:
    try:
        soup = make_soup(page_html)
        div_block_urls = soup.find_all('div', attrs={'class': 'vacancies__search-item__title'})
        urls = list(map(lambda div: f"{job_page_url}{div.findChild().get('href')}", div_block_urls))
        return urls
    except Exception as e:
        print('Can not parse this page!')
        print('Error = ', e)


def main():
    serps = create_serps()
    with Pool(10) as pool:
        pages = pool.map(get_page, serps)
        jobs_urls = list(chain(*pool.map(get_jobs_urls, pages)))
        jobs = [Job(**job) for job in pool.map(parse_job_data, jobs_urls)]

    db_insert_many(db, jobs, lock)


if __name__ == '__main__':
    main()
