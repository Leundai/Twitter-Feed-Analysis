import time
from api import create_app
from api.helpers.task_helpers import _set_task_progress
from api.core import logger
import sys

# Create the app in order to operate within the context of the app
app = create_app()


def analyze_profile() -> None:
    """
    A background task that uses Twitter API and runs emotion detection on all collected tweets
    """
    pass


# def count_seconds(seconds: int) -> None:
#     """
#     A background task which counts up to the number of seconds passed as an argument
#     """
#     with app.app_context():
#         logger.info("Running task count seconds")
#         try:
#             number = seconds
#             _set_task_progress(0)

#             i = 0

#             for i in range(0, number):
#                 i += 1
#                 time.sleep(1)
#                 _set_task_progress(100 * i // number)

#         except:
#             logger.error("Unhandled exception", exc_info=sys.exc_info())

#         finally:
#             _set_task_progress(100)
