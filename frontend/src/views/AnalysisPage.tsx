import React from "react";
import AnalysisHeader from "../components/AnalysisHeader";

import "./AnalysisPage.css";

import dummyData from "../dummyData.json";
const analysisResults = dummyData.result.result;

function AnalysisPage() {
  return (
    <div className="analysis-container">
      <AnalysisHeader emotionCount={analysisResults.emotion_count} />
    </div>
  );
}

export default AnalysisPage;
