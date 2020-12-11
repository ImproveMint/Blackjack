from pandas import DataFrame

from card import Card, Rank, Suit
from hand import Hand
from dealer import Dealer
import probability

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
        if max_value > 0.5:
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
    'D' = Double or else Hit
    'd' = Double or else stand
    '''
    action_probs = probability.probability_of_complete_actions_winning(shoe, hand, dealer)

    max_value = max(action_probs)
    optimal = '*'

    if max_value == action_probs[0]:
        # double if in your favour otherwise hit
        if max_value > 0.5:
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

def produce_basic_strategy(shoe):

    bs_hard = [ [0] * 10 for _ in range(10)]
    bs_soft = [ [0] * 10 for _ in range(7)]
    bs_split = [ [0] * 10 for _ in range(10)]

    #Hard table
    for row in range(0, 10):
        for col in range(0, 10):
            assert(shoe.cards_in_shoe == 52*shoe.DECKS)
            #print(f"({row}, {col})")
            d_rank = Rank(col+1) # dealer's up card rank

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

            d1 = Card(d_rank, Suit.Spade)

            dealer = Dealer(shoe)
            dealer.deal_card(d1)

            p_hand = Hand([p1,p2])
            d_hand = Hand([d1])
            shoe.draw(d1)
            optimal = optimal_action(shoe, p_hand, dealer)
            print(f"{p_hand.value} VS {d_hand.value} --> '{optimal}'")
            shoe.reinstate_card(d1)
            bs_hard[row][col] = optimal

    # Soft Table
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
    #         d_hand = Hand([d1])
    #
    #         shoe.draw(d1)
    #         shoe.draw(p1)
    #         optimal = shoe.optimal_action(p_hand, d_hand)
    #         print(f"{p_hand.value} VS {d_hand.value} --> '{optimal}'")
    #         shoe.__add_card(d1)
    #         shoe.__add_card(p1)
    #         bs_soft[row][col] = optimal

    #Split Table
    # for row in range(7, 9):
    #     for col in range(0, 10):
    #         assert(shoe.cards_in_shoe == 52*shoe.DECKS)
    #         #print(f"({row}, {col})")
    #         d_rank = Rank(col+1) # dealer's up card rank
    #         p_rank = Rank(row+1)
    #
    #         if d_rank == 10:
    #             d_rank = Rank.Ace
    #         if p_rank == 10:
    #             p_rank = Rank.Ace
    #
    #         p1 = Card(p_rank, Suit.Spade)
    #         p2 = Card(p_rank, Suit.Spade)
    #         d1 = Card(d_rank, Suit.Spade)
    #
    #         p_hand = Hand([p1,p2])
    #         d_hand = Hand([d1])
    #
    #         shoe.draw(d1)
    #         shoe.draw(p1)
    #         shoe.draw(p2)
    #         optimal = shoe.optimal_action(p_hand, d_hand)
    #         print(f"{p_hand.value} VS {d_hand.value} --> '{optimal}'")
    #         shoe.__add_card(d1)
    #         shoe.__add_card(p1)
    #         shoe.__add_card(p2)
    #         bs_split[row][col] = optimal

    print(DataFrame(bs_hard))
    #print(DataFrame(bs_soft))
    #print(DataFrame(bs_split))

def produce_complete_strategy(shoe):

    bs_hard = [ [0] * 10 for _ in range(10)]
    bs_soft = [ [0] * 10 for _ in range(7)]
    bs_split = [ [0] * 10 for _ in range(10)]

    #Hard table
    for row in range(0, 10):
        for col in range(0, 10):
            assert(shoe.cards_in_shoe == 52*shoe.DECKS)
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

            d1 = Card(d_rank, Suit.Spade)

            dealer = Dealer(shoe)
            dealer.deal_card(d1)

            p_hand = Hand([p1,p2])
            d_hand = Hand([d1])
            shoe.draw(d1)
            optimal = optimal_complete_action(shoe, p_hand, dealer)
            print(f"{p_hand.value} VS {d_hand.value} --> '{optimal}'")
            shoe.reinstate_card(d1)
            bs_hard[row][col] = optimal

    print(DataFrame(bs_hard))
