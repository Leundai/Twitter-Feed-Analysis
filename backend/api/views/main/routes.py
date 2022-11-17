from uuid import uuid4
from flask import current_app, request
from api.views.main import bp
from api.core import create_response, logger
from api.models import TaskProfile

# GET request for /accounts/<type>
@bp.route("/secret", methods=["GET"])
def get_secret():

    logger.info("Getting Secret")
    return create_response(data={"secret": "Hello"})


@bp.route("/analyze", methods=["GET"])
def start_analyzing():
    logger.info("About to create new profile")
    new_profile = TaskProfile()
    logger.info("About to queue this into Redis Queue")
    rq_job = current_app.task_queue.enqueue(
        "api.tasks.analyze_profile.count_seconds", 15
    )
    new_profile.task_id = rq_job.get_id()
    logger.info("About to save this into mongodb")
    new_profile.save()
    logger.info("Successfully saved this")

    return create_response(data={"request_id": rq_job.get_id()})


@bp.route("/analysis_status", methods=["GET"])
def get_analysis_status():
    req_body = request.json
    task_id = req_body.get("task_id", None)

    # TODO: Add data checkers here
    if task_id is None or not task_id:
        return create_response(status=400, message="Missing task id/invalid task_id")

    try:
        task = TaskProfile.objects.get(task_id=task_id)
    except Exception as e:
        logger.error(e)
        return create_response(status=500, message="Failed to get task")

    return create_response(data={"progress": task.get_progress()})
