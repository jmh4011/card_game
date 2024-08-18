from sqlalchemy.ext.asyncio import AsyncSession
import random

class Player:
    def __init__(self, db: AsyncSession, user_id:int, deck_id:int, cards = dict[int,int]) -> None:
        self.db = db
        self.user_id = user_id
        self.deck_id = deck_id
        self.hands = []
        self.fields = []
        self.graveyards = []
        self.decks = [val for key, val in cards.items() for _ in range(key)]

    
    def shuffle(self):
        random.shuffle(self.decks)
        
    
    def draw(self, num = 1):
        for _ in range(num):
            self.hands.append(self.decks.pop())
    
    def summon_hand(self, index):
        card = self.hands.pop(index)