import uuid
from services.schema import GatherJobSchema
from typing import List
from services.indexer.helpers import update_service_state
from services.gather.database import Job as gather_job, init_db
from services.indexer.database import Job as prod_job, init_prod_db


class Indexer:
    __job_batch_size = 10_000

    def __init__(self):
        self.__gather_db = init_db()
        self.__prod_db = init_prod_db()
        self._max_jobs = self.__gather_db.query(gather_job).count()
        self._current_insert_size = 0

    @property
    def _batch_size(self) -> int:
        return self.__job_batch_size

    def _get_gathered_jobs(self) -> list:
        jobs_batch = (
            self.__gather_db.query(gather_job)
            .order_by(gather_job.id)
            .offset(self._current_insert_size)
            .limit(self._batch_size)
            .all()
        )
        return GatherJobSchema().dump(jobs_batch, many=True)

    def _check_exist_urls(self, job_info_list: List[dict]):
        exist_urls = set(
            map(
                lambda record: record.url,
                self.__prod_db.query(prod_job).filter(
                    prod_job.url.in_({job['url'] for job in job_info_list})
                )
            )
        )
        batch_unique_urls = {job['url'] for job in job_info_list}
        new_jobs = [
            job for job in job_info_list
            if job['url'] not in exist_urls and job['url'] in batch_unique_urls
        ]

        return [prod_job(**{**new_job, 'uid': uuid.uuid4()}) for new_job in new_jobs]

    def _add_batch(self, data: List[dict]) -> None:
        for job in data:
            self.__prod_db.add(job)
            self._current_insert_size += 1

        self.__prod_db.commit()

    def run(self):
        while self._current_insert_size < self._max_jobs:
            gathered_jobs = self._get_gathered_jobs()
            new_jobs = self._check_exist_urls(gathered_jobs)
            self._add_batch(new_jobs)


if __name__ == '__main__':
    update_service_state('Gather', False)
    update_service_state('Indexer', True)
    indexer = Indexer()
    indexer.run()
    update_service_state('Indexer', False)
