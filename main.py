import random
import math
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
        return []
    else:
        n = len(subsets)
        indices = np.zeros(n)
        for i in range(n):
            for j in range(4):
                if (subsets[i][0][j] == subsets[i][1][j] == subsets[i][2][j]) or (
                        subsets[i][0][j] != subsets[i][1][j] != subsets[i][2][j] != subsets[i][0][j]):
                    indices[i] += 1
                else:
                    break
        for i in range(n):
            if indices[i] >= 4:
                set_index = i
                break
            else:
                set_index = []
    if not set_index:
        sets = []
    else:
        sets = subsets[set_index]
    return sets


def get_spread(deck):
    if len(deck) == 0:
        return print("Beautiful ending of zero cards, good fortune for you.")
    elif len(deck) <= 12:
        spread = deck.copy()
        sets = find_set(spread)
        if not sets:
            return print("Yippee")
        else:
            indices = [0, 0, 0]
            for i in range(len(spread)):
                for k in range(3):
                    card_of_moment = spread[i]
                    if np.array_equiv(sets[k], card_of_moment):
                        indices[k] = int(i)
            spread = np.delete(spread, indices, axis=0)
            return get_spread(spread)
    elif len(deck) <= 15:
        spread = deck[:12]
        deck_new = deck[12:]
        sets = find_set(spread)
        if not sets:
            spread = np.append(spread, deck[:3], axis=0)
            deck_new = deck[3:]
            sets = find_set(spread)
            if not sets:
                return print("Yuppee")
            else:
                indices = [0, 0, 0]
                for i in range(len(spread)):
                    for k in range(3):
                        card_of_moment = spread[i]
                        if np.array_equiv(sets[k], card_of_moment):
                            indices[k] = int(i)
                spread = np.delete(spread, indices, axis=0)
                return get_spread(spread)
        else:
            for k in range(3):
                for i in range(len(spread)):
                    if np.array_equiv(sets[k], spread[i]):
                        spread[i] = deck_new[k]
            deck_new = deck_new[3:]
            return get_spread(spread)
    elif len(deck) <= 18:
        spread = deck[12:]
        deck_new = deck[12:]
        sets = find_set(spread)
        if not sets:
            spread = np.append(spread, deck[:3], axis=0)
            deck_new = deck[3:]
            sets = find_set(spread)
            if not sets:
                spread = np.append(spread, deck_new[:3], axis=0)
                deck_new = deck_new[3:]
                sets = find_set(spread)
                if not sets:
                    return print("Yoppee")
                else:
                    indices = [0, 0, 0]
                    for i in range(len(spread)):
                        for k in range(3):
                            card_of_moment = spread[i]
                            if np.array_equiv(sets[k], card_of_moment):
                                indices[k] = int(i)
                    spread = np.delete(spread, indices, axis=0)
                    return get_spread(spread)
            else:
                for k in range(3):
                    for i in range(len(spread)):
                        if np.array_equiv(sets[k], spread[i]):
                            spread[i] = deck_new[k]
                deck_new = deck_new[3:]
                deck = np.append(spread, deck_new, axis=0)
                return get_spread(deck)
    else:
        spread = deck[:12]
        deck_new = deck[12:]
        sets = find_set(spread)
        if not sets:
            spread = np.append(spread, deck_new[:3], axis=0)
            deck_new = deck_new[3:]
            sets = find_set(spread)
            if not sets:
                spread = np.append(spread, deck_new[:3], axis=0)
                deck_new = deck_new[3:]
                sets = find_set(spread)
                if not sets:
                    spread = np.append(spread, deck_new[:3], axis=0)
                    deck_new = deck_new[3:]
                    sets = find_set(spread)
                    indices = [0, 0, 0]
                    if not sets:
                        return print("Ummmmmm...")
                    for k in range(3):
                        for i in range(len(spread)):
                            if np.array_equiv(sets[k], spread[i]):
                                indices[k] = i
                    spread = np.delete(spread, indices, axis=0)
                    deck = np.append(spread, deck_new, axis=0)
                    return get_spread(deck)
                else:
                    indices = [0, 0, 0]
                    for k in range(3):
                        for i in range(len(spread)):
                            if np.array_equiv(sets[k], spread[i]):
                                indices[k] = i
                    spread = np.delete(spread, indices, axis=0)
                    deck = np.append(spread, deck_new, axis=0)
                    return get_spread(deck)
            else:
                indices = [0, 0, 0]
                for k in range(3):
                    for i in range(len(spread)):
                        if np.array_equiv(sets[k], spread[i]):
                            indices[k] = i
                spread = np.delete(spread, indices, axis=0)
                deck = np.append(spread, deck_new, axis=0)
                return get_spread(deck)
        else:
            for k in range(3):
                for i in range(len(spread)):
                    if np.array_equiv(sets[k], spread[i]):
                        spread[i] = deck_new[k]
            deck_new = deck_new[3:]
            deck = np.append(spread, deck_new, axis=0)
            return get_spread(deck)

get_spread(get_deck())
