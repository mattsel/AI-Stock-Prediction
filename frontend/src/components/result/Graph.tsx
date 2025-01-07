import React, { useEffect, useRef } from 'react';
import Plotly from 'plotly.js';

type Props = {
  state: any;
};

export const Graph: React.FC<Props> = ({ state }) => {
  const plotContainerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (plotContainerRef.current && state.dates && state.actual && state.predicted) {
      const traceActual = {
        x: state.dates,
        y: state.actual,
        mode: 'lines',
        name: 'Actual',
        line: { color: 'blue' },
      };

      const tracePredicted = {
        x: state.dates,
        y: state.predicted,
        mode: 'lines',
        name: 'Predicted',
        line: { color: 'red' },
      };

      const data = [traceActual, tracePredicted];
      const layout = {
        title: 'Stock Price Prediction',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Stock Price' },
      };

      Plotly.newPlot(plotContainerRef.current, data, layout);
    }
  }, [state]);

  return (
    <div className="graph">
      {state.dates && state.actual && state.predicted ? (
        <div ref={plotContainerRef} />
      ) : (
        <p>Loading plot...</p>
      )}
    </div>
  );
};
