import React from "react";
import { atom } from "recoil";
import { DeckSelection, UserCards, UserStat } from "../types/routers";
import { Card, Effect } from "../types/models";

export const isAuthenticatedState = atom<boolean>({
  key: "isAuthenticated",
  default: false,
});

export const loadingState = atom<boolean>({
  key: "loading",
  default: false,
});

export const userStats = atom<UserStat>({
  key: "user",
  default: { stat_id: 0, user_id: 0, nickname: "", money: 0, current_mod_id: 1 },
});

export const cardsStats = atom<Record<number, Card>>({
  key: "cards",
  default: {},
});

export const effectsStats = atom<Record<number, Effect>>({
  key: "effects",
  default: {},
});

export const userCardsStats = atom<UserCards>({
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
