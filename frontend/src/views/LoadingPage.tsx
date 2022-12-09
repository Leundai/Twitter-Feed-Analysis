import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Typography } from "@mui/material";

import "./LoadingPage.css";
import CircularProgressWithLabel from "../components/CircularProgressWithLabel";

function LoadingPage() {
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    if (progress >= 100) {
      navigate("/analysis");
    }
    // Ignoring navigate as deps
    // eslint-disable-next-line
  }, [progress]);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress((prevProgress) =>
        prevProgress >= 100 ? 100 : prevProgress + 20
      );
    }, 400);

    return () => {
      clearInterval(timer);
    };
    // Ignoring progress and navigate as deps
    // eslint-disable-next-line
  }, []);

  return (
    <div className="loading-container">
      <Typography variant="h4" color="white" marginBottom=".5em">
        Analyzing your Twitter feed
      </Typography>
      <CircularProgressWithLabel
        variant="determinate"
        value={progress}
        color="info"
        size="4em"
      />
    </div>
  );
}

export default LoadingPage;
