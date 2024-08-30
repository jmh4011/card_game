import React, { useRef, useEffect, useState, ReactNode } from "react";
import styled from "styled-components";

interface ResDescriptionProps {
  children: ReactNode;
}

const ResDescription: React.FC<ResDescriptionProps> = ({ children }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [fontSize, setFontSize] = useState<number>(100);

  const updateSize = () => {
    if (!containerRef.current) return;

    const parentElement = containerRef.current.parentElement;
    if (parentElement) {
      const parentWidth = parentElement.clientWidth;
      const parentHeight = parentElement.clientHeight;

      const textLength = (children as string).length;
      const lines = (children as string).split("\n").length;
      const avgCharsPerLine = textLength / lines;

      const calculatedFontSize = Math.min(
        parentWidth / avgCharsPerLine,
        parentHeight / (lines * 1.8)
      );

      setFontSize(calculatedFontSize);
    }
  };

  useEffect(() => {
    updateSize();
    window.addEventListener("resize", updateSize);
    return () => {
      window.removeEventListener("resize", updateSize);
    };
  }, [children]);

  return (
    <Container ref={containerRef} fontSize={fontSize}>
      {children}
    </Container>
  );
};

export default ResDescription;

const Container = styled.div<{ fontSize?: number }>`
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  overflow: hidden;
  white-space: pre-wrap;
  font-size: ${(props) => `${props.fontSize}px`};
`;
