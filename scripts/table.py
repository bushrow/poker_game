from uuid import uuid4

from scripts.deck import Deck
from scripts.hand import Hand


class Table:
    def __init__(self, players, blinds=(5, 10), bet_limit=5000):
        self.table_id = uuid4()
        self.max_seats = 9
        self.blinds = blinds
        self.bet_limits = (blinds[0], bet_limit)
        self.pot = 0
        self.current_bet = 0

        self.deck = Deck()
        self.cards_showing = []

        self._init_players(players)

    def __repr__(self):
        return f"Table: {self.num_players}/9 seats filled\n{self.blinds} blinds\n{self.bet_limits} limits"

    def _init_players(self, players):
        self.players = []
        self.player_hands = {}
        self.num_players = 0
        self.seats = {i: None for i in range(self.max_seats)}
        self.open_seats = list(range(self.max_seats))

        for p in players:
            p.join_table(self)

        self.button_order = [s for s in self.seats if self.seats[s]]
        self.button_start_ix = -1

    def pass_button(self):
        self.button_order = [p for p in self.seats.values() if p]
        self.button_start_ix += 1
        if (self.button_start_ix >= len(self.button_order)) or self.button_start_ix < 0:
            self.button_start_ix = 0
        for p in self.button_order:
            p.seat_button = None
        self.button_order[self.button_start_ix].seat_button = "D"
        (self.button_order[1:] + self.button_order[:1])[
            self.button_start_ix
        ].seat_button = "SB"
        (self.button_order[2:] + self.button_order[:2])[
            self.button_start_ix
        ].seat_button = "BB"

    def deal(self):
        dealt_cards = self.deck.deal(self.num_players)
        self.player_hands = {
            p: Hand((dealt_cards[i], dealt_cards[self.num_players + i]))
            for i, p in enumerate(self.players)
        }
        self.cards_showing = []

    def flop(self):
        self.deck.burn()
        self.cards_showing.extend([self.deck.turn() for _ in range(3)])

    def turn(self):
        self.deck.burn()
        self.cards_showing.append(self.deck.turn())

    def collect_blinds(self):
        for p in self.players:
            if p.seat_button == "SB":
                p.bet(self.blinds[0], blind=True)
            elif p.seat_button == "BB":
                p.bet(self.blinds[1], blind=True)

    def collect_bets(self, under_gun=False):
        if len([p for p in self.players if not p.folded]) == 1:
            return

        start_ix = self.button_start_ix + 1
        if under_gun:
            start_ix += 2
        for p in self.players[start_ix:] + self.players[:start_ix]:
            if p.folded or p.all_in:
                continue
            p.choose_action()

        i = start_ix
        while True:
            bets = [p.current_bet for p in self.players if not (p.folded or p.all_in)]
            pots_right = all(b == self.current_bet for b in bets)
            if pots_right or len(bets) <= 1:
                break

            if self.players[i].folded or self.players[i].all_in:
                i += 1
            else:
                self.players[i].choose_action()
                i += 1
            if i >= self.num_players:
                i -= self.num_players

        self.current_bet = 0
        for p in self.players:
            p.current_bet = 0

    def distribute_pot(self, winners):
        for winner in winners:
            winner[0].bank_roll += self.pot / len(winners)
            print(f"{(str(winner[0])+':').ljust(25)} {winner[1]} ({winner[2]})")

        self.pot = 0