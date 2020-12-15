from pandas import DataFrame
from card import Card, Rank, Suit
from hand import Hand
from dealer import Dealer
import probability
from shoe import Shoe
import numpy

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

def infinite_basic_action(hand, dealer):
    '''
    Returns the basic strategy action for a player given their, hand, the dealer's hand
    and assuming the shoe has no removal effects
    '''
    #In future add checks for soft and splits
    lookup_row = -1
    lookup_col = -1

    if hand.soft:
        if hand.value >= 19:
            lookup_row = 6
        else:
            lookup_row = hand.value - 13

    #For hard basic strategy
    # assign correct row lookup
    else:
        if hand.value <= 8:
            lookup_row = 0
        elif hand.value >= 17:
            lookup_row = 9
        else:
            lookup_row = hand.value-8

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
    '''
    Returns the complete strategy action for a player given their, hand, the dealer's hand
    and assuming the shoe has no removal effects
    '''
    #In future add checks for soft and splits
    lookup_row = -1
    lookup_col = -1

    if hand.soft:
        if hand.value == 19:
            lookup_row = 1
        elif hand.value == 20:
            lookup_row = 2
        else:
            lookup_row = 0

    #For hard basic strategy
    # assign correct row lookup
    else:
        if hand.value <= 8:
            lookup_row = 0
        elif hand.value >= 17:
            lookup_row = 9
        else:
            lookup_row = hand.value-8

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

def optimal_action(shoe, hand, dealer):
    '''
    Returns the optimal action given a player's hand and the up card of the
    dealer. This currently functions using basic strategy approach which
    seems to be a one step look ahead

    Returns a character representing which action is optimal
    'H' = Hit
    'S' = Stand
    'P' = Split
    'D' = Double or else Hit
    'd' = Double or else stand
    '''
    action_probs = probability.probability_of_basic_actions_winning(shoe, hand, dealer)

    max_value = max(action_probs)
    optimal = '*'

    if max_value == action_probs[0]:
        # double if in your favour otherwise hit
        if 2*(2*action_probs[2]-1) > 2*action_probs[0] -1: #EV calculation
            optimal = 'D'
        else:
            optimal = 'H'

    elif max_value == action_probs[1]:
        # double if in your favour otherwise stand
        if 2*(2*action_probs[2] - 1) > (2*action_probs[1] - 1):
            optimal = 'd'
        else:
            optimal = 'S'

    elif max_value == action_probs[3]:
        optimal = 'P'

    return optimal

def optimal_complete_action(shoe, hand, dealer):
    '''
    Returns the optimal action given a player's hand and the up card of the
    dealer. This currently functions using basic strategy approach which
    seems to be a one step look ahead

    Returns a character representing which action is optimal
    'H' = Hit
    'S' = Stand
    'P' = Split
    'D' = Double otherwise Hit
    'd' = Double otherwise Stand
    '''
    action_probs = probability.probability_of_complete_actions_winning(shoe, hand, dealer)

    max_value = max(action_probs)

    if round(max_value,2) > 1:
        print(hand)
        print(dealer.hand)
        print(action_probs)
        assert(max_value <= 1)

    optimal = '*'

    if max_value == action_probs[0]:
        # double if in your favour otherwise hit
        if 2*(2*action_probs[2] - 1) > 2*action_probs[0] - 1: #EV calculation
            optimal = 'D'
        else:
            optimal = 'H'

    elif max_value == action_probs[1]:
        # double if in your favour otherwise stand
        if 2*(2*action_probs[2] - 1) > (2*action_probs[1] - 1): #EV calculation
            optimal = 'd'
        else:
            optimal = 'S'

    elif max_value == action_probs[3]:
        optimal = 'P'

    return optimal

