import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

export const StockResult: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { state } = useLocation();
  const [stockSymbol, setStockSymbol] = useState('');
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

      <div className="form">
        <form onSubmit={handleFormSubmit}>
          <div className="form-group">
            <label htmlFor="stock_symbol">Select Stock Symbol:</label>
            <input
              type="text"
              id="stock_symbol"
              name="stock_symbol"
              list="stock_symbols"
              value={stockSymbol}
              onChange={(e) => setStockSymbol(e.target.value)}
              required
            />
            <datalist id="stock_symbols">
            </datalist>
          </div>

          <div className="form-group">
            <button type="submit">Predict</button>
            {state.stock_symbol}
          </div>
        </form>
      </div>

      <div className="chart">
        {state.result_html && (
          <>
            <h2>Prediction Result</h2>
            <div dangerouslySetInnerHTML={{ __html: state.result_html }} />
          </>
        )}
      </div>

      <div className="response">
        {state.mse && (
          <p>
            Thank you for trying AI Stock Prediction. <br />
            This AI produced a Mean Squared Error (MSE) of: {state.mse}.<br />
            This value represents the average squared difference between the predicted and actual values.
          </p>
        )}
      </div>

      <div className="graph">
        {state.plot_div && (
          <>
            <h2>Actual vs Predicted ({state.plot_div})</h2>
            <div dangerouslySetInnerHTML={{ __html: state.plot_div }} />
          </>
        )}
      </div>

      <script src="../static/recommendation.js"></script>
    </div>
  );
};