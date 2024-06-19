import numpy as np
from itertools import combinations as combo

# initializing attributes
color = [0, 1, 2]
text = [0, 1, 2]
shape = [0, 1, 2]
mult = [0, 1, 2]
attr = [color, text, shape, mult]

# get rand deck
def get_deck():
    deck = np.zeros((81, 4))
    for i in range(81):
        # Multiplicity
        deck[i][0] = i % 3
        # Texture
        if (int(i / 3)) % 3 == 0:
            pass
        elif (int(i / 3)) % 3 == 1:
            deck[i][1] = 1
        else:
            deck[i][1] = 2
        # Color
        if (int(i / 9)) % 3 == 0:
            pass
        elif (int(i / 9)) % 3 == 1:
            deck[i][2] = 1
        else:
            deck[i][2] = 2
        # Shape
        if (int(i / 27)) % 3 == 0:
            pass
        elif (int(i / 27)) % 3 == 1:
            deck[i][3] = 1
        else:
            deck[i][3] = 2
        # Shuffling
    np.random.shuffle(deck)
    return deck

def find_set(spread):
    subsets = list(combo(spread, 3))
    if len(subsets) == 0:
        sets = []
        return sets
    else:
        n = len(subsets)
        indices = np.zeros(n)
        for i in range(n):
            for j in range(4):
                if (subsets[i][0][j] == subsets[i][1][j] == subsets[i][2][j]) or (subsets[i][0][j] != subsets[i][1][j] != subsets[i][2][j] != subsets[i][0][j]):
                    indices[i] += 1
                else:
                    break
        set_index = []
        for i in range(len(indices)):
            if indices[i] >= 4:
                set_index = np.append(set_index, i)
                break
            else:
                continue
        if len(set_index) == 0:
            sets = []
        else:
            sets = subsets[int(set_index[0])]
        return sets

def get_spread_end(spread, deck_new): #finishes game at point where sets are deleted, not replaced
    chosen_set = find_set(spread)
    if not chosen_set and len(deck_new) >= 3:
        return get_spreader(spread, deck_new)
    elif not chosen_set:
        return print("game ends with", len(spread))
    else:
        indices = [0, 0, 0]
        for i in range(len(spread)):
            for k in range(3):
                if np.array_equiv(chosen_set[k], spread[i]):
                    indices[k] = int(i)
        spread = np.delete(spread, indices, axis=0)
        return get_spread_end(spread, [])


def get_spreader(spread, deck_new): #adds three cards to spread
    spread = np.append(spread, deck_new[:3], axis=0)
    deck_new = deck_new[3:]
    return spread, deck_new

def get_spread(deck): #continues game at point where sets are replaced
    spread = deck[:12]
    deck_new = deck[12:]
    chosen_set = find_set(spread)
    for i in range(int(len(deck_new) / 3)):
        if not chosen_set:
            spread, deck_new = get_spreader(spread, deck_new)
            chosen_set = find_set(spread)
        else:
            break
    if not chosen_set:
        return print("game ends with", len(spread))
    elif len(deck_new) < 3:
         return get_spread_end(spread, deck_new)
    else:
        for k in range(3):
            for i in range(len(spread)):
                if np.array_equiv(chosen_set[k], spread[i]):
                    spread[i] = deck_new[k]
        deck_new = deck_new[3:]
        deck = np.append(spread, deck_new, axis=0)
        return get_spread(deck)

get_spread(get_deck())