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
  width: 100%;
  height: 6vh;
  background-color: rgb(100, 100, 100);
  color: rgb(255,255,255);
`;

const Icon = styled(IoMdArrowBack)`
  display: inline-block;
  width: 5vh;
  height: 5vh;
`

const Name = styled.div`
  display: inline-block;
  font-size: 4vh;
`
