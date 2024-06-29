import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import { card } from "../../utils/inter";
import Card from "../Card"; // Card 컴포넌트 임포트

interface HandProps {
  cards: card[];
  scale: number; // 카드의 크기를 조절하기 위한 스케일
}

const MyHand: React.FC<HandProps> = ({ cards, scale }) => {
  const len = cards.length;

  const setRotate = (index: number) => {
    return len < 3 ? 0 : (index - (len / 2)) * 1;
  };

  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);
  const handContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handContainer = handContainerRef.current;

    if (!handContainer) return;

    let isDown = false;
    let startX: number;
    let scrollLeft: number;

    const onMouseDown = (e: MouseEvent) => {
      isDown = true;
      handContainer.classList.add('active');
      startX = e.pageX - handContainer.offsetLeft;
      scrollLeft = handContainer.scrollLeft;
    };

    const onMouseLeave = () => {
      isDown = false;
      handContainer.classList.remove('active');
    };

    const onMouseUp = () => {
      isDown = false;
      handContainer.classList.remove('active');
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - handContainer.offsetLeft;
      const walk = (x - startX) * 2; // 스크롤 속도 조절
      handContainer.scrollLeft = scrollLeft - walk;
    };

    handContainer.addEventListener('mousedown', onMouseDown);
    handContainer.addEventListener('mouseleave', onMouseLeave);
    handContainer.addEventListener('mouseup', onMouseUp);
    handContainer.addEventListener('mousemove', onMouseMove);

    return () => {
      handContainer.removeEventListener('mousedown', onMouseDown);
      handContainer.removeEventListener('mouseleave', onMouseLeave);
      handContainer.removeEventListener('mouseup', onMouseUp);
      handContainer.removeEventListener('mousemove', onMouseMove);
    };
  }, []);

  return (
    <HandContainer ref={handContainerRef}>
      {cards.map((card, index) => (
        <HandCard
          key={index}
          rotate={setRotate(index)}
          scale={hoveredIndex === index ? scale * 1.2 : scale} // 커지는 효과 적용
          onMouseEnter={() => setHoveredIndex(index)}
          onMouseLeave={() => setHoveredIndex(null)}
        >
          <Card card={card} scale={hoveredIndex === index ? scale * 1.2 : scale} />
        </HandCard>
      ))}
    </HandContainer>
  );
};

export default MyHand;

const HandContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-x: auto; // 수평 스크롤을 가능하게 함
  overflow-y: hidden; // 수직 스크롤을 숨김
  background-color: #f5f5f5; // 패의 배경색
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); // 패의 그림자 효과
  cursor: grab;

  &.active {
    cursor: grabbing;
  }
`;

const HandCard = styled.div<{ rotate: number; scale: number }>`
  width: ${({ scale }) => 630 * scale}px;
  height: ${({ scale }) => 830 * scale}px;
  transform: rotate(${({ rotate }) => rotate}deg);
  transition: transform 0.3s; // 부드러운 애니메이션 효과
  &:hover {
    z-index: 1; // 마우스를 올렸을 때 카드가 다른 카드들보다 위에 표시되도록 함
  }
`;
