import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from '@fluentui/react-components';
import { Error } from './Error';

export const Form: React.FC = () => {
  const [stockName, setStockName] = useState('');
  const [stockNamesList, setStockNamesList] = useState<string[]>([]);
  const [filteredNames, setFilteredNames] = useState<string[]>([]);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const apiHost = process.env.FLASK_BACKEND_URL || 'http://localhost:5000';

  useEffect(() => {
    axios.get(`${apiHost}/api/stocks/all`)
      .then((response) => {
        setStockNamesList(response.data);
        setFilteredNames(response.data.slice(0, 4));
      })
      .catch((error) => {
        setErrorMessage('Failed to load stock names. Please try again.');
      });
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      setStockName(stockName);
    }, 300);

    return () => clearTimeout(timer);
  }, [stockName]);

  useEffect(() => {
    if (stockName) {
      const filteredData = stockNamesList.filter(item =>
        item.toLowerCase().includes(stockName.toLowerCase())
      );
      setFilteredNames(filteredData.slice(0, 4));
    } else {
      setFilteredNames(stockNamesList.slice(0, 4));
    }
  }, [stockName, stockNamesList]);

  const handleSearchInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    setStockName(e.target.value);
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage('');

    if (!stockName.trim()) {
      setErrorMessage('Stock name cannot be empty.');
      return;
    }

    try {
      const response = await fetch(`${apiHost}/api/result`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stock_symbol: stockName }),
      });

      if (response.ok) {
        const data = await response.json();
        navigate(`/result/${stockName}`, { state: data });
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
          <label htmlFor="stock_name">Enter Stock Name:</label>
          
          <input
            type="text"
            id="stock_name"
            name="stock_name"
            value={stockName}
            onChange={handleSearchInput}
            list="stock-suggestions"
            required
          />
          
          <datalist id="stock-suggestions">
            {filteredNames.map((name, index) => (
              <option key={index} value={name} />
            ))}
          </datalist>
        </div>

        <div className="form-group" id="submit-button">
          <Button
            appearance="subtle"
            size="small"
            className="submitButton"
            type="submit"
          >
            Calculate
          </Button>
        </div>
      </form>
      <Error errorMessage={errorMessage} />
    </div>
  );
};
