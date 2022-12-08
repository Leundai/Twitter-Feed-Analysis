from api import create_app, emotion_classifier
from api.helpers.task_helpers import _set_task_progress
from api.core import logger
from api.utils.constants import EMOTIONS
from api.utils.scripts import remove_urls
from tweepy import Client
import concurrent.futures
from datetime import datetime, timedelta
import pandas as pd
import pprint

pp = pprint.PrettyPrinter()

# Create the app in order to operate within the context of the app
app = create_app()


def classify_tweet(args: tuple) -> pd.Series:
    """Thread worker function classifies text and
    converts to a row for a Dataframe

    Args:
        args (tuple): Tweet Metadata Parameters

    Returns:
        pd.Series: Formatted row for analysis
    """
    tweet_id, text, author_id, created_at = args

    try:
        # emotion_classifier returns an array hence [0]
        predictions = emotion_classifier(text)[0]
    except Exception as e:
        logger.error(e)
        return {}

    result = {
        "tweet_id": tweet_id,
        "content": text,
        "author_id": author_id,
        "created_at": created_at,
    }

    for prediction in predictions:
        result[prediction["label"]] = prediction["score"]

    return pd.Series(result)


def analyze_profile() -> None:
    """
    A background task that uses Twitter API and runs emotion detection on all collected tweets
    """
    with app.app_context():
        twitter_client: Client = app.config["TWITTER_CLIENT"]
        res = twitter_client.get_me()
        user = res.data
        logger.info(f"Twitter User ID: {user.id}")

        current_time = datetime.now()
        tweet_list = []

        # TODO: Put this more specific to a local timezone to be more accurate of a day activity
        for _ in range(28):
            prev_hour_time = current_time - timedelta(hours=6)
            current_timeline = twitter_client.get_home_timeline(
                expansions=["author_id"],
                tweet_fields=["created_at"],
                start_time=prev_hour_time,
                end_time=current_time,
            )
            current_time -= timedelta(hours=6)

            if current_timeline.data is None:
                continue

            tweet_list.extend(
                [
                    (
                        tweet.id,
                        remove_urls(tweet.text),
                        tweet.author_id,
                        tweet.created_at,
                    )
                    for tweet in current_timeline.data
                    if remove_urls(tweet.text) != ""
                ]
            )

        logger.info(f"Tweet count: {len(tweet_list)}")

        prediction_results = pd.DataFrame()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []

            tweet_len = len(tweet_list)
            # Start up threads
            for tweet in tweet_list:
                futures.append(executor.submit(classify_tweet, tweet))

            progress_index = 0
            # Process thread results
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    new_row = result.to_frame().T
                    prediction_results = pd.concat(
                        [new_row, prediction_results],
                        ignore_index=True,
                    )
                    progress_index += 1
                    _set_task_progress(int(90 * progress_index / tweet_len))
                except Exception as e:
                    logger.error(e)
                    logger.error("ConnectTimeout.")

        # Force all prediction results to respective types
        tweet_metadata = ["tweet_id", "author_id"]
        prediction_results[EMOTIONS] = prediction_results[EMOTIONS].astype(float)
        prediction_results[tweet_metadata] = prediction_results[tweet_metadata].astype(
            int
        )
        prediction_results["created_at"] = prediction_results["created_at"].astype(str)

        # Display overall emotion of the home feed
        # Including breakdown of each emotion
        max_emotion_per_row = prediction_results[EMOTIONS].idxmax(axis=1)
        emotion_count = max_emotion_per_row.value_counts().to_dict()

        # Largest feed contributors to each emotion
        prediction_results["max_emotion"] = max_emotion_per_row
        emotion_contributors = dict()
        for emotion in EMOTIONS:
            filtered_results = prediction_results[
                prediction_results["max_emotion"] == emotion
            ]
            author_occurance = filtered_results.value_counts(subset=["author_id"])
            max_occurance = author_occurance.max()
            max_authors = author_occurance[
                author_occurance == max_occurance
            ].index.tolist()
            emotion_contributors[emotion] = {
                "occurance": max_occurance,
                "author_ids": [x[0] for x in max_authors],
            }

        # Most emotional tweets
        max_emotion_per_column = prediction_results[EMOTIONS].idxmax()
        max_emotional_tweets = (
            prediction_results.take(max_emotion_per_column.values.tolist())
            .drop(EMOTIONS, axis=1)
            .to_dict("records")
        )

        # Fluctuation of your Twitter feed emotions over time
        classified_tweets = prediction_results.drop(EMOTIONS, axis=1).to_dict("records")

        # Consolidate all data and analysis
        analysis_result = {
            "emotion_count": emotion_count,
            "emotion_contributors": emotion_contributors,
            "max_emotional_tweets": max_emotional_tweets,
            "classified_tweets": classified_tweets,
        }
        _set_task_progress(100, analysis_result)
