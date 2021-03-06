'''
*Differences in charts may be due to slight variations in rules
I think the differences in strategy expecially in soft chart
is due to 6 card charlie rule. 

My Optimal Hard Strategy
    2  3  4  5  6  7  8  9  T  A
8   H  H  H  H  H  H  H  H  H  H
9   H  D  D  D  D  H  H  H  H  H
10  D  D  D  D  D  D  D  D  H  H
11  D  D  D  D  D  D  D  D  H  H
12  H  H  S  S  S  H  H  H  H  H
13  S  S  S  S  S  H  H  H  H  H
14  S  S  S  S  S  H  H  H  H  H
15  S  S  S  S  S  H  H  H  H  H
16  S  S  S  S  S  H  H  H  H  H
17+ S  S  S  S  S  S  S  S  S  S

*DIFFERENCES in my strategy and basic
    2  3  4  5  6  7  8  9  T  A
11  .  .  .  .  .  .  .  .  D  .


My optimal soft strategy
    2  3  4  5  6  7  8  9  T  A
13  H  H  H  H  D  H  H  H  H  H
14  H  H  H  D  D  H  H  H  H  H
15  H  H  H  D  D  H  H  H  H  H
16  H  H  D  D  D  H  H  H  H  H
17  H  D  D  D  D  H  H  H  H  H
18  S  d  d  d  d  S  S  H  H  H
19  S  S  S  S  S  S  S  S  S  S

GAME update optimal strategy.... needs work
9 cent differnce vs 6. 12 cent vs 5
13  .  .  .  H  H  .  .  .  .  .

6 cent different vs 5 and 3 cent vs 6
14  .  .  .  H  H  .  .  .  .  .

Against 4 it's like a 5 cent different but against 5 it's 1.5
15  .  .  H  H  .  .  .  .  .  .

1.5 cent difference
16  .  .  H  .  .  .  .  .  .  .

*Differences in my strategy and basic
   2  3  4  5  6  7  8  9  T  A
13 .  .  .  D  .  .  .  .  .  .
14 .  .  .  .  .  .  .  .  .  .
15 .  .  D  .  .  .  .  .  .  .

My optimal split strategy differences these should all be splits
    2  3  4  5  6  7  8  9  T  A
22  H  H  H  H  P  H  H  H  H  H
33  H  H  H  P  P  P  H  H  H  H
44  H  H  H  H  H  H  H  H  H  H
55  D  D  D  D  D  D  D  D  H  H
66  H  P  P  P  P  H  H  H  H  H
77  P  P  P  P  P  P  H  H  H  H
88  P  P  P  P  P  P  P  P  H  H
99  P  P  P  P  P  S  P  P  S  S
TT  S  S  S  S  S  S  S  S  S  S

    2  3  4  5  6  7  8  9  T  A
22  .  .  P  P  .  P  .  .  .  .
33  .  .  P  .  .  .  .  .  .  .
88  .  .  .  .  .  .  .  .  P  P
'''

from pandas import DataFrame
from card import Card, Rank, Suit
from hand import Hand
from game import Game
import probability
from shoe import Shoe
import numpy
from constants import Action

