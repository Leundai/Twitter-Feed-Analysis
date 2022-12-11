import React from "react";
import { TwitterTweetEmbed } from "react-twitter-embed";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import { EmotionContributors } from "../types/analysisInterface";

import "./AnalysisContributors.css";

type Props = {
  emotionContributors: EmotionContributors;
};

const tweetOptions = {
  theme: "dark",
  hide_media: true,
  conversation: "none",
  cards: "hidden",
  width: 550,
};

const data01 = [
  {
    name: "Angry",
    value: 400,
  },
  {
    name: "Other",
    value: 300,
  },
];

const colors = ["#29B6F6", "#29B6F6"];

function AnalysisContributors({ emotionContributors }: Props) {
  return (
    <div className="contributor-container">
      <div className="contributor-card">
        <div className="tweet-card">
          <TwitterTweetEmbed
            tweetId="1600932268461391872"
            options={tweetOptions}
          />
        </div>
        <ResponsiveContainer width="40%" height={300} minWidth={300}>
          <PieChart>
            <Pie
              data={data01}
              nameKey="name"
              dataKey="value"
              cx="50%"
              cy="50%"
              innerRadius={50}
              outerRadius={80}
              paddingAngle={5}
              label
            >
              {data01.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={index === 0 ? "#29B6F6" : "white"}
                />
              ))}
            </Pie>
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="contributor-card">
        <div className="tweet-card">
          <TwitterTweetEmbed
            tweetId="1600914754460995584"
            options={tweetOptions}
          />
        </div>
        <ResponsiveContainer width="40%" height={300} minWidth={300}>
          <PieChart>
            <Pie
              data={data01}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              fill="#82ca9d"
              label
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="contributor-card">
        <div className="tweet-card">
          <TwitterTweetEmbed
            tweetId="1600917097927811072"
            options={tweetOptions}
          />
        </div>
        <ResponsiveContainer width="40%" height={300} minWidth={300}>
          <PieChart>
            <Pie
              data={data01}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              fill="#82ca9d"
              label
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default AnalysisContributors;
