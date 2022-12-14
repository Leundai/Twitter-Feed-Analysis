import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { CircularProgress, Typography } from "@mui/material";

import "./LoadingPage.css";
import CircularProgressWithLabel from "../components/CircularProgressWithLabel";
import { useLocalStorage } from "../hooks/useLocalStorage";

function LoadingPage() {
  const [analysis, setAnalysis] = useLocalStorage("analysis", undefined);
  const [progress, setProgress] = useState(0);
  const [taskId, setTaskId] = useState("");
  const { userId } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    if (analysis) {
      navigate("/analysis");
    }

    if (progress < 100) return;

    fetch(`http://127.0.0.1:5000/api/results/${taskId}`, {
      method: "GET",
    })
      .then((response) => {
        if (response.status === 200) return response.json();
        throw new Error("failed to authenticate user");
      })
      .then((result) => {
        setAnalysis(result.result.data);
        navigate("/analysis");
      })
      .catch((error) => {
        console.error(error);
      });

    // Ignoring navigate as deps
    // eslint-disable-next-line
  }, [progress]);

  useEffect(() => {
    if (!taskId) {
      return;
    }

    const timer = setInterval(() => {
      fetch(`http://127.0.0.1:5000/api/analysis_status/${taskId}`, {
        method: "GET",
      })
        .then((response) => {
          if (response.status === 200) return response.json();
          throw new Error("failed to get task progress");
        })
        .then((result) => {
          setProgress(result.result.progress);
        })
        .catch((error) => {
          console.error(error);
        });
    }, 1000);

    return () => {
      clearInterval(timer);
    };
    // Ignoring progress and navigate as deps
    // eslint-disable-next-line
  }, [taskId]);

  useEffect(() => {
    // Begin analysis
    fetch(`http://127.0.0.1:5000/api/analyze/${userId}`, {
      method: "GET",
    })
      .then((response) => {
        if (response.status === 200) return response.json();
        throw new Error("failed to authenticate user");
      })
      .then((result) => {
        setTaskId(result.result.taskId);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div className="loading-container">
      <Typography variant="h4" color="white" marginBottom=".5em">
        Analyzing your Twitter feed
      </Typography>
      {progress === 0 ? (
        <CircularProgress color="info" size="4em" />
      ) : (
        <CircularProgressWithLabel
          variant="determinate"
          value={progress}
          color="info"
          size="4em"
        />
      )}
    </div>
  );
}

export default LoadingPage;
