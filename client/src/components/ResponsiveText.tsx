import React, { useRef, useEffect, useState, ReactNode } from "react";
import styled from "styled-components";

// Container 스타일 컴포넌트 정의, fontSize를 props로 받아서 설정
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
  const [fontSize, setFontSize] = useState<number>(100); // 초기 폰트 크기를 100으로 설정

  const updateFontSize = () => {
    if (!containerRef.current) return;

    const parentElement = containerRef.current.parentElement;
    if (parentElement) {
      const parentWidth = parentElement.clientWidth;
      const parentHeight = parentElement.clientHeight;

      // 폰트 크기 최적화
      let newFontSize = 100;
      let fits = false;

      while (!fits) {
        // 가상 텍스트 요소 생성
        const testElement = document.createElement("span");
        testElement.style.fontSize = `${newFontSize}px`;
        testElement.style.visibility = "hidden";
        testElement.style.whiteSpace = "nowrap";
        testElement.innerText = children as string;
        document.body.appendChild(testElement);

        const textWidth = testElement.offsetWidth;
        const textHeight = testElement.offsetHeight;

        document.body.removeChild(testElement);

        // 텍스트 크기가 부모 요소보다 작거나 같을 때까지 폰트 크기 조정
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
  }, [children]); // children이 변경될 때마다 폰트 크기 재계산

  return (
    <Container ref={containerRef} fontSize={fontSize}>
      {children}
    </Container>
  );
};

export default ResponsiveText;
