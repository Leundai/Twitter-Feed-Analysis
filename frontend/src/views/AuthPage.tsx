import React, { useEffect } from "react";
import "./AuthPage.css";

import { useNavigate } from "react-router-dom";
import { Typography, Button } from "@mui/material";
import TwitterIcon from "@mui/icons-material/Twitter";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { useLocalStorage } from "hooks/useLocalStorage";

function AuthPage() {
  const navigate = useNavigate();
  const [analysis, setAnalysis] = useLocalStorage("analysis", undefined);

  const login = () => {
    window.open("http://127.0.0.1:5000/api/auth/login", "_self");
  };

  useEffect(() => {
    if (analysis) {
      navigate("/analysis");
    }
    // eslint-disable-next-line
  }, []);

  return (
    <div className="auth-container">
      <header className="auth-header">
        <Typography variant="h3" marginBottom=".5em" color="white">
          Understand your Twitter feed's emotions
        </Typography>
        <Button
          size="large"
          variant="outlined"
          color="info"
          startIcon={<TwitterIcon />}
          onClick={() => login()}
        >
          Login with twitter
        </Button>
      </header>
      <div className="about-button">
        <Button
          size="medium"
          color="info"
          endIcon={<ArrowForwardIcon />}
          onClick={() => navigate("/about")}
        >
          How it works
        </Button>
      </div>
    </div>
  );
}

export default AuthPage;
