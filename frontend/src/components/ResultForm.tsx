import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Navbar } from './shared/Navbar';
import { Form } from './shared/Form';
import { Error } from './shared/Error'
import { Chart } from './result/Chart';
import { Description } from './result/Description';
import { Graph } from './result/Graph';

export const StockResult: React.FC = () => {
  const { state } = useLocation();
  const [errorMessage, setErrorMessage] = useState('');

  return (
    <div>
      <Navbar/>
      <Form setErrorMessage={setErrorMessage}/>
      <Chart state={state}/>
      <Description state={state}/>
      <Graph state={state}/>
      <Error errorMessage={errorMessage}/>
    </div>
  );
};