import React from "react";
import { Routes, Route } from "react-router-dom";
import AuthPage from "./views/AuthPage";

import "./App.css";

function App() {
  return (
    <Routes>
      <Route index element={<AuthPage />} />
      <Route path="/about" element={<div></div>} />
    </Routes>
  );
}

export default App;
