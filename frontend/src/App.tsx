import React from "react";
import { Routes, Route } from "react-router-dom";
import AuthPage from "views/AuthPage";
import AboutPage from "views/AboutPage";
import Layout from "views/Layout";
import LoadingPage from "views/LoadingPage";
import AnalysisPage from "views/AnalysisPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<AuthPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/loading/:userId" element={<LoadingPage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
      </Route>
    </Routes>
  );
}

export default App;
