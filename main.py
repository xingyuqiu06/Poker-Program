import random
def poker(hands):
    "Return a list of the best hand: poker([hand,hand,hand]) => hand"
    return allmax(hands, key=hand_rank)

def allmax(iter, key=None):
    "return a list of all items equal to the max of the iterable"
    result, maxval = [], None
    key = key or (lambda x: x)
    for x in iter:
        xval = key(x)
        if not result or xval > maxval:
            maxval = xval
            result = [x]
        elif xval == maxval:
            result.append(x)
    return result

def deal(num_player, n=5, deck = [r+s for r in '23456789TJQKA' for s in 'SHDC']):
    random.shuffle(deck)
    return [deck[n*i:n*(i+1)] for i in range(num_player)]

def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first"
    ranks = ['--23456789TJQKA'.index(r) for r,s in hand]
    ranks.sort(reverse = True)
    return [5,4,3,2,1] if (ranks == [14,5,4,3,2]) else ranks

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    # Your code here.
    for r in ranks:
        if n == ranks.count(r):return r
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    a = []
    for r in ranks:
        if ranks.count(r) == 2:a.append(r)
    if len(set(a)) == 2:return (a[0], a[2])
    return None

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    a = 0
    for v in ranks:
        v = int(v)
        index = ranks.index(v)
        if index < len(ranks)-1 and v - int(ranks[index+1]) == 1:
            a += 1
    return a == len(ranks)-1

def flush(hand):
    "Return True if all the cards have the same suit."
    suit = [s for r,s in hand]
    return all(s == suit[0] for s in suit)


def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):  # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):  # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):  # full house
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):  # flush
        return (5, ranks)
    elif straight(ranks):  # straight
        return (4, max(ranks))
    elif kind(3, ranks):  # 3 of a kind
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):  # 2 pair
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):  # kind
        return (1, kind(2, ranks), ranks)
    else:  # high card
        return (0, ranks)

hand_names = ['sf', 'fk', 'fh', 'fl','straight', 'tk', 'tp', 'kd', 'hc']
def test():
    "Test cases for the function in poker program"
    sf = "6C 7C 8C 9C TC".split()
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    tp = "TD 9H TH 7C 3S".split() # Two Pair
    fkranks = card_ranks(fk)
    tpranks = card_ranks(tp)
    assert card_ranks(fk) == [9,9,9,9,7]
    assert kind(4, fkranks) == 9
    assert kind(3, fkranks) == None
    assert kind(2, fkranks) == None
    assert kind(1, fkranks) == 7
    assert straight([9,8,7,6,5]) == True
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh,fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    return print("tests pass")

def hand_percentages(n=700*1000):
    counts = [0]*9
    for i in range(int(n/10)):
        for hand in deal(num_player=10):
            rankings = hand_rank(hand)[0]
            counts[rankings] += 1
    for i in reversed(range(9)):
        print("%14s: %6.3f %%" % (hand_names[i], 100.*counts[i]/n))

hand_percentages()
test()