import React from 'react';
import Base from './operator/Base';
import Login from './operator/Login';

const App: React.FC = () => (
  <Base content={<Login />} pages={['Login']} />
);

export default App;
