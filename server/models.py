from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Card(Base):
    __tablename__ = "cards"
    card_id = Column(Integer, primary_key=True, index=True)
    card_name = Column(String(100), nullable=False)
    card_class = Column(String(50), nullable=True)
    attack = Column(Integer, nullable=True)
    health = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    image = Column(String(255), nullable=True)
    cost = Column(Integer, nullable=True)
    card_type = Column(Integer, nullable=True)
    decks = relationship("DeckCard", back_populates="card")
    user_cards = relationship("UserCard", back_populates="card")

class DeckCard(Base):
    __tablename__ = "deck_cards"
    deck_card_id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("decks.deck_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    card_count = Column(Integer, default=1, nullable=False)
    deck = relationship("Deck", back_populates="cards")
    card = relationship("Card", back_populates="decks")

class Deck(Base):
    __tablename__ = "decks"
    deck_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    deck_name = Column(String(100), nullable=True)
    image = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    user = relationship("User", back_populates="decks")
    cards = relationship("DeckCard", back_populates="deck")

class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    user2_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    played_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    moves = relationship("GameMove", back_populates="game")
    user1 = relationship("User", foreign_keys=[user1_id])
    user2 = relationship("User", foreign_keys=[user2_id])
    winner = relationship("User", foreign_keys=[winner_id])

class GameMove(Base):
    __tablename__ = "game_moves"
    move_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    move_description = Column(Text, nullable=True)
    move_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    game = relationship("Game", back_populates="moves")
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
    stats = relationship("UserStats", back_populates="user")
    user_cards = relationship("UserCard", back_populates="user")

class UserStats(Base):
    __tablename__ = "user_stats"
    stat_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    nickname= Column(String(100), nullable=False)
    money = Column(Integer, nullable=False)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="stats")
    
class UserCard(Base):
    __tablename__ = "user_cards"
    user_card_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    card_count = Column(Integer, nullable=False,default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    user = relationship("User", back_populates="user_cards")
    card = relationship("Card", back_populates="user_cards")

class UserDeckSelection(Base):
    __tablename__ = "user_deck_selections"
    selection_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    game_mode = Column(String(50), nullable=False)
    deck_id = Column(Integer, ForeignKey("decks.deck_id"), nullable=False)
    selection_date = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    user = relationship("User", back_populates="deck_selections")
    deck = relationship("Deck")