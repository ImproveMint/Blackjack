'''
This class calculates useful probabilities for the game of blackjack
'''

from copy import deepcopy
from card import Card, Rank, Suit
from hand import Hand
from shoe import Shoe
from constants import Action

def probability_of_card(shoe, card):
    '''
    Returns the probability that the next card drawn from the shoe will be 'card'
    '''
    return shoe.ranks_left[card.rank]/shoe.cards_in_shoe

def probability_of_hand(shoe, hand, index):
    '''
    Returns the probability of drawing to a specific hand starting from a specific
    hand as indicated by the value index.

    Assumes cards have not already been drawn from shoe!

    Example: If a hand consists of (ignoring suits) [3, 4, J, A, 2] and the
    index = 2, this function returns the probability of drawing a [J, A, 2]
    In a single deck shoe with replacement that would equal (4/13)*(4/13)*(4/13)
    '''

    shoe.cards_in_shoe

    # make copies so that variables can be reinstated after calculations
    copy_cards_in_shoe = shoe.cards_in_shoe
    copy_ranks_left = deepcopy(shoe.ranks_left)
    count = shoe.r_count

    prob = 1

    for card in range(index, len(hand.cards)):
        prob*=probability_of_card(shoe, hand.cards[card])
        shoe.draw(hand.cards[card])

    # reinstate values so shoe statistics remain unchanged
    shoe.cards_in_shoe = copy_cards_in_shoe
    shoe.ranks_left = copy_ranks_left
    shoe.r_count = count

    return prob

def probability_of_winning(hand, dealer_probs):
    '''
    Returns the probability of winning a hand against all possible dealer hands

    To call this function player needs a hand and dealer needs an up card
    '''

    value = hand.value
    win = 0

    # Player busted
    if value > 21:
        win = 0

    # Player has BJ and so only pushes against a dealer's BJ
    elif hand.blackjack:
        win = sum(dealer_probs) - dealer_probs[5]/2# it's a push if both have BJ so I think divided in 2 is equivalent

    elif value == 21:
        win = sum(dealer_probs) - (dealer_probs[4]/2) - dealer_probs[5] # here we have 21 so we push against 21, lose to dealer's BJ and win all other times

    #Any hand that didn't bust and is not blackjack
    else:
        for x in range(len(dealer_probs)-3):
            if value > x + 17:
                win += dealer_probs[x]
            elif value == x + 17:
                win += (dealer_probs[x]/2)
        win += dealer_probs[6] #Beats all busted hands

    return win

def probability_of_basic_actions_winning(shoe, hand, dealer):
    # hit and double should return the same value as they both return a
    # single card. I imagine the difference in choice has to do with the odds
    # if your odds are in your favour you should increase your bet size
    dealer_probs = dealer.dealer_outcome_probs()
    action_probs = [0, 0, 0, 0] # hit | stand | double | split

    hit = basic_hit(shoe, hand, dealer, len(hand.cards), dealer_probs)
    action_probs[Action.HIT] = hit
    # print(f"HIT {round(100*hit,2)}% ", end="")

    stand = basic_stand(hand, dealer, dealer_probs)
    action_probs[Action.STAND] = stand
    # print(f"STAND {round(100*stand,2)}% ", end="")

    double = hit
    action_probs[Action.DOUBLE] = double
    # print(f"DOUBLE {round(100*double,2)}% ", end="")

    if hand.can_split():
        split = basic_split(shoe, hand, dealer, dealer_probs)
        action_probs[Action.SPLIT] = split
        # print(f"SPLIT {round(100*split,2)}% ", end="")

    # print("")

    return action_probs

def probability_of_complete_actions_winning(shoe, hand, dealer):

    dealer_probs = dealer.dealer_outcome_probs()

    assert(round(sum(dealer_probs),2) == 1.00)

    action_probs = [0, 0, 0, 0] # hit | stand | double | split

    print(hand)

    hit = complete_hit(shoe, hand, dealer, len(hand.cards), dealer_probs)
    action_probs[0] = hit
    # print(f"HIT {round(100*hit,2)}% ", end="")

    print(hand)

    stand = basic_stand(hand, dealer, dealer_probs) # stand is same in every case
    action_probs[1] = stand
    # print(f"STAND {round(100*stand,2)}% ", end="")

    print(hand)

    double = complete_double(shoe, hand, dealer_probs)
    action_probs[2] = double

    print(hand)
    # print(f"DOUBLE {round(100*double,2)}% ", end="")

    # if hand.can_split():
    #     split = complete_split(hand, dealer)
    #     action_probs[3] = split
    #     print(f"SPLIT {round(100*split,2)}% ", end="")

    # print("")

    return action_probs

