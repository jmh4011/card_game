import { useRef } from 'react';
import { gsap } from 'gsap';

export const useAnimationEffect = () => {
  const elementRef = useRef<HTMLElement | null>(null);

  // 카드 이동 효과
  const playMoveAnimation = (element: HTMLElement) => {
    gsap.fromTo(
      element,
      { x: -100, opacity: 0 },
      { x: 0, opacity: 1, duration: 1, ease: 'power3.out' }
    );
  };

  // 공격 애니메이션
  const playAttackAnimation = (element: HTMLElement) => {
    gsap.fromTo(
      element,
      { scale: 1 },
      { scale: 1.2, duration: 0.2, repeat: 3, yoyo: true }
    );
  };

  // 카드 파괴 애니메이션
  const playDestroyAnimation = (element: HTMLElement) => {
    gsap.to(element, {
      opacity: 0,
      scale: 0,
      duration: 1,
      ease: 'power3.out',
    });
  };

  // 발광 애니메이션 (ex: 효과 적용 시)
  const playGlowAnimation = (element: HTMLElement) => {
    gsap.to(element, {
      boxShadow: '0 0 20px 10px rgba(255,255,255,0.8)',
      duration: 0.5,
      yoyo: true,
      repeat: 1,
    });
  };

  // 카드에 애니메이션을 적용할 수 있도록 elementRef 반환
  return {
    elementRef,
    playMoveAnimation,
    playAttackAnimation,
    playDestroyAnimation,
    playGlowAnimation,
  };
};