def produce_basic_strategy(decks):

    shoe = Shoe(decks)

    bs_hard = [ [0] * 10 for _ in range(10)]
    bs_soft = [ [0] * 10 for _ in range(7)]
    bs_split = [ [0] * 10 for _ in range(10)]

    #Hard table
    # for row in range(0, 10):
    #     for col in range(0, 10):
    #         assert(shoe.cards_in_shoe == 52*shoe.DECKS)
    #         #print(f"({row}, {col})")
    #         d_rank = Rank(col+1) # dealer's up card rank
    #
    #         if d_rank == 10:
    #             d_rank = Rank.Ace
    #
    #         # player values 8 - 11
    #         if row < 4:
    #             p1 = Card(Rank.Six, Suit.Spade)
    #             p2 = Card(Rank(row+1), Suit.Spade)
    #         # Player values 12 - 18
    #         elif row >= 4:
    #             p1 = Card(Rank.Ten, Suit.Spade)
    #             p2 = Card(Rank(row-3), Suit.Spade)
    #
    #         d1 = Card(d_rank, Suit.Spade)
    #
    #         dealer = Dealer(shoe)
    #         dealer.deal_card(d1)
    #
    #         p_hand = Hand([p1,p2])
    #         d_hand = Hand([d1])
    #         shoe.draw(d1)
    #         optimal = optimal_action(shoe, p_hand, dealer)
    #         print(f"{p_hand.value} VS {d_hand.value} --> '{optimal}'")
    #         shoe.reinstate_card(d1)
    #         bs_hard[row][col] = optimal

    #Soft Table
    # for row in range(0, 7):
    #     for col in range(0, 10):
    #         assert(shoe.cards_in_shoe == 52*shoe.DECKS)
    #         #print(f"({row}, {col})")
    #         d_rank = Rank(col+1) # dealer's up card rank
    #
    #         if d_rank == 10:
    #             d_rank = Rank.Ace
    #
    #         p1 = Card(Rank.Ace, Suit.Spade)
    #         p2 = Card(Rank(row+1), Suit.Spade)
    #         d1 = Card(d_rank, Suit.Spade)
    #
    #         p_hand = Hand([p1,p2])
    #         dealer = Dealer(shoe)
    #         dealer.deal_card(d1)
    #
    #         shoe.draw(d1)
    #         shoe.draw(p1)
    #         optimal = optimal_action(shoe, p_hand, dealer)
    #         print(f"{p_hand.value} VS {dealer.hand.value} --> '{optimal}'")
    #         shoe.reinstate_card(d1)
    #         shoe.reinstate_card(p1)
    #         bs_soft[row][col] = optimal

    # Split Table
    for row in range(0, 10):
        for col in range(0, 10):
            assert(shoe.cards_in_shoe == 52*shoe.DECKS)
            d_rank = Rank(col+1) # dealer's up card rank
            p_rank = Rank(row+1)

            if d_rank == 10:
                d_rank = Rank.Ace
            if p_rank == 10:
                p_rank = Rank.Ace

            p1 = Card(p_rank, Suit.Spade)
            p2 = Card(p_rank, Suit.Spade)
            d1 = Card(d_rank, Suit.Spade)

            p_hand = Hand([p1,p2])
            dealer = Dealer(shoe)
            dealer.deal_card(d1)

            shoe.draw(d1)
            shoe.draw(p1)
            shoe.draw(p2)
            optimal = optimal_action(shoe, p_hand, dealer)
            print(f"{p_hand.value} VS {dealer.hand.value} --> '{optimal}'")
            shoe.reinstate_card(d1)
            shoe.reinstate_card(p1)
            shoe.reinstate_card(p2)
            bs_split[row][col] = optimal

    print(DataFrame(bs_hard))
    print(DataFrame(bs_soft))
    print(DataFrame(bs_split))

def produce_complete_strategy(decks):

    shoe = Shoe(decks)

    bs_hard = [ [0] * 10 for _ in range(10)]
    bs_soft = [ [0] * 10 for _ in range(8)]
    bs_split = [ [0] * 10 for _ in range(10)]

    #Hard table
    # for row in range(0, 10):
    #     for col in range(0, 10):
    #         d_rank = Rank(col+1)
    #
    #         if d_rank == 10:
    #             d_rank = Rank.Ace
    #
    #         # player values 8 - 11
    #         if row < 4:
    #             p1 = Card(Rank.Six, Suit.Spade)
    #             p2 = Card(Rank(row+1), Suit.Spade)
    #         # Player values 12 - 18
    #         elif row >= 4:
    #             p1 = Card(Rank.Ten, Suit.Spade)
    #             p2 = Card(Rank(row-3), Suit.Spade)
    #
    #         d1 = Card(d_rank, Suit.Spade)
    #
    #         dealer = Dealer(shoe)
    #         dealer.deal_card(d1)
    #
    #         p_hand = Hand([p1,p2])
    #         d_hand = Hand([d1])
    #         shoe.draw(d1)
    #         optimal = optimal_complete_action(shoe, p_hand, dealer)
    #         print(f"{p_hand.value} VS {d_hand.value} --> '{optimal}'")
    #         shoe.reinstate_card(d1)
    #         bs_hard[row][col] = optimal
    #
    # print(DataFrame(bs_hard))

    #Soft Table
    for row in range(0, 8):
        for col in range(0, 10):
            assert(shoe.cards_in_shoe == 52*shoe.DECKS)
            #print(f"({row}, {col})")
            d_rank = Rank(col+1) # dealer's up card rank

            if d_rank == 10:
                d_rank = Rank.Ace

            p1 = Card(Rank.Ace, Suit.Spade)
            p2 = Card(Rank(row+1), Suit.Spade)
            d1 = Card(d_rank, Suit.Spade)

            p_hand = Hand([p1,p2])
            dealer = Dealer(shoe)
            dealer.deal_card(d1)

            shoe.draw(d1)
            shoe.draw(p1)
            optimal = optimal_complete_action(shoe, p_hand, dealer)
            print(f"{p_hand.value} VS {dealer.hand.value} --> '{optimal}'")
            shoe.reinstate_card(d1)
            shoe.reinstate_card(p1)
            bs_soft[row][col] = optimal

    print(DataFrame(bs_soft))
