import { CircularProgress, Typography } from "@mui/material";
import React, { useState } from "react";
import { TwitterTweetEmbed } from "react-twitter-embed";
import { ClassifiedTweets } from "../types/analysisInterface";

import "./AnalysisTopTweets.css";

type Props = {
  topEmotionalTweets: ClassifiedTweets;
};

const tweetOptions = {
  theme: "dark",
  hide_media: true,
  conversation: "none",
  cards: "hidden",
  width: 550,
};

function AnalysisTopTweets({ topEmotionalTweets }: Props) {
  const [loadedTweets, setLoadedTweets] = useState<boolean[]>(
    Array(7).fill(true)
  );
  const [loading, setLoading] = useState<boolean>(true);

  return (
    <div className="top-tweets-container">
      <Typography color="white" variant="h4">
        Most Emotional Tweets
      </Typography>
      <div className="top-tweet-cards">
        {topEmotionalTweets.map((tweet, index) => (
          <div className="top-tweet-card">
            <Typography color="#29B6F6" variant="h4" marginBottom=".5em">
              {tweet.max_emotion}
            </Typography>
            <TwitterTweetEmbed
              key={`top-tweet-${index}`}
              tweetId={tweet.tweet_id}
              options={tweetOptions}
              placeholder={<CircularProgress />}
              onLoad={(element) => {
                if (element === undefined) {
                  setLoadedTweets((prevState: boolean[]): boolean[] => {
                    const newLoaded = [...prevState];
                    newLoaded[index] = false;
                    return newLoaded;
                  });
                }
                setLoading(false);
              }}
            />
            {!loading && !loadedTweets[index] && (
              <div className="top-tweet-unavailable">
                <Typography color="white" variant="h5">
                  Could Not Load Tweet 😭
                </Typography>
                <Typography color="#29B6F6" variant="h5">
                  "{tweet.content}"
                </Typography>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default AnalysisTopTweets;
