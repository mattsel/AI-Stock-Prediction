import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const StockForm: React.FC = () => {
  const [stockSymbol, setStockSymbol] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleFormSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      try {
        const response = await fetch('http://localhost:5000/api/result', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ stock_symbol: stockSymbol }),
        });
  
        if (response.ok) {
          const data = await response.json();
          navigate(`/result/${stockSymbol}`, { state: data });
        } else {
          alert('Failed to fetch stock data');
        }
      } catch (error) {
        console.error(error);
        alert('Error occurred. Please try again later.');
      }
  };
  

  return (
    <div>
      <div className="navbar">
        <a href="/">
          <h1>AI Stock Predictions</h1>
        </a>
        <a href="https://github.com/mattsel/AI-Stock-Prediction">
          <p>Repository</p>
        </a>
      </div>

      <div className="response">
        <p>
          This web application fetches historical S&P 500 Index data, preprocesses it, 
          and employs scikit-learn's linear regression to predict future stock prices. 
          The model learns from historical data, establishing patterns between opening, 
          high, and low prices to predict closing prices. Results are visualized with Plotly, 
          providing an interactive display of actual versus predicted values.
        </p>
      </div>

      <div className="form">
        <form onSubmit={handleFormSubmit}>
          <div className="form-group">
            <label htmlFor="stock_symbol">Enter Ticker Symbol:</label>
            <input
              type="text"
              id="stock_symbol"
              name="stock_symbol"
              value={stockSymbol}
              onChange={(e) => setStockSymbol(e.target.value)}
              list="stock_symbols"
              required
            />
            <datalist id="stock_symbols">
            </datalist>
          </div>

          <div className="form-group">
            <button type="submit">Predict</button>
          </div>
        </form>
      </div>

      {errorMessage && (
        <div className="alert" role="alert">
          {errorMessage}
        </div>
      )}
      <script src="../static/recommendation.js"></script>
    </div>
  );
};