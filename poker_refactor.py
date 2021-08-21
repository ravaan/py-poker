def poker(hands):
    "Returns the list of best poker hands from the given hands" 
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=lambda x:x):
    "Return a list of all items equal to the max of the iterable"
    result, maxval = [], None

    for iter in iterable:
        iter_value = key(iter)
        if iter_value == maxval:
            result.append(iter)
        if not result or iter_value > maxval:
            result, maxval = [iter], iter_value
    
    return result

def hand_rank(hand):
    "Return the value representing the rank of the hand"
    groups = group(["..23456789TJQKA".index(r) for r, _ in hand])
    counts, ranks = unzip(groups)
    if ranks == [14, 5, 4, 3, 2]: rank = [5, 4, 3, 2, 1]

    straight = len(ranks) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for _, s in hand])) == 1
    return (9 if (5, ) == counts else
            8 if straight and flush else
            7 if (4, 1) == counts else 
            6 if (3, 2) == counts else 
            5 if flush else 
            4 if straight else
            3 if (3, 1, 1) == counts else
            2 if (2, 2, 1) == counts else 
            1 if (2, 1, 1, 1) == counts else
            0), ranks

def group(items):
    "Return a list of [(count, x)...] in decreasing order of count with highest x as tie breaker"
    group = [(items.count(x), x) for x in set(items)]
    return sorted(group, reverse=True)

def unzip(pairs): return zip(*pairs)

def test():
    "Test cases for the poker program"
    sf = "9S 7S 8S 5S 6S".split() # Straight flush  - 8 
    fk = "9S 9C 6H 9D 9H".split() # Four of a kind  - 7
    fh = "2S 2H 6C 6H 6S".split() # Full house      - 6
    flush = " 2H 5H TH QH AH".split() # Flush       - 5
    s1 = "AH 3S 2H 4H 5H".split() # A-5 Straight    - 4
    s2 = "2H 4S 3S 5H 6D".split() # 2-6 Straight    - 4
    tk = "7H 7S 7D TH JD".split() # Three of a Kind - 3
    tp = "7H 7C 2H 2C 3S".split() # two pairs       - 2
    op = "AH AD 2H 5D QH".split() # One pair        - 1
    ah = "AH 4S 3S 7H TH".split() # Ace high        - 0
    sh = "2H 3H 5H 6D 7D".split() # Seven high      - 0
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([sf, sf, fk, fh, flush, s1, s2, s1, tk, tp, op, ah, sh] + 99 * [tk]) == [sf, sf]
    assert poker([s1, s2]) == [s2]
    assert poker([ah, sh]) == [ah]
    return "Test Passed"

print (test())