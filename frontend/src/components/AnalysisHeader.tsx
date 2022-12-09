import React, { useEffect, useState } from "react";
import { Typography } from "@mui/material";
import { EmotionCount, EmotionKey } from "../types/analysisInterface";
import { emojiMap } from "../utils/constants";

type Props = {
  emotionCount: EmotionCount;
};

const maxEmotion = (emotionCount: EmotionCount): string =>
  Object.keys(emotionCount).reduce((a: string, b: string) => {
    const aKey = a as EmotionKey;
    const bKey = b as EmotionKey;
    return emotionCount[aKey] > emotionCount[bKey] ? a : b;
  });

const getEmoji = (emotion: string): string => emojiMap[emotion as EmotionKey];

const sumTweetCount = (emotionCount: EmotionCount) =>
  Object.values(emotionCount).reduce((a, b) => a + b, 0);

const emotionShare = (
  emotionCount: EmotionCount,
  maxEmotion: string
): string => {
  const total: number = sumTweetCount(emotionCount);
  const percent: number =
    (emotionCount[maxEmotion as EmotionKey] / total) * 100;
  return percent.toPrecision(3);
};

// TODO: Handle the case with ties
function AnalysisHeader({ emotionCount }: Props) {
  const [emotion, setEmotion] = useState("😐");

  useEffect(() => {
    setEmotion(maxEmotion(emotionCount));

    return () => {
      setEmotion("😐");
    };
  }, [emotionCount]);

  return (
    <div>
      <Typography variant="h1">{getEmoji(emotion)}</Typography>
      <Typography variant="h4" color="white">
        Your twitter feed feels {emotion}
      </Typography>
      <Typography variant="h5" color="white">
        {`${emotionShare(emotionCount, emotion)}% `}
        of {sumTweetCount(emotionCount)} tweets
      </Typography>
    </div>
  );
}

export default AnalysisHeader;
