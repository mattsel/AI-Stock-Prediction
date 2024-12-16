import React, { useState } from 'react';
import { Navbar } from './shared/Navbar';
import { Form } from './shared/Form'
import { Description } from './index/Description';
import { Error } from './shared/Error'

export const StockForm: React.FC = () => {
  const [errorMessage, setErrorMessage] = useState('');
  return (
    <div>
      <Navbar/>
      <Description/>
      <Form setErrorMessage={setErrorMessage}/>
      {errorMessage && <Error errorMessage={errorMessage} />}
    </div>
  );
};