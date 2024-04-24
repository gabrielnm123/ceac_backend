import React from "react";
import { ConfigProvider } from 'antd';
import ptBR from 'antd/lib/locale/pt_BR';
import Login from './operator/Login'

function App() {
  return (
    <ConfigProvider locale={ptBR}>
      <Login />
    </ConfigProvider>
  )
}

export default App;
