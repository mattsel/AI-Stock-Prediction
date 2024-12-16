import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface FormProps {
  setErrorMessage: React.Dispatch<React.SetStateAction<string>>;
}

export const Form: React.FC<FormProps> = ({ setErrorMessage }) => {
  const [stockSymbol, setStockSymbol] = useState('');
  const navigate = useNavigate();

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');

    if (!stockSymbol.trim()) {
      setErrorMessage('Stock symbol cannot be empty.');
      return;
    }

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
        setErrorMessage('Failed to fetch stock data. Please try again.');
      }
    } catch (error) {
      console.error(error);
      setErrorMessage('Error occurred. Please try again later.');
    }
  };

  return (
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
  );
};
