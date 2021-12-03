from backend import db
from sqlalchemy import desc, asc
from backend.models import Job, JobClicks
from backend.schemas.schema import JobSerpSchema


class SerpConstructor:
    __JOBS_PER_PAGE = 20

    def __init__(self, payload: dict):
        self._payload = payload
        self.__base_query = self.__get_base_query()
        self._page = payload['page']

    @property
    def jobs_per_page(self):
        return self.__JOBS_PER_PAGE

    @staticmethod
    def __get_base_query():
        base_query = (
            db.session.query(Job, JobClicks)
            .outerjoin(JobClicks, Job.uid == JobClicks.uid)
            .order_by(asc(JobClicks.count_clicks))
            .order_by(desc(Job.posted_at))
        )

        return base_query

    def _get_applied_filters(self) -> dict:
        return {
            filter_name: filter_value
            for filter_name, filter_value in self._payload.items()
            if bool(filter_value) and filter_name != 'page'
        }

    def _add_title_filter(self, title: str):
        self.__base_query = self.__base_query.filter(Job.title.like(f'%{title}%'))

    def _add_region_filter(self, region: str):
        self.__base_query = self.__base_query.filter(Job.region.like(f'%{region}%'))

    def _add_job_type_filter(self):
        self.__base_query = self.__base_query.filter(Job.job_type.like('%Full%'))

    def _add_remote_type_filter(self):
        self.__base_query = self.__base_query.filter(Job.remote_type == '1')

    def _add_salary_filter(self, salary: str):
        self.__base_query = self.__base_query.filter(Job.salary.like(f'%{salary}%'))

    def _add_pagination(self):
        self.__base_query = (
            self.__base_query
            .offset((self._page - 1) * self.__JOBS_PER_PAGE)
            .limit(self.__JOBS_PER_PAGE)
        )

    def get_jobs(self) -> list:
        applied_filters = self._get_applied_filters()
        filters_methods = {
            'job-title': self._add_title_filter,
            'job-region': self._add_region_filter,
            'remote-type': self._add_remote_type_filter,
            'job-type': self._add_job_type_filter,
            'salary': self._add_salary_filter
        }
        for filter_name, filter_value in applied_filters.items():
            if filter_name in {'job-type', 'remote-type'}:
                filters_methods[filter_name]()
            else:
                filters_methods[filter_name](filter_value)

        self._add_pagination()
        query_items_result = [model[0] for model in self.__base_query.all()]
        return JobSerpSchema().dump(query_items_result, many=True)
