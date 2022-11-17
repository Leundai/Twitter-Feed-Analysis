from rq import get_current_job
from api import db
from api.models import TaskProfile
from api.core import logger


def _set_task_progress(progress: int) -> None:
    """
    A helper function which updates the progress status of a background task

    Parameters
    ----------
    progress : int
        The percentage of the task progress
    """
    job = get_current_job()
    if job:

        job.meta["progress"] = progress
        job.save_meta()

        if progress >= 100:
            try:
                task = TaskProfile.objects.get(task_id=job.get_id())
                task.complete = True
                task.save()
            except Exception as e:
                logger.error(e)
