from time import sleep

from scripts.ranking import compare_hands
from scripts.hand import Hand
from scripts.player import Player
from scripts.table import Table


def play_round(table, real_time=False, duration=5):
    for p in table.players:
        p.folded = False
        p.all_in = False

    table.pass_button()
    table.collect_blinds()
    print()

    table.deal()

    if real_time:
        for p, h in table.player_hands.items():
            if p.name == "You":
                print(f"{(str(p)+':').ljust(25)} {h}")
            else:
                print(f"{(str(p)+':').ljust(25)} XX XX")
        print()

    else:
        print(table.player_hands, "\n")

    table.collect_bets(under_gun=True)

    if real_time:
        sleep(duration)

    print()
    table.flop()
    if real_time:
        print(table.cards_showing, "\t\t(Flop)", "\n")
        sleep(duration)
    table.collect_bets()

    print()
    table.turn()
    if real_time:
        print(table.cards_showing, "\t(Turn)", "\n")
        sleep(duration)
    table.collect_bets()

    print()
    table.turn()
    print(table.cards_showing, "\t(River)", "\n")
    if real_time:
        sleep(duration)
    table.collect_bets()
    print()

    if real_time:
        print("Pocket Cards:")
        for p, h in table.player_hands.items():
            print(f"{(str(p)+':').ljust(25)} {h}")
        print()

    print("Competing Hands:")
    winners = [(None, Hand(), None)]
    for p, h in table.player_hands.items():
        if p.folded:
            continue
        bh, label = h.best_hand(table.cards_showing)
        print(f"{(str(p)+':').ljust(25)} {bh} ({label})")
        res = compare_hands(bh.cards, winners[0][1].cards)
        if res:
            winners = [(p, bh, label)]
        elif res == 0:
            winners.append((p, bh, label))

    print()
    print(f"Final Pot: ${table.pot}")
    print("Winner(s):")
    table.distribute_pot(winners)


if __name__ == "__main__":
    player_names = ["You", "John", "Kayce", "Jamie", "Beth", "Rip"]
    players = [Player(n, 1000) for n in player_names]
    t = Table(players)
    while True:
        play_round(t, real_time=True)
        if input("Play again? (y/n): ") != "y":
            break
        else:
            print()