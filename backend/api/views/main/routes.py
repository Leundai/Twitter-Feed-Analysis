from flask import current_app, request
from api import limiter
from api.views.main import bp
from api.utils.scripts import NpEncoder
from api.core import create_response, logger
from api.models import TaskProfile
import json

# TODO: customize this to be to a specific user id
# with oauth
@bp.route("/analyze/<user_id>", methods=["GET"])
@limiter.exempt
def start_analyzing(user_id):
    logger.info(user_id)
    try:
        task: TaskProfile = TaskProfile.objects.get(user_id=user_id)
    except Exception as e:
        logger.error(e)
        return create_response(status=500, message="Task doesn't exist or has expired")

    if task.task_id:
        return create_response(data={"taskId": task.task_id})

    rq_job = current_app.task_queue.enqueue(
        "api.tasks.twitter_analysis.analyze_profile.analyze_profile",
        (task.access_token, task.access_secret),
    )
    task.task_id = rq_job.get_id()
    logger.info(task.task_id)
    task.save()

    return create_response(data={"taskId": task.task_id})


@bp.route("/analysis_status/<task_id>", methods=["GET"])
@limiter.exempt
def get_analysis_status(task_id):
    logger.info(task_id)
    # TODO: Add validators here
    if task_id is None or not task_id:
        return create_response(status=400, message="Missing task id/invalid task_id")

    try:
        task: TaskProfile = TaskProfile.objects.get(task_id=task_id)
    except Exception as e:
        logger.error(e)
        return create_response(status=500, message="Task doesn't exist or has expired")

    task_progress = task.get_progress()
    if task_progress is None:
        return create_response(status=500, message="Task has expired")
    return create_response(data={"progress": task_progress})


@bp.route("/results/<task_id>", methods=["GET"])
@limiter.exempt
def get_results(task_id):
    logger.info(task_id)
    # TODO: Add validators here
    if task_id is None or not task_id:
        return create_response(status=400, message="Missing task id/invalid task_id")

    try:
        task: TaskProfile = TaskProfile.objects.get(task_id=task_id)
    except Exception as e:
        logger.error(e)
        return create_response(status=400, message="Task doesn't exist or has expired")

    task_progress = task.get_progress()
    if task_progress is None:
        return create_response(status=400, message="Task has expired")
    elif task_progress < 100:
        logger.info("Task result is incomplete")
        return create_response(status=400, message="Task result is in progress")

    task_result = task.get_result()
    # Convert any missing np.dtypes to primitive types
    json_dump = json.dumps(task_result, cls=NpEncoder)
    converted_data = json.loads(json_dump)

    task.delete()
    return create_response(data={"data": converted_data})
