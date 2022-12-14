from flask import current_app, request
from api.views.main import bp
from api.utils.scripts import NpEncoder
from api.core import create_response, logger
from api.models import TaskProfile
import json

# TODO: customize this to be to a specific user id
# with oauth
@bp.route("/analyze", methods=["GET"])
def start_analyzing():
    req_body = request.json
    user_id = req_body.get("user_id", None)

    try:
        task: TaskProfile = TaskProfile.objects.get(user_id=user_id)
    except Exception as e:
        logger.error(e)
        return create_response(status=500, message="Task doesn't exist or has expired")

    rq_job = current_app.task_queue.enqueue(
        "api.tasks.twitter_analysis.analyze_profile.analyze_profile",
        (task.access_token, task.access_secret),
    )
    task.task_id = rq_job.get_id()
    logger.info(task.task_id)
    task.save()

    return create_response(data={"request_id": task.task_id})


@bp.route("/analysis_status", methods=["GET"])
def get_analysis_status():
    req_body = request.json
    task_id = req_body.get("task_id", None)

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
    elif task_progress >= 100:
        logger.info("calling task result")
        task_result = task.get_result()
        task.delete()

        # Convert any missing np.dtypes to primitive types
        json_dump = json.dumps(task_result, cls=NpEncoder)
        converted_data = json.loads(json_dump)

        return create_response(
            data={"progress": task_progress, "result": converted_data}
        )
    return create_response(data={"progress": task_progress})
