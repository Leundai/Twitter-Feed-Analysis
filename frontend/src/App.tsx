import React from "react";
import { Routes, Route } from "react-router-dom";
import AuthPage from "./views/AuthPage";
import AboutPage from "./views/AboutPage";
import Layout from "./views/Layout";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<AuthPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Route>
    </Routes>
  );
}

export default App;
