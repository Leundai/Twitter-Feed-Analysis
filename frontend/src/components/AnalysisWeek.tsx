import { Typography } from "@mui/material";
import React from "react";
import {
  Bar,
  BarChart,
  Legend,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts";
import { WeekResults } from "../types/analysisInterface";

type Props = {
  weekResults: WeekResults[];
};

const EMOTIONS = [
  "anger",
  "disgust",
  "joy",
  "sadness",
  "neutral",
  "fear",
  "surprise",
];

const barColors = [
  "#C64E48", // Anger
  "#289559", // Disgust
  "#EAD94C", // Joy
  "#5F5F5F", // Sadness
  "#F2F2F2", // Neutral
  "#6B5EA6", // Fear
  "#35A7FF", // Surprise
];

function AnalysisWeek({ weekResults }: Props) {
  return (
    <>
      <Typography variant="h4" color="white" marginBottom="1em">
        Emotion over the past 7 days
      </Typography>
      <ResponsiveContainer width={"70%"} height={240} minWidth={370}>
        <BarChart
          width={500}
          height={300}
          data={weekResults}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <Legend />
          <XAxis dataKey="date" reversed />
          <YAxis />
          {EMOTIONS.map((emotion, index) => (
            <Bar dataKey={emotion} fill={barColors[index]} minPointSize={3} />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </>
  );
}

export default AnalysisWeek;
