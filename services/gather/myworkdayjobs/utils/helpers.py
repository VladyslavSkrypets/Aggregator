import re
import dateparser
import requests
import datetime
import logging


def split_url(url: str) -> list:
    url_parts = re.search(r"//(.+?)/(.+?)(/|\?|$)", url)
    return [url_parts.group(1), url_parts.group(2)] if url_parts else [None] * 2


def parse_remote_type(region: str) -> str:
    return '1' if re.findall(r"\s(remote|home\s*based)\s", region, re.IGNORECASE) else ''


def date_parser(date_raw: str) -> dateparser.date:
    date = ' '.join(re.sub(r"(\+|Posted\d*)", "", date_raw).split()).capitalize()
    return dateparser.parse(date, settings={'TIMEZONE': 'UTC'}, date_formats=["%Y-%m-%d"])


def get_jobs_count(url: str) -> int:
    jobs_count = 0
    try:
        response = requests.get(url, timeout=60)
        jobs_count = response.json().get('body').get('children')[0] \
            .get('facetContainer').get('paginationCount').get('value')
        return jobs_count if isinstance(jobs_count, int) else 0
    except Exception as e:
        logging.error(f"Got Error during parsing company info !\nError = {e}")
        return jobs_count


def records_expired(expire_at: datetime.date) -> bool:
    return expire_at <= datetime.datetime.strptime(
        datetime.datetime.utcnow().strftime("%Y-%m-%d"), "%Y-%m-%d"
    )


def remove_expire_jobs(db, table) -> None:
    expire_date = datetime.datetime.utcnow() - datetime.timedelta(days=45)
    db.query(table).filter(table.posted_at <= expire_date).delete()
    db.commit()
