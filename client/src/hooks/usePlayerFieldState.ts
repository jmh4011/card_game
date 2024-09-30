import { useRecoilState } from "recoil";
import { playerHandsState, playerFieldsState, playerGravesState, playerDecksState } from "../atoms/play";

export const usePlayerFieldState = () => {
  const [hands, setHands] = useRecoilState(playerHandsState);
  const [fields, setFields] = useRecoilState(playerFieldsState);
  const [graves, setGraves] = useRecoilState(playerGravesState);
  const [decks, setDecks] = useRecoilState(playerDecksState);

  return {
    hands, setHands,
    fields, setFields,
    graves, setGraves,
    decks, setDecks,
  };
};
