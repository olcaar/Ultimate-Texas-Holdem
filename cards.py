import random

# Define the deck of cards
suits = ['♠️', '♥️', '♦️', '♣️']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Define the possible hands in Texas Hold'em
hands = ['High Card', 'Pair', 'Two Pair', 'Three of a Kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind',
         'Straight Flush', 'Royal Flush']


class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(rank + suit)
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def shuffle(self):
        self.__init__()

