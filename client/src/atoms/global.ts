import React from "react";
import { atom } from "recoil";
import { Card, CardCount, Deck, DeckSelection, UserStat } from "../utils/types";

export const modalState = atom<{ id: string; element: React.FC }[]>({
  key: "modalState",
  default: [],
});

export const isAuthenticatedState = atom<boolean | null>({
  key: "isAuthenticated",
  default: null,
});

export const loadingState = atom<boolean>({
  key: "loading",
  default: false,
});

export const userStats = atom<UserStat>({
  key: "user",
  default: { stat_id: 0, user_id: 0, nickname: "", money: 0 },
});

export const cardsStats = atom<Record<number, Card>>({
  key: "cards",
  default: {},
});

export const userCardsStats = atom<CardCount>({
  key: "userCrads",
  default: {},
});

export const deckSelectionState = atom<DeckSelection>({
  key: "deckSelection",
  default: {},
});

export const wsTokenState = atom<string>({
  key: "wsToekn",
  default: "1",
});
