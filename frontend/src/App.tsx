import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { StockForm } from './components/StockForm';
import { StockResult } from './components/ResultForm';
export const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" Component={StockForm} />
        <Route path="/result/:stockSymbol" Component={StockResult} />
      </Routes>
    </Router>
  );
};