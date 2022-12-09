import React from "react";
import "./authPage.css";

import { Link } from "react-router-dom";
import { Typography, Button } from "@mui/material";
import TwitterIcon from "@mui/icons-material/Twitter";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

function AuthPage() {
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
        >
          Login with twitter
        </Button>
      </header>
      <div className="about-button">
        <Button size="medium" color="info" endIcon={<ArrowForwardIcon />}>
          <Link to="/about">How it works</Link>
        </Button>
      </div>
    </div>
  );
}

export default AuthPage;
