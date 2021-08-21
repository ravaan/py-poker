def poker(hands, key=None):
    """Returns the list of best poker hands from the given hands"""
    if not key:
        key = hand_rank
    return all_max(hands, key=key)


def all_max(iterable, key=lambda x: x):
    """Return a list of all items equal to the max of the iterable"""
    result, maxvalue = [], None

    for iter in iterable:
        iter_value = key(iter)
        if iter_value == maxvalue:
            result.append(iter)
        if not result or iter_value > maxvalue:
            result, maxvalue = [iter], iter_value
    return result


def hand_rank(hand):
    """Return the value representing the rank of the hand"""
    ranks = card_ranks(hand)

    if straight(ranks) and flush(hand):
        return 8, max(ranks)
    elif kind(4, ranks):
        return 7, max(ranks), min(ranks)
    elif kind(3, ranks) and kind(2, ranks):
        return 6, kind(3, ranks), kind(2, ranks)
    elif flush(hand):
        return 5, ranks
    elif straight(ranks):
        return 4, max(ranks)
    elif kind(3, ranks):
        return 3, kind(3, ranks), ranks
    elif two_pairs(ranks):
        return 2, two_pairs(ranks), ranks
    elif kind(2, ranks):
        return 1, kind(2, ranks), ranks
    return 0, ranks


def card_ranks(cards):
    """Return the rank of the given card"""
    ranks = ['..23456789TJQKA'.index(rank) for rank, _ in cards]
    ranks.sort(reverse=True)

    # handle A 2 3 4 5 straight
    if ranks == [14, 5, 4, 3, 2]:
        ranks = [5, 4, 3, 2, 1]

    return ranks


def straight(ranks):
    """Return true if ranks for a straight"""
    return (max(ranks) - min(ranks) == 4) and len(set(ranks)) == 5


def flush(cards):
    """Return true if all cards have the same suit"""
    suits = [suit for _, suit in cards]
    return len(set(suits)) == 1


def kind(n, ranks):
    """Returns the first rank this hand has n of,"""
    "returns none if no rank is n-of-a kind"
    for rank in ranks:
        if ranks.count(rank) == n:
            return rank
    return None


def two_pairs(ranks):
    """Returns the ranks in decreasing order"""
    "if there are two pairs of them else returns None"
    pair = kind(2, ranks)
    low_pair = kind(2, list(reversed(ranks)))
    if pair and pair is not low_pair:
        return pair, low_pair
    return None

def get_count_and_rank(hand):
    groups = group(["..23456789TJQKA".index(rank) for rank, _ in hand])
    return zip(*groups)


def hand_rank1(hand):
    """Return the value representing the rank of the hand"""
    counts, ranks = get_count_and_rank(hand)
    if ranks == [14, 5, 4, 3, 2]:
        ranks = [5, 4, 3, 2, 1]

    is_straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    is_flush = len(set([suit for _, suit in hand])) == 1
    return (9 if (5, ) == counts else
            8 if is_straight and is_flush else
            7 if (4, 1) == counts else
            6 if (3, 2) == counts else
            5 if is_flush else
            4 if is_straight else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else
            1 if (2, 1, 1, 1) == counts else
            0), ranks


def hand_rank2(hand):
    """Return the value representing the rank of the hand"""
    count_ranking = {
        (5, ): 10,
        (4, 1): 7,
        (3, 2): 6,
        (3, 1, 1): 3,
        (2, 2, 1): 2,
        (2, 1, 1, 1): 1,
        (1, 1, 1, 1, 1): 0
    }
    counts, ranks = get_count_and_rank(hand)
    if ranks == [14, 5, 4, 3, 2]:
        ranks = [5, 4, 3, 2, 1]

    is_straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    is_flush = len(set([suit for _, suit in hand])) == 1
    return max(count_ranking[counts], 4 * is_straight + 5 * is_flush), ranks


def group(items):
    """Return a list of [(count, x)...] in decreasing order of count"""
    "with highest x as tie breaker"
    group = [(items.count(x), x) for x in set(items)]
    return sorted(group, reverse=True)




def test(key=hand_rank):
    """Test cases for the poker program"""
    sf = "9S 7S 8S 5S 6S".split()  # Straight flush  - 8
    fk = "9S 9C 6H 9D 9H".split()  # Four of a kind  - 7
    fh = "2S 2H 6C 6H 6S".split()  # Full house      - 6
    flush = " 2H 5H TH QH AH".split()  # Flush       - 5
    s1 = "AH 3S 2H 4H 5H".split()  # A-5 Straight    - 4
    s2 = "2H 4S 3S 5H 6D".split()  # 2-6 Straight    - 4
    tk = "7H 7S 7D TH JD".split()  # Three of a Kind - 3
    tp = "7H 7C 2H 2C 3S".split()  # two pairs       - 2
    op = "AH AD 2H 5D QH".split()  # One pair        - 1
    ah = "AH 4S 3S 7H TH".split()  # Ace high        - 0
    sh = "2H 3H 5H 6D 7D".split()  # Seven high      - 0
    fk_ranks = card_ranks(fk)
    tp_ranks = card_ranks(tp)
    assert card_ranks(sf) == [9, 8, 7, 6, 5]
    assert card_ranks(fk) == [9, 9, 9, 9, 6]
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert kind(4, fk_ranks) == 9
    assert kind(3, fk_ranks) is None
    assert kind(2, fk_ranks) is None
    assert kind(1, fk_ranks) == 6
    assert two_pairs(fk_ranks) is None
    assert two_pairs(tp_ranks) == (7, 2)
    hands = [sf, sf, fk, fh, flush, s1, s2, s1, tk, tp, op, ah, sh] + 99 * [tk]
    assert poker(hands, key) == [sf, sf]
    assert poker([s1, s2], key) == [s2]
    assert poker([ah, sh], key) == [ah]
    return "Test Passed with key=" + key.__name__


print(test())
print(test(hand_rank1))
print(test(hand_rank2))
