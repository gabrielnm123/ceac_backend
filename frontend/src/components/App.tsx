import React from 'react';
import Base from './operator/Base';
import { Login, breadcrumbItemLogin } from './operator/Login';

const App: React.FC = () => (
  <Base content={ <Login /> } breadcrumbItem={ breadcrumbItemLogin } />
);

export default App;
