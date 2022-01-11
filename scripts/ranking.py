from scripts.deck import Deck


def counts(h):
    if not h:
        return []
    vals = [Deck.value(c) for c in h]
    return [vals.count(v) for v in set(vals)]


def score(h):
    if not h:
        return 0
    vals = [Deck.value(c) for c in h]
    return sum(len(Deck.VALS) ** i * v for i, v in enumerate(vals))


def straight_flush(h):
    return straight(h) and flush(h)


def four_of_a_kind(h):
    return 4 in counts(h)


def full_house(h):
    return 3 in counts(h) and 2 in counts(h)


def flush(h):
    if not h:
        return False
    return len(set(map(Deck.suit, h))) == 1


def straight(h):
    if not h:
        return False
    vals = sorted(Deck.value(c) for c in h)
    if vals[0] == 0 and vals[-1] == len(Deck.VALS) - 1:  # if there's a two and an ace
        vals = vals[:-1]  # then remove the ace
    return [x + 1 for x in vals[:-1]] == vals[1:]


def three_of_a_kind(h):
    return 3 in counts(h)


def two_pair(h):
    return counts(h).count(2) == 2


def pair(h):
    return 2 in counts(h)


def high_card(h):
    return True


hand_rank_funcs = [
    straight_flush,
    four_of_a_kind,
    full_house,
    flush,
    straight,
    three_of_a_kind,
    two_pair,
    pair,
    high_card,
]


def compare_hands(h1, h2):  # return True if h1 wins, False otherwise
    for f in hand_rank_funcs:
        r1, r2 = f(h1), f(h2)
        if r1 and not r2:
            return f.__name__
        elif r2 and not r1:
            return None
        elif r1 and r2:
            s1, s2 = score(h1), score(h2)
            if s1 > s2:
                return f.__name__
            elif s2 > s1:
                return None
            else:
                return 0
    return 0  # tie case
