import React from 'react';
import { Breadcrumb, Layout, Menu, theme } from 'antd';
import './css/Base.css'

const { Header, Content, Footer } = Layout;

const items = new Array(15).fill(null).map((_, index) => ({
  key: index + 1,
  label: `nav ${index + 1}`,
}));

type BaseProps = {
  content: React.ReactNode;
  pages: Array<String>;
};

const Base: React.FC<BaseProps> = (props) => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <Layout className='layout-base'>
      <Header className='header-base'>
        <div className="demo-logo" />
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={['2']}
          items={items}
          style={{ flex: 1, minWidth: 0 }}
        />
      </Header>
      <Content className='content-base'>
        <Breadcrumb className='content-breadcrumb-base'>
          { props.pages.map((page, index) => (
            <Breadcrumb.Item key={index}>
              {page}
            </Breadcrumb.Item>
          )) }
        </Breadcrumb>
        <div
          style={{
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
          className='content-div1-base'
        >
          { props.content }
        </div>
      </Content>
      <Footer className='footer-base'>
        Ant Design ©2024 Created by Gabriel Nunes
      </Footer>
    </Layout>
  );
};

export default Base;
