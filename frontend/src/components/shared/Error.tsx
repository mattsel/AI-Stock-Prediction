/* Will Be a Toast*/
import React from 'react';

type Props = {
  errorMessage: string;
};

export const Error: React.FC<Props> = ({ errorMessage }) => {
  return (
    <div className="alert alert-danger" role="alert">
      {errorMessage}
    </div>
  );
};
