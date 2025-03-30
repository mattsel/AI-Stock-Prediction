import React from 'react';
import { Navbar } from './shared/Navbar';
import { Form } from './shared/Form'
import { Description } from './index/Description';

export const StockForm: React.FC = () => {
  return (
    <div>
      <Navbar/>
      <Description/>
      <Form/>
    </div>
  );
};