def basic_hit(shoe, hand, dealer, index, dealer_probs):
    '''
    Returns the probability of winning if player hits

    This function looks a single step ahead. IE It hits and then regardless
    of the value of the hand it stands and plays out the dealer
    '''

    win = 0

    # Hand is already perfect no need to hit - hitting would not necessarily make you lose but there's no advantage
    if hand.blackjack:
        return 0

    if hand.value == 21:
        hand_prob = probability_of_hand(shoe, hand, index)
        win_prob = basic_stand(hand, dealer, dealer_probs)
        win += hand_prob*win_prob
        return win

    # special rule that you can't hit after splitting aces
    elif hand.split_aces:
        hand_prob = probability_of_hand(shoe, hand, 1)
        win_prob = basic_stand(hand, dealer, dealer_probs)
        win += hand_prob*win_prob
        return win

    # the hand is hit with each possible card rank
    for rank in Rank:
        new_hand = deepcopy(hand)
        new_hand.add_card(Card(rank, Suit.Spade)) # arbitrary suit

        hand_prob = probability_of_hand(shoe, new_hand, index)
        win_prob = basic_stand(new_hand, dealer, dealer_probs)
        win += hand_prob*win_prob

    return win

def basic_stand(hand, dealer, dealer_probs):
    '''
    Returns the probability of winning if player stands
    '''
    return probability_of_winning(hand, dealer_probs)

def basic_split(shoe, hand, dealer, dealer_probs):
    '''
    Returns the probability of winning a hand if chosen action is split
    I don't think I need to simulate both hands, they are identical
    there will be a slight change in shoe dynamics after playing the first hand
    but it shouldn't matter too much
    '''

    win = 0

    for rank in Rank:
        new_hand = deepcopy(hand)
        new_hand.split_hand()
        new_hand.add_card(Card(rank, Suit.Spade))
        win += probability_of_card(shoe, Card(rank, Suit.Spade))*basic_stand(new_hand, dealer, dealer_probs)
    return win

def complete_hit(shoe, hand, dealer, index, dealer_probs):
    '''
    Returns the probability of winning a hand if action is to hit
    '''

    win = 0

    # busted
    if hand.value > 21:
        return 0

    # Hand is already perfect no need to hit - hitting would not necessarily make you lose but there's no advantage
    elif hand.blackjack:
        return 0

    elif hand.value == 21:
        hand_prob = probability_of_hand(shoe, hand, index)
        win_prob = basic_stand(hand, dealer, dealer_probs)
        win += hand_prob*win_prob
        return win

    # special rule that you can't hit after splitting aces
    elif hand.split_aces:
        hand_prob = probability_of_hand(shoe, hand, 1)
        win_prob = basic_stand(hand, dealer, dealer_probs)
        win += hand_prob*win_prob
        return win

    #This is the 6 card charlie rule, you automatically win
    elif hand.value <= 21 and len(hand.cards) >= 6:
        prob = probability_of_hand(shoe, hand, index)
        return prob # charlies win 100% of the time they are dealt

    # For each rank we could draw after hitting
    if len(hand.cards) == index:
        for rank in range(Rank(0), Rank.King + 1):
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(Rank(rank), Suit.Spade))

            win += complete_hit(shoe, new_hand, dealer, index, dealer_probs)
    else:
        for rank in range(hand.cards[-1].rank, Rank.King + 1):
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(Rank(rank), Suit.Spade))

            win += complete_hit(shoe, new_hand, dealer, index, dealer_probs)

    if len(hand.cards) > index:
        hand_prob = probability_of_hand(shoe, hand, index)
        win_prob = basic_stand(hand, dealer, dealer_probs)
        win += hand_prob*win_prob

    return win

def complete_double(shoe, hand, dealer_probs):
    '''
    Returns the probability of winning a hand if action is to double down
    '''

    #This function can NOT be called if hand consist of more than 2 cards
    #assert(len(hand.cards) == 2)
    #this function should not be called if hand value is 21 or busted
    #assert(hand.value < 21)

    win = 0

    # Hand is already perfect no need to hit - hitting would not necessarily make you lose but there's no advantage
    if hand.blackjack:
        return 0

    if hand.value == 21:
        hand_prob = probability_of_hand(shoe, hand, index)
        win_prob = basic_stand(hand, dealer, dealer_probs)
        win += hand_prob*win_prob
        return win

    # For each rank we could draw after doubling down
    # goal is to find what percentage of time we win vs lose
    for rank in Rank:
        new_hand = deepcopy(hand)
        new_hand.add_card(Card(rank, Suit.Spade))

        prob = probability_of_card(shoe, Card(rank, Suit.Spade))

        win+=prob*probability_of_winning(new_hand, dealer_probs)

    return win

def complete_split(shoe, hand, dealer):
    '''
    Returns the probability of winning a hand if chosen action is split
    I don't think I need to simulate both hands, they are identical in expectation
    there will be a slight change in shoe dynamics after playing the first hand
    but it shouldn't matter enough to warrant double the computation
    '''
    dealer_probs = dealer.dealer_outcome_probs()

    hand.split_hand() # Split hand - removes a card
    win = 0

    for rank in Rank:
        new_hand = deepcopy(hand)
        new_hand.add_card(Card(rank, Suit.Spade)) # adds a second card (auto hit)
        win += complete_hit(shoe, new_hand, dealer, 1, dealer_probs) # then calls hit to run all simulations after hit

    return win
