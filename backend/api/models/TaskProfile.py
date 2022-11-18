# from api.core import Mixin
from flask_mongoengine import Document
from api.core import logger
from flask import current_app
from mongoengine import StringField, BooleanField
import redis
import rq


class TaskProfile(Document):
    """User Profile Collection."""

    task_id = StringField()
    name = StringField()
    result = StringField()
    complete = BooleanField(default=False)

    def get_rq_job(self):
        """Query for rq job and returns job instance

        :returns None if expired or does not exist
        """
        try:
            rq_job = rq.job.Job.fetch(self.task_id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            logger.error("Failed to get rq job")
            return None

        return rq_job

    def get_progress(self):
        """Query for rq job and returns job progress

        :returns None if expired or does not exist
        """
        job = self.get_rq_job()
        return None if job is None else job.meta.get("progress", 0)

    def get_result(self):
        """Query for rq job and returns job result

        :returns None if expired or does not exist
        """
        job = self.get_rq_job()
        return None if job is None else job.result

    def __repr__(self):
        return f"""<TaskProfile {self.task_id} {self.name} {self.complete}>"""
