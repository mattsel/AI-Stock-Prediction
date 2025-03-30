import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { StockForm } from './components/StockForm';
import { StockResult } from './components/ResultForm';

export const App: React.FC = () => {
  return (
    <Router> {}
      <RoutesWrapper />
    </Router>
  );
};

const RoutesWrapper: React.FC = () => {
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/') {
      import('./styling/indexForm.css');
    } else {
      import('./styling/resultForm.css');
    }
  }, [location.pathname]);

  return (
    <Routes>
      <Route path="/" element={<StockForm />} />
      <Route path="/result/:stockSymbol" element={<StockResult />} />
    </Routes>
  );
};
