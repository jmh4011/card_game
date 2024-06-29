from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import Base

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
    player_cards = relationship("PlayerCard", back_populates="card")

class DeckCard(Base):
    __tablename__ = "deckcards"
    deck_card_id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("decks.deck_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    deck = relationship("Deck", back_populates="cards")
    card = relationship("Card", back_populates="decks")

class Deck(Base):
    __tablename__ = "decks"
    deck_id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    deck_name = Column(String(100), nullable=True)
    image = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    player = relationship("Player", back_populates="decks")
    cards = relationship("DeckCard", back_populates="deck")
    stats = relationship("PlayerStats", back_populates="deck")

class GameMove(Base):
    __tablename__ = "gamemoves"
    move_id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.game_id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    move_description = Column(Text, nullable=True)
    move_timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    game = relationship("Game", back_populates="moves")
    player = relationship("Player")

class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("players.player_id"), nullable=True)
    played_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    moves = relationship("GameMove", back_populates="game")
    player1 = relationship("Player", foreign_keys=[player1_id])
    player2 = relationship("Player", foreign_keys=[player2_id])
    winner = relationship("Player", foreign_keys=[winner_id])

class Player(Base):
    __tablename__ = "players"
    player_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    decks = relationship("Deck", back_populates="player")
    stats = relationship("PlayerStats", back_populates="player")
    player_cards = relationship("PlayerCard", back_populates="player")

class PlayerStats(Base):
    __tablename__ = "playerstats"
    stat_id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    current_deck_id = Column(Integer, ForeignKey("decks.deck_id"), nullable=True)
    money = Column(Integer, nullable=False)
    last_updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    player = relationship("Player", back_populates="stats")
    deck = relationship("Deck", back_populates="stats")

class PlayerCard(Base):
    __tablename__ = "playercards"
    player_card_id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.card_id"), nullable=False)
    card_count = Column(Integer, nullable=False,default=1)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=True)
    player = relationship("Player", back_populates="player_cards")
    card = relationship("Card", back_populates="player_cards")
