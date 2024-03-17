import React from 'react';
import { createRoot } from 'react-dom/client';

const App = () => {
  return <div>Hello, React!</div>;
};

const root = createRoot(document.getElementById('root'));
root.render(<App />);
