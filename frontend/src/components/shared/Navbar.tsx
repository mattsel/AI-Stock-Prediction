import React from 'react';

export const Navbar: React.FC = () => {

  return (
    <div className="navbar">
        <a href="/">
          <h1>AI Stock Predictions</h1>
        </a>
        <a href="https://github.com/mattsel/AI-Stock-Prediction">
          <p>Repository</p>
        </a>
      </div>
  );
};