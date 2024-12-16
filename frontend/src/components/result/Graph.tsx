import React from 'react';

type Props = {
    state: any;
}
export const Graph: React.FC<Props> = ({ state }) => {
  return (
    <div className="graph">
        {state.plot_div && (
        <>
            <h2>Actual vs Predicted ({state.stock_symbol})</h2>
            <div dangerouslySetInnerHTML={{ __html: state.plot_div }} />
        </>
        )}
    </div>
    );
};