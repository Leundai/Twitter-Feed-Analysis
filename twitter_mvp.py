from dotenv import load_dotenv
import os
from tweepy import Client
from transformers import pipeline
import concurrent.futures
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pprint
import re

pp = pprint.PrettyPrinter()


# Load env variables
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
TWITTER_BEARER = os.environ.get("TWITTER_BEARER")
twitter_auth = {
    "bearer_token": TWITTER_BEARER,
    "consumer_key": TWITTER_API_KEY,
    "consumer_secret": TWITTER_API_SECRET,
    "access_token": TWITTER_ACCESS_TOKEN,
    "access_token_secret": TWITTER_ACCESS_SECRET,
}

twitter_client = Client(**twitter_auth)

emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None,
)

EMOTIONS = ["anger", "disgust", "joy", "fear", "neutral", "sadness", "surprise"]


def remove_urls(text):
    # Use a regular expression to search for URLs in the input string
    # and replace them with an empty string
    return re.sub(r"https?://\S+", "", text)


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
        print(e)
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


def twitter_analysis(user_id):
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

        print(current_timeline.meta.get("result_count", None))

        if current_timeline.data is None:
            continue

        tweet_list.extend(
            [
                (tweet.id, remove_urls(tweet.text), tweet.author_id, tweet.created_at)
                for tweet in current_timeline.data
                if remove_urls(tweet.text) != ""
            ]
        )

    print(len(tweet_list))

    prediction_results = pd.DataFrame()

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = []

        # Start up threads
        for tweet in tweet_list:
            futures.append(executor.submit(classify_tweet, tweet))

        # Process thread results
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                new_row = result.to_frame().T
                prediction_results = pd.concat(
                    [new_row, prediction_results],
                    ignore_index=True,
                )
            except Exception as e:
                print(e)
                print("ConnectTimeout.")

    # Force all prediction results to respective types
    tweet_metadata = ["tweet_id", "author_id"]
    prediction_results[EMOTIONS] = prediction_results[EMOTIONS].astype(np.float64)
    prediction_results[tweet_metadata] = prediction_results[tweet_metadata].astype(
        np.int64
    )

    # Display overall emotion of the home feed
    # Including breakdown of each emotion
    max_emotion_per_row = prediction_results[EMOTIONS].idxmax(axis=1)
    emotion_count = max_emotion_per_row.value_counts().to_dict()
    pp.pprint(emotion_count)

    # Largest feed contributors to each emotion
    prediction_results["max_emotion"] = max_emotion_per_row
    emotion_contributors = dict()
    for emotion in EMOTIONS:
        filtered_results = prediction_results[
            prediction_results["max_emotion"] == emotion
        ]
        author_occurance = filtered_results.value_counts(subset=["author_id"])
        max_occurance = author_occurance.max()
        max_authors = author_occurance[author_occurance == max_occurance].index.tolist()
        emotion_contributors[emotion] = {
            "occurance": max_occurance,
            "author_ids": [x[0] for x in max_authors],
        }
    pp.pprint(emotion_contributors)

    # Most emotional tweets
    max_emotion_per_column = prediction_results[EMOTIONS].idxmax()
    max_emotional_tweets = (
        prediction_results.take(max_emotion_per_column.values.tolist())
        .drop(EMOTIONS, axis=1)
        .to_dict("records")
    )
    pp.pprint(max_emotional_tweets)

    # Fluctuation of your Twitter feed emotions over time
    classified_tweets = prediction_results.drop(EMOTIONS, axis=1).to_dict("records")
    pp.pprint(classified_tweets[:5])


res = twitter_client.get_me()
user = res.data
print(user.id)
twitter_analysis(user.id)
