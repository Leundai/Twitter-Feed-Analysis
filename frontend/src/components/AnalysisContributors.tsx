import { Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { TwitterMentionButton, TwitterTweetEmbed } from "react-twitter-embed";
import { Cell, Legend, Pie, PieChart, ResponsiveContainer } from "recharts";
import {
  EmotionsContributors,
  EmotionContributors,
  ClassifiedTweets,
  EmotionCount,
  ClassifiedTweet,
  AuthorsInfo,
} from "../types/analysisInterface";

import "./AnalysisContributors.css";
import { maxEmotion } from "./AnalysisHeader";

interface FormattedAuthor {
  tweetId: string;
  authorId: string;
  pieData: {
    name: string;
    value: number;
  }[];
}

const tweetOptions = {
  theme: "dark",
  hide_media: true,
  conversation: "none",
  cards: "hidden",
  width: 550,
};

const MAX_TWEET_DISPLAY = 3;

const formatData = (
  emotionContributors: EmotionContributors,
  emotion: string,
  classifiedTweets: ClassifiedTweets,
  emotionCount: number
): FormattedAuthor[] => {
  const authors = emotionContributors;
  const formattedAuthors = Object.keys(authors)
    .sort((a, b) => emotionContributors[b] - emotionContributors[a])
    .map((authorId) => {
      const topTweet = Object.values(classifiedTweets)
        .filter(
          (tweet) =>
            tweet.author_id === authorId && tweet.max_emotion === emotion
        )
        .sort(
          (a, b) =>
            Number(a[emotion as keyof ClassifiedTweet]) -
            Number(b[emotion as keyof ClassifiedTweet])
        )[0];
      return {
        tweetId: topTweet.tweet_id,
        authorId: authorId,
        pieData: [
          {
            name: "Contributed",
            value: emotionContributors[authorId as keyof EmotionContributors],
          },
          {
            name: "Total tweets of this emotion",
            value: emotionCount,
          },
        ],
      };
    });
  return formattedAuthors;
};

type Props = {
  emotionsContributors: EmotionsContributors;
  classifiedTweets: ClassifiedTweets;
  emotionCount: EmotionCount;
  authorsInfo: AuthorsInfo;
};

function AnalysisContributors({
  emotionsContributors,
  classifiedTweets,
  emotionCount,
  authorsInfo,
}: Props) {
  const [tableData, setTableData] = useState<FormattedAuthor[]>();
  const [emotion, setEmotion] = useState<string>();
  const [loadedTweets, setLoadedTweets] = useState<boolean[]>(
    Array(MAX_TWEET_DISPLAY).fill(false)
  );
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const newEmotion = maxEmotion(emotionCount);
    setEmotion(newEmotion);

    setTableData(
      formatData(
        emotionsContributors[newEmotion as keyof EmotionsContributors],
        newEmotion,
        classifiedTweets,
        emotionCount[newEmotion as keyof EmotionCount]
      )
    );
  }, [classifiedTweets, emotionCount, emotionsContributors]);

  const formatTitle = () =>
    tableData && (
      <Typography color="white" variant="h4">
        Top {tableData.length > 1 && tableData.length} Contributor
        {tableData.length > 1 && "s"} of {emotion}
      </Typography>
    );

  return (
    <div className="contributor-container">
      {formatTitle()}
      {tableData &&
        tableData.map((authorData, index) => (
          <div key={`card-${index}`} className="contributor-card">
            <div className="tweet-card">
              <TwitterTweetEmbed
                tweetId={authorData.tweetId}
                options={tweetOptions}
                onLoad={(element) => {
                  if (element !== undefined) {
                    setLoadedTweets((prevState: boolean[]): boolean[] => {
                      const newLoaded = [...prevState];
                      newLoaded[index] = true;
                      return newLoaded;
                    });
                  }
                  setLoading(false);
                }}
              />
              {!loading && true && (
                <Typography color="white" variant="h4">
                  Could Not Load The Tweet 😭
                  <TwitterMentionButton
                    screenName={authorsInfo[authorData.authorId].username}
                    options={{ size: "large" }}
                  />
                </Typography>
              )}
            </div>
            <ResponsiveContainer width="40%" height={300} minWidth={300}>
              <PieChart>
                <Legend verticalAlign="top" height={36} />
                <Pie
                  data={authorData.pieData}
                  nameKey="name"
                  dataKey="value"
                  cx="50%"
                  cy="50%"
                  innerRadius={50}
                  outerRadius={80}
                  paddingAngle={5}
                  label
                >
                  {authorData.pieData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={index === 0 ? "#29B6F6" : "white"}
                    />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>
        ))}
    </div>
  );
}

export default AnalysisContributors;
