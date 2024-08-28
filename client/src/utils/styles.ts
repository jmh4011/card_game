import styled, { keyframes } from "styled-components";

export const OutModal = styled.div`
  z-index: 10;
  display: block;
  background: rgba(0, 0, 0, 0.3);
  position: fixed;
  width: 100vw;
  height: 100vh;
`;

export const Vibration = keyframes`
  0% { transform: translateX(0); }
  25% { transform: translateX(5px); }
  75% { transform: translateX(-5px); }
  100% { transform: translateX(0); }
`;
