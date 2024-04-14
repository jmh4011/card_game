import { useCallback, useEffect, useId, useState } from "react";
import { atom, useRecoilState } from "recoil";


export const modalState = atom<{ id: string; element: React.FC }[]>({
  key: 'modalState',
  default: [],
});

const isArrEmpty = (arr: unknown[]) => arr.length === 0;

const useModal = (component: React.FC) => {
  const [modalElements, setModal] = useRecoilState(modalState);
  // 전역 상태에 element 자체를 상태로 저장한다.
  const id = useId() + `-${new Date().getTime()}`;
  // 컴포넌트에 id를 부여해서 식별한다.
  const [isOpen, setIsOpen] = useState(false);
  // 해당 컴포넌트가 열렸는지 안열렸는지 알려주는 상태

  const openModal = useCallback(() => {
    setModal((pre) => [...pre, { id: id, element: component }]);
    // modal을 전역상태에 추가한다
    document.body.style.overflow = 'hidden';
    // modal이 open되면 배경의 스크롤을 막아야함
  }, [component, id, setModal]);

  const closeModal = useCallback(() => {
    setModal((pre) => pre.filter((c) => c.id !== id));
    // modal을 전역상태에서 제거한다.

    if (isArrEmpty(modalElements)) document.body.style.overflow = 'unset';
    // modal이 모두 꺼지면 배경의 스크롤이 가능해야함
  }, [id, modalElements, setModal]);


  return { isOpen, openModal, closeModal };
};

export default useModal;