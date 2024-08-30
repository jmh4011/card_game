import React, { useRef, useEffect, useState, ReactNode } from "react";
import styled from "styled-components";

interface ScrollableDescriptionProps {
  children: ReactNode;
}

const ScrollableDescription: React.FC<ScrollableDescriptionProps> = ({
  children,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [fontSize, setFontSize] = useState<number>(100);

  const updateSize = () => {
    if (!containerRef.current) return;

    const parentElement = containerRef.current.parentElement;
    if (parentElement) {
      const parentWidth = parentElement.clientWidth;
      const parentHeight = parentElement.clientHeight;

      const calculatedFontSize = Math.min(
        parentWidth * 0.07,
        parentHeight * 0.5
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

export default ScrollableDescription;

const Container = styled.div<{ fontSize?: number }>`
  width: 100%;
  height: 100%;
  display: flex;
  white-space: pre-wrap;
  font-size: ${(props) => `${props.fontSize}px`};
`;
