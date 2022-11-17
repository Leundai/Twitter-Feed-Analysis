# from api.core import Mixin
from flask_mongoengine import Document
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
        try:
            rq_job = rq.job.Job.fetch(self.task_id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            current_app.logger.info("Failed to get rq job")
            return None

        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        current_app.logger.info(job.get_status())
        return job.meta.get("progress", 0) if job is not None else 100

    def __repr__(self):
        return f"""<TaskProfile {self.task_id} {self.name} {self.complete}>"""