#HARD BASIC Strategy for 8 deck ranging from 8 to 17
basic_strat_hard8 = numpy.array([  ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
                                    ['D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
                                    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
                                    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
                                    ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']])
basic_strat_soft8 = numpy.array([   ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
                                    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
                                    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
                                    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
                                    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'S'],
                                    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']])

#These are almost certainly garbage
complete_strat_hard8 = numpy.array([   ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
                                        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
                                        ['D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
                                        ['D', 'D', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H'],
                                        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
                                        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
                                        ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                        ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                        ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
                                        ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']])
complete_strat_soft8 = numpy.array([['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
                                    ['S', 'S', 'S', 'H', 'S', 'S', 'S', 'S', 'H', 'S'],
                                    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']]) # only for when value is 19 all others are H

'''
def infinite_basic_action(hand, dealer):

    # Returns the basic strategy action for a player given their, hand, the dealer's hand
    # and assuming the shoe has no removal effects

    #In future add checks for soft and splits
    lookup_row = -1
    lookup_col = -1

    if hand.soft:
        if hand.sum >= 19:
            lookup_row = 6
        else:
            lookup_row = hand.sum - 13

    #For hard basic strategy
    # assign correct row lookup
    else:
        if hand.sum <= 8:
            lookup_row = 0
        elif hand.sum >= 17:
            lookup_row = 9
        else:
            lookup_row = hand.sum-8

    # assign correct col lookup
    if dealer.hand.cards[0] == Rank.Ace:
        lookup_col = 9
    elif dealer.hand.cards[0].blackjack_value() == 10:
        lookup_col = 8
    else:
        lookup_col = dealer.hand.cards[0].rank-1

    if hand.soft:
        return basic_strat_soft8[lookup_row, lookup_col]
    else:
        return basic_strat_hard8[lookup_row, lookup_col]

def infinite_complete_action(hand, dealer):

    # Returns the complete strategy action for a player given their, hand, the dealer's hand
    # and assuming the shoe has no removal effects

    #In future add checks for soft and splits
    lookup_row = -1
    lookup_col = -1

    if hand.soft:
        if hand.sum == 19:
            lookup_row = 1
        elif hand.sum == 20:
            lookup_row = 2
        else:
            lookup_row = 0

    #For hard basic strategy
    # assign correct row lookup
    else:
        if hand.sum <= 8:
            lookup_row = 0
        elif hand.sum >= 17:
            lookup_row = 9
        else:
            lookup_row = hand.sum-8

    # assign correct col lookup
    if dealer.hand.cards[0] == Rank.Ace:
        lookup_col = 9
    elif dealer.hand.cards[0].blackjack_value() == 10:
        lookup_col = 8
    else:
        lookup_col = dealer.hand.cards[0].rank-1

    if hand.soft:
        return complete_strat_soft8[lookup_row, lookup_col]
    else:
        return complete_strat_hard8[lookup_row, lookup_col]
'''

def optimal_action(game):
    '''
    Returns the optimal action given a player's hand and the up card of the
    dealer

    Returns a character representing which action is optimal
    'H' = Hit
    'S' = Stand
    'P' = Split
    'D' = Double otherwise Hit
    'd' = Double otherwise Stand
    '''
    action_evs = probability.action_ev(game)
    optimal_action = action_evs.index(max(action_evs))

    if optimal_action == Action.HIT:
        return 'H'

    elif optimal_action == Action.STAND:
        return 'S'

    elif optimal_action == Action.DOUBLE:
        if action_evs[Action.HIT] > action_evs[Action.STAND]:
            return 'D' # Double if possible otherwise Hit
        else:
            return 'd' # Double if possible otherwise Stand

    elif optimal_action == Action.SPLIT:
        return 'P'

def calc_split_strategy(decks):
    # Split Table
    shoe = Shoe(8)
    rows = 9
    cols = 10
    bs_split = [ [0] * cols for _ in range(rows)]

    for row in range(0, rows):
        for col in range(0, cols):
            assert(shoe.cards_in_shoe == 52*shoe.DECKS)
            d_rank = Rank(col+1)
            p_rank = Rank(row+1)

            if d_rank == 10:
                d_rank = Rank.Ace
            if p_rank == 10:
                p_rank = Rank.Ace

            p1 = Card(p_rank, Suit.Spade)
            p2 = Card(p_rank, Suit.Spade)
            p_hand = Hand([p1,p2])
            upcard = Card(d_rank, Suit.Spade)

            game = Game(p_hand, upcard, shoe)

            optimal = optimal_action(game)
            shoe.reset_shoe()
            bs_split[row][col] = optimal

    print(DataFrame(bs_split))

def calc_hard_strategy(decks):

    shoe = Shoe(decks)
    rows = 10
    cols = 10
    bs_hard = [ [0] * cols for _ in range(rows)]

    #Hard table
    for row in range(0, rows):
        for col in range(0, cols):
            d_rank = Rank(col+1)

            if d_rank == 10:
                d_rank = Rank.Ace

            # player values 8 - 11
            if row < 4:
                p1 = Card(Rank.Six, Suit.Spade)
                p2 = Card(Rank(row+1), Suit.Spade)
            # Player values 12 - 18
            elif row >= 4:
                p1 = Card(Rank.Ten, Suit.Spade)
                p2 = Card(Rank(row-3), Suit.Spade)

            upcard = Card(d_rank, Suit.Spade)

            p_hand = Hand([p1,p2])

            game = Game(p_hand, upcard, shoe)

            optimal = optimal_action(game)
            bs_hard[row][col] = optimal
            shoe.reset_shoe()

    print(DataFrame(bs_hard))

def calc_soft_strategy(decks):

    shoe = Shoe(decks)

    rows = 7 # S13 - S19
    cols = 10
    bs_soft = [ [0] * cols for _ in range(rows)]

    #Soft Table
    for row in range(0, rows):
        for col in range(0, cols):
            assert(shoe.cards_in_shoe == 52*shoe.DECKS)
            d_rank = Rank(col+1) # dealer's up card rank

            if d_rank == 10:
                d_rank = Rank.Ace

            upcard = Card(d_rank, Suit.Spade)
            p1 = Card(Rank.Ace, Suit.Spade)
            p2 = Card(Rank(row+1), Suit.Spade)
            p_hand = Hand([p1,p2])

            game = Game(p_hand, upcard, shoe)
            optimal = optimal_action(game)
            bs_soft[row][col] = optimal
            shoe.reset_shoe()

    print(DataFrame(bs_soft))
