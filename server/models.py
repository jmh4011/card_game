from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Card(Base):
    __tablename__ = "cards"
    card_id = Column(Integer, primary_key=True, index=True)
    card_name = Column(String(100), nullable=False)
    card_class = Column(String(50), nullable=True)
    attack = Column(Integer, nullable=True)
    health = Column(Integer, nullable=True)
    image_path = Column(String(255), nullable=True)
    card_type = Column(Integer, nullable=True)  # 카드 유형
    effects = relationship("CardEffect", back_populates="card")  # 다대다 관계 테이블

class CardEffect(Base):
    __tablename__ = "card_effects"
    card_effect_id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    effect_id = Column(Integer, ForeignKey("effects.effect_id"), nullable=False)
    card = relationship("Card", back_populates="effects")
    effect = relationship("Effect")

class Effect(Base):
    __tablename__ = "effects"
    effect_id = Column(Integer, primary_key=True, index=True)
    effect_name = Column(String(100), nullable=False)
    effect_name = Column(String(100), nullable=False)
    condition = Column(Text, nullable=True)
    cost = Column(Text, nullable=True)
    effect = Column(Text, nullable=True)

class Deck(Base):
    __tablename__ = "decks"
    deck_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    deck_name = Column(String(100), nullable=True)
    image_path = Column(String(255), nullable=True)
    is_public = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    user = relationship("User", back_populates="decks")
    cards = relationship("DeckCard", back_populates="deck")

class DeckCard(Base):
    __tablename__ = "deck_cards"
    deck_card_id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("decks.deck_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    card_count = Column(Integer, default=1, nullable=False)
    deck = relationship("Deck", back_populates="cards")
    card = relationship("Card")

class GameHistory(Base):
    __tablename__ = "game_history"
    game_id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    played_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    moves = relationship("GameHistoryMove", back_populates="game")
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    winner = relationship("User", foreign_keys=[winner_id])

class GameHistoryMove(Base):
    __tablename__ = "game_history_moves"
    move_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_history.game_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    move_description = Column(Text, nullable=True)
    move_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    game = relationship("GameHistory", back_populates="moves")
    user = relationship("User")

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    refresh_token_expiry = Column(DateTime, nullable=True)
    decks = relationship("Deck", back_populates="user")
    stats = relationship("UserStat", back_populates="user")
    user_cards = relationship("UserCard", back_populates="user")
    user_deck_selections = relationship("UserDeckSelection", back_populates="user")

class UserStat(Base):
    __tablename__ = "user_stats"
    stat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    nickname = Column(String(100), nullable=False)
    money = Column(Integer, nullable=False)
    current_mod_id = Column(Integer, default=1, nullable=False)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="stats")

class UserCard(Base):
    __tablename__ = "user_cards"
    user_card_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    card_count = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    user = relationship("User", back_populates="user_cards")
    card = relationship("Card")

class UserDeckSelection(Base):
    __tablename__ = "user_deck_selections"
    selection_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    mod_id = Column(Integer, nullable=False)
    deck_id = Column(Integer, ForeignKey("decks.deck_id"), nullable=False)
    selection_date = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user = relationship("User", back_populates="user_deck_selections")
    deck = relationship("Deck")

class GameMod(Base):
    __tablename__ = 'game_mods'
    mod_id = Column(Integer, primary_key=True, index=True)
    mod_name = Column(String(50), nullable=False)
    is_open = Column(Boolean, default=False, nullable=False)
    image_path = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
