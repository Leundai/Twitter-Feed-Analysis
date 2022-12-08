from rq import get_current_job
from api.models import TaskProfile
from api.core import logger


def _set_task_progress(progress: int, data_result=None) -> None:
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
        logger.info(progress)

        if progress >= 100:
            try:
                task = TaskProfile.objects.get(task_id=job.get_id())
                if task.complete:
                    return
                task.complete = True
                task.save()

                job.meta["result"] = data_result
                job.save_meta()
                logger.info(f"Finished Task {job.get_id()}")
            except Exception as e:
                logger.error(e)
