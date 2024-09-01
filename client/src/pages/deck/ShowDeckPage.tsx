import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import useHttpDeck from "../../api/decks";
import { useSetRecoilState } from "recoil";
import ConfigDeckPage from "./ConfigDeckPage";
import ReadOnlyDeckPage from "./ReadOnlyDeckPage";
import { CardCount, Deck } from "../../utils/types";
import Navbar from "../../components/Navbar";

const ShowDeckPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { getDeck } = useHttpDeck();
  const [showType, setShowType] = useState(0);
  const [loading, setLoading] = useState(true);

  const [showDeck, setShowDeck] = useState<Deck>({
    deck_id: 0,
    deck_name: "null",
    image_path: "0.png",
    user_id: 0,
    is_public: false,
  });
  const [deckCards, setDeckCards] = useState<CardCount>({});

  useEffect(() => {
    getDeck(
      Number(id),
      (data: any) => {
        console.log(id , data)
        setShowType(data.read_only ? 1 : 0);
        setShowDeck(data.deck);
        setDeckCards(data.deck_cards);
      },
      () => {
        setShowType(2);
      },
      setLoading
    );
  }, [id]);

  return (
    <>
      {loading ? (
        <div> loading...</div>
      ) : (
        <>
          {showType === 0 && (
            <ConfigDeckPage
              deck={showDeck}
              deckCards={deckCards}
              setDeck={setShowDeck}
              setDeckCards={setDeckCards}
            />
          )}
          {showType === 1 && (
            <ReadOnlyDeckPage deck={showDeck} deckCards={deckCards} />
          )}
          {showType === 2 && (
            <div>
              <Navbar to={-1} name=""></Navbar>
              권한 없음
            </div>
          )}
        </>
      )}
    </>
  );
};

export default ShowDeckPage;
