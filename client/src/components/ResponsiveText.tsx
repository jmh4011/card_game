import React, { useRef, useEffect, useState, ReactNode } from "react";
import styled from "styled-components";

interface ResponsiveTextProps {
  children: ReactNode;
}

const ResponsiveText: React.FC<ResponsiveTextProps> = ({ children }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [fontSize, setFontSize] = useState<number>(100);

  const updateFontSize = () => {
    if (!containerRef.current) return;

    const parentElement = containerRef.current.parentElement;
    if (parentElement) {
      const parentWidth = parentElement.clientWidth;
      const parentHeight = parentElement.clientHeight;

      // 텍스트 길이 (글자 수)
      const textLength = typeof children === 'string' ? children.length : React.Children.count(children);

      // 부모 요소의 크기와 텍스트 길이를 고려한 폰트 크기 계산
      const widthFactor = 0.9; // Width factor to fit text within width
      const heightFactor = 0.8; // Height factor to fit text within height
      
      
      // 부모 요소의 너비와 텍스트 길이에 따라 폰트 크기 조정
      const calculatedFontSizeByWidth = (parentWidth / textLength) * widthFactor;
      const calculatedFontSizeByHeight = parentHeight * heightFactor;
      
      // 최종 폰트 크기: 둘 중 더 작은 값을 사용
      const newFontSize = Math.min(calculatedFontSizeByWidth, calculatedFontSizeByHeight);

      setFontSize(newFontSize);
    }
  };

  useEffect(() => {
    updateFontSize();
    window.addEventListener("resize", updateFontSize);
    return () => {
      window.removeEventListener("resize", updateFontSize);
    };
  }, [children]);

  

  return (
    <Container ref={containerRef} fontSize={fontSize}>
      {children}
    </Container>
  );
};

export default ResponsiveText;

const Container = styled.div<{ fontSize: number }>`
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  white-space: nowrap;
  padding: 0 5px;
  font-size: ${({fontSize}) => `${fontSize}`}px;
`;

