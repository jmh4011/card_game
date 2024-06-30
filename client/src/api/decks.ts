import { http } from './api';

type setFn = (data: any) => void;

export const GetDecks = (userId: number, setDecks: setFn, setLoading: setFn) => {
  http('get', `/decks/${userId}`, setDecks, setLoading);
}

export const PostDecks = (userId: number, setDeck: setFn, setLoading: setFn,
  deck_name: string = `새로운 덱`, 
  image: string = "0.png") => {
  http('post', `/decks/`, setDeck, setLoading, {
    player_id: userId,
    deck_name: deck_name,
    image: image
  });
}

export const GetDeckPlayerCards = (deck_id: number, userId: number, callback: setFn, setLoading: setFn) => {
  http('get', `/decks/cards/${deck_id}/${userId}`, callback, setLoading);
}

interface deckUpdate {
  deck_name: string;
  image: string;
  deck_cards: number[];
}

export const PutDeckUpdate = (deck_id: number, data: deckUpdate, setDeck: setFn, setDeckCards: setFn, setLoading: setFn) => {
  http('put', `/decks/${deck_id}`, (data: any) => {
    setDeck(data.deck);
    setDeckCards(data.deck_cards);
  }, setLoading, data);
}
