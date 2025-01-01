import React from 'react';
import { Link } from '@fluentui/react';
import { Button } from '@fluentui/react-components';

export const Navbar: React.FC = () => {

  return (
    <div className="navbar" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '10px' }}>
      <a href="/">
        <h1>AI Stock Predictions</h1>
      </a>
      
      <Link href="https://github.com/mattsel/AI-Stock-Prediction" target="_blank" style={{ textDecoration: 'none' }}>
        <Button appearance="subtle" size="large" className="button">
          Repository
        </Button>
      </Link>
    </div>
  );
};