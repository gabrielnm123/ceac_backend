import React from 'react';
import Base from './operator/Base';
import Login from './operator/Login';

const link = (access: Array<string>) => {
  return (
    access.map((item) => (
      {title: item}
    ))
  )
}

const menuItems = (access: Array<string>) => {
  return (
    access.map((item, index) => (
      {key: index, label:item}
    ))
  )
}

const testArray = (cont: number) => {
  let array = []
  for (let i = 0; i <= cont; i++) {
    array.push(`test ${i}`)
  }
  return array
}


const App: React.FC = () => (
  <Base content={ <Login /> } link={ link(['Login']) } menuItems={menuItems(testArray(50))}/>
);

export default App;
