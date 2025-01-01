import React, { useState } from 'react';
import { Navbar } from './shared/Navbar';
import { Form } from './shared/Form'
import { Description } from './index/Description';
import { Error } from './shared/Error'

export const StockForm: React.FC = () => {
  return (
    <div>
      <Navbar/>
      <Description/>
      <Form/>
    </div>
  );
};