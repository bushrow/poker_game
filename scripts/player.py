import random
from uuid import uuid4


class Player:
    def __init__(self, name, bank_roll):
        self.player_id = uuid4()

        self.name = name
        self.bank_roll = bank_roll

        self.table = None
        self.table_position = None
        self.seat_button = None

        self.folded = False
        self.current_bet = 0
        self.all_in = False

    def __repr__(self):
        s = (
            f"{self.name} - ${self.bank_roll} ({self.seat_button})"
            if self.seat_button
            else f"{self.name} - ${self.bank_roll}"
        )
        return s

    def deposit(self, amount):
        self.bank_roll += amount

    def join_table(self, table):
        self.table = table
        table.players.append(self)
        self.table_position = table.open_seats.pop(0)
        table.seats[self.table_position] = self
        table.num_players += 1
        table.player_hands[self] = None

    def leave_table(self):
        self.table.seats[self.table_position] = None
        self.table.open_seats.append(self.table_position)
        self.table_position = None
        self.table = None

    def bet(self, amount, blind=False, ante=False):
        self.bank_roll -= amount
        self.current_bet += amount
        if blind:
            print(self, "bet the blind.")
        elif ante:
            print(self, "ante'd up.")
        else:
            if self.current_bet > self.table.current_bet:
                if self.table.current_bet == 0:
                    print(f"{self} bet ${self.current_bet}.")
                else:
                    print(
                        f"{self} raised by ${self.current_bet - self.table.current_bet} to ${self.current_bet}."
                    )
            else:
                print(f"{self} called to ${self.current_bet}.")

        self.table.current_bet = max(self.table.current_bet, self.current_bet)
        self.table.pot += amount

    def choose_action(self):
        if self.name == "You":
            bet_amt = 0
            if self.table.current_bet > self.current_bet:
                action = input("Call (c), Raise (r), or Fold (f): ").lower()
                if action == "c":
                    # call
                    bet_amt = self.table.current_bet - self.current_bet
                elif action == "r":
                    # raise
                    bet_amt = int(input("Raise amount: $")) + self.table.current_bet
                else:
                    # fold
                    print("You folded.")
                    self.folded = True
                    return
            else:
                action = input("Check (k) or Bet (b): ").lower()

                if action == "b":
                    # bet
                    bet_amt = int(input("Bet amount: $"))
                elif action == "k":
                    # check
                    print("You checked.")
                    return
                else:
                    # fold
                    print("You folded.")
                    self.folded = True
                    return

        else:
            r = random.random()
            bet_amt = 0
            if self.table.current_bet > self.current_bet:
                bet_amt = max(self.table.current_bet - self.current_bet, 0)
                if r < 0.4:
                    # fold
                    print(self, "folded.")
                    self.folded = True
                    return
                elif r < 0.45:
                    # raise
                    bet_amt *= 2 + random.randint(0, 5) * self.table.blinds[0]

            else:
                if r < 0.75:
                    # check
                    print(self, "checked.")
                    return
                else:
                    # bet
                    bet_amt = random.randint(1, 5) * self.table.blinds[0]

        bet_amt = min(bet_amt, self.bank_roll)
        if bet_amt == self.bank_roll:
            self.all_in = True

        self.bet(bet_amt)