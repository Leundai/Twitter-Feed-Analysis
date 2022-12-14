import React from "react";
import AnalysisHeader from "../components/AnalysisHeader";
import AnalysisHistogram from "../components/AnalysisHistogram";
import AnalysisContributors from "../components/AnalysisContributors";
import AnalysisTopTweets from "../components/AnalysisTopTweets";

import "./AnalysisPage.css";

import AnalysisWeek from "../components/AnalysisWeek";
import { useLocalStorage } from "../hooks/useLocalStorage";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";

function AnalysisPage() {
  const [analysis, setAnalysis] = useLocalStorage("analysis", undefined);

  return (
    <div className="analysis-container">
      <AnalysisHeader emotionCount={analysis.emotion_count} />
      <AnalysisHistogram emotionCount={analysis.emotion_count} />
      <AnalysisContributors
        emotionsContributors={analysis.emotion_contributors}
        classifiedTweets={analysis.classified_tweets}
        emotionCount={analysis.emotion_count}
        authorsInfo={analysis.authors}
      />
      <AnalysisTopTweets topEmotionalTweets={analysis.max_emotional_tweets} />
      <AnalysisWeek weekResults={analysis.week_results} />
    </div>
  );
}

export default AnalysisPage;
