import React from "react";
import { Bar, BarChart, Cell, ResponsiveContainer, XAxis } from "recharts";
import { EmotionCount, EmotionKey } from "../types/analysisInterface";

type Props = {
  emotionCount: EmotionCount;
};

const barColors = [
  "#C64E48", // Anger
  "#289559", // Disgust
  "#6B5EA6", // Fear
  "#EAD94C", // Joy
  "#F2F2F2", // Neutral
  "#5F5F5F", // Sadness
  "#35A7FF", // Surprise
];

const formatData = (emotionCount: EmotionCount) => {
  const data = Object.keys(emotionCount).map((key: string) => {
    const entry = { emotion: key, count: emotionCount[key as EmotionKey] };
    return entry;
  });
  return data;
};

function AnalysisHistogram({ emotionCount }: Props) {
  return (
    <ResponsiveContainer width={"80%"} height={200} minWidth={200}>
      <BarChart margin={{ top: 30 }} data={formatData(emotionCount)}>
        <XAxis dataKey="emotion" fontSize={12} stroke="white" />
        <Bar
          dataKey="count"
          fill="#FFF"
          label={{ fill: "white", fontSize: 12, position: "top" }}
          minPointSize={20}
        >
          {formatData(emotionCount).map((entry, index) => (
            <Cell fill={barColors[index]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export default AnalysisHistogram;
