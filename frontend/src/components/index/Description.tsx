import React from 'react';

export const Description: React.FC = ({  }) => {
  return (
    <div className="response">
        <p>
            This web application fetches historical S&P 500 Index data, preprocesses it, 
            and employs scikit-learn's linear regression to predict future stock prices. 
            The model learns from historical data, establishing patterns between opening, 
            high, and low prices to predict closing prices. Results are visualized with Plotly, 
            providing an interactive display of actual versus predicted values.
        </p>
    </div>
  );
};