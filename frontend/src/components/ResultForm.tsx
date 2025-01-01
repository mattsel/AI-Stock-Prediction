import React from 'react';
import { useLocation } from 'react-router-dom';
import { Navbar } from './shared/Navbar';
import { Form } from './shared/Form';
import { Chart } from './result/Chart';
import { Description } from './result/Description';
import { Graph } from './result/Graph';

export const StockResult: React.FC = () => {
  const { state } = useLocation();

  return (
    <div>
      <Navbar/>
      <Form/>
      <Chart state={state}/>
      <Description state={state}/>
      <Graph state={state}/>
    </div>
  );
};