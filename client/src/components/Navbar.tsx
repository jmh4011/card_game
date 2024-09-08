import React, { ReactNode } from "react";
import styled from "styled-components";
import { IoMdArrowBack } from "react-icons/io";
import { useNavigate } from "react-router-dom";

interface NavbarPorps {
  to: string | number | (() => void);
  name: string;
  children?: ReactNode;
}

const Navbar: React.FC<NavbarPorps> = ({ to, name, children}) => {
  const navigate = useNavigate();

  return (
    <Container>
      <Icon
        onClick={() => {
          switch(typeof(to)) {
            case 'number':
              navigate(to)
              break
            case 'string':
              navigate(to)
              break
            default:
              to()
              break
          }
        }}
      />
      <Name>{name}</Name>
      {children}
    </Container>
  );
};

export default Navbar;

const Container = styled.div`
  align-items: center;
  display: flex;
  width: 100%;
  height: 6vh;
  background-color: rgb(100, 100, 100);
  color: rgb(255,255,255);
`;

const Icon = styled(IoMdArrowBack)`
  float: left;
  width: 5vh;
  height: 5vh;
`

const Name = styled.div`
  float: left;
  font-size: 4vh;
`

