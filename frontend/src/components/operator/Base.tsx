import React from 'react';
import './css/Base.css'
import Logo from '../img/ceac.png'
import type { MenuProps } from 'antd'
import { Breadcrumb, Layout, Menu, theme, Dropdown, Space } from 'antd';

const { Header, Content, Footer } = Layout;

interface MenuItemType {
  key: number;
  label: string;
};

interface ItemType extends MenuItemType {};

interface BreadcrumbItemType {
  title: string;
}

interface Partial extends BreadcrumbItemType {}

interface BaseProps {
  content: React.ReactNode;
  link: Array<Partial>;
  menuItems: Array<ItemType>;
};

const Base: React.FC<BaseProps> = (props) => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Layout className='layout-base'>
      <Header className='header-base'>
        <img src={Logo} alt="logo" className='logo-base'/>
        <Menu className='menu-base'
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['2']}
          items={props.menuItems}
        />
      </Header>
      <Content className='content-base'>
        <Breadcrumb
          items={props.link}
        />
        <div
          style={{
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
          className='content-div1-base'
        >
          {props.content ? props.content : null}
        </div>
      </Content>
      <Footer className='footer-base'>
        ©2024 Criado por Gabriel Nunes
      </Footer>
    </Layout>
  );
};

export default Base;
