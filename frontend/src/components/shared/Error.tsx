import React, { useEffect } from 'react';
import { toast, ToastContainer } from 'react-toastify';

type Props = {
  errorMessage: string;
};

export const Error: React.FC<Props> = ({ errorMessage }) => {
  useEffect(() => {
    if (errorMessage) {
      toast.error(errorMessage, {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
      });
    }
  }, [errorMessage]);

  return (
    <div>
      <ToastContainer />
    </div>
  );
};
