from itertools import combinations

from scripts.deck import Deck
from scripts.ranking import compare_hands


class Hand:
    def __init__(self, cards=[]):
        self.cards = cards

    def __repr__(self):
        return " ".join(sorted(self.cards, key=lambda c: Deck.VALS.index(c[0])))

    def best_hand(self, table_cards):
        cards = table_cards[:]
        cards.extend(self.cards)
        best = Hand()
        best_label = None
        for h in combinations(cards, 5):
            label = compare_hands(h, best.cards)
            if label:
                best = Hand(h)
                best_label = label.replace("_", " ").title()
        return best, best_label

    def show_odds(self):
        pass