from uuid import uuid4
from flask import current_app, request
from api.views.main import bp
from api.core import create_response, logger
from api.models import TaskProfile


@bp.route("/analyze", methods=["GET"])
def start_analyzing():
    new_profile = TaskProfile()
    rq_job = current_app.task_queue.enqueue(
        "api.tasks.analyze_profile.count_seconds", 2
    )
    new_profile.task_id = rq_job.get_id()
    logger.info(new_profile.task_id)
    new_profile.save()

    return create_response(data={"request_id": rq_job.get_id()})


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
        logger.info(task_result)
        task.delete()
        return create_response(data={"progress": task_progress, "result": task_result})
    return create_response(data={"progress": task_progress})
