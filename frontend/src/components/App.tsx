import React from 'react';
import Base from './operator/Base';
import Login from './operator/Login';

const testArray = (cont: number) => {
  let array = []
  for (let i = 0; i <= cont; i++) {
    array.push(`test ${i}`)
  }
  return array
}

const App: React.FC = () => (
  <Base content={ <Login /> } link={ ['Login'] } menuItems={testArray(20)}/>
);

export default App;
