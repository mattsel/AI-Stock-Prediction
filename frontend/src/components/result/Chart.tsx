import React from 'react';

type Props = {
    state: any;
}
export const Chart: React.FC<Props> = ({ state }) => {
  return (
    <div className="chart">
        {state.result_html && (
        <>
            <h2>Prediction Result</h2>
            <div dangerouslySetInnerHTML={{ __html: state.result_html }} />
        </>
        )}
    </div>
  );
};