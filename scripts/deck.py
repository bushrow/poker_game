from itertools import product
import random


class Deck:
    SUITS = "HDCS"
    VALS = "23456789TJQKA"
    CARDS = [v + s for v, s in product(VALS, SUITS)]

    def __init__(self):
        self.cards = Deck.CARDS[:]

    @staticmethod
    def value(c):
        return Deck.VALS.index(c[0])

    @staticmethod
    def suit(c):
        return c[1]

    def shuffle(self):
        self.cards = Deck.CARDS[:]
        random.shuffle(self.cards)

    def deal(self, num_players):
        self.shuffle()
        dealt_cards = self.cards[: num_players * 2]
        self.cards = self.cards[num_players * 2 :]
        return dealt_cards

    def burn(self):
        self.cards.pop(0)

    def turn(self):
        return self.cards.pop(0)