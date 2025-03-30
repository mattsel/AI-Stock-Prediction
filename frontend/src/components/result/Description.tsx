import React from 'react';

type Props = {
    state: any;
}
export const Description: React.FC<Props> = ({ state }) => {
  return (
    <div className="response">
        {state.mse && (
        <p>
            Thank you for trying AI Stock Prediction. <br />
            This AI produced a Mean Squared Error (MSE) of: {state.mse}.<br />
            This value represents the average squared difference between the predicted and actual values.
        </p>
        )}
    </div>
  );
};