import React, { useRef, useEffect, useState, ReactNode } from "react";
import styled from "styled-components";


const Container = styled.div<{ fontSize: number }>`
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden; /* 텍스트가 넘칠 경우 숨김 */
  white-space: nowrap; /* 텍스트 줄 바꿈 방지 */
  font-size: ${(props) => props.fontSize}px; /* props로 받은 fontSize 적용 */
`;

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

      
      let newFontSize = 100;
      let fits = false;

      while (!fits) {
        const testElement = document.createElement("span");
        testElement.style.fontSize = `${newFontSize}px`;
        testElement.style.visibility = "hidden";
        testElement.style.whiteSpace = "nowrap";
        testElement.innerText = children as string;
        document.body.appendChild(testElement);

        const textWidth = testElement.offsetWidth;
        const textHeight = testElement.offsetHeight;

        document.body.removeChild(testElement);

        if (textWidth <= parentWidth && textHeight <= parentHeight) {
          fits = true;
        } else {
          newFontSize -= 1;
        }
      }

      setFontSize(newFontSize * 0.90);
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
