import { Button } from "@mui/material";
import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { useLocalStorage } from "../hooks/useLocalStorage";

import "./Layout.css";

function Layout() {
  const [analysis, setAnalysis] = useLocalStorage("analysis", undefined);
  const navigate = useNavigate();
  return (
    <div>
      {analysis && (
        <Button
          size="large"
          color="info"
          className="logout-button"
          onClick={() => {
            setAnalysis(undefined);
            navigate("/");
          }}
        >
          Logout
        </Button>
      )}

      <Outlet />
    </div>
  );
}

export default Layout;
