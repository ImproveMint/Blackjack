'''
This class calculates useful probabilities for the game of blackjack
'''

from copy import deepcopy
from card import Card, Rank, Suit
from hand import Hand
from shoe import Shoe
from constants import Action, Outcome

def prob_card(card, shoe=None):
    '''
    Returns the probability of drawing a certain card from the shoe.
    If no shoe is provided then it returns the probability assuming infinite deck
    '''
    prob = 1/13 # infinite deck/shoe
    if shoe is not None:
        prob = shoe.ranks_left[card.rank]/shoe.cards_in_shoe
    assert(prob >= 0)
    return prob

def prob_cards(hand, index=0, shoe=None):
    '''
    Returns the probability of drawing some permutation of cards.
    Eg the probability of drawing an ace and then a king is (4/52)*(4/51) for a single deck shoe.
    If an index is provided it will ignore the cards that are before the index.

    Assumes cards have not already been drawn from shoe! That is because this
    function's purpose is to simulate different outcomes.
    '''

    prob = 1 #intial probability of 1 and is updated as we go

    # assumes with replacement, not ideal but might be close enough
    if shoe == None:
        for card in range(index, len(hand.cards)):
            prob*=prob_card(hand.cards[card])

    # if shoe is provided then it takes into account removal effects
    else:
        # make copy so we don't change original shoe probabilities
        shoe_copy = deepcopy(shoe)

        for card in range(index, len(hand.cards)):
            prob*=prob_card(hand.cards[card], shoe_copy)
            shoe_copy.draw(hand.cards[card])

    assert(prob >= 0)

    return prob

def prob_outcomes(hand, dealer_probs):
    '''
    Returns the probability of winning, drawing and losing a hand against all
    possible hand combinations for the dealers

    To call this function player needs a hand and dealer needs an up card
    '''
    outcomes = [0, 0, 0] # Win | Draw | Lose , respectively
    value = hand.sum # lookup once to save time

    # Player busted
    if value > 21:
        outcomes[Outcome.LOSE] = 1 # Lose 100% of the time

    # Player has BJ and so only pushes against a dealer's BJ
    elif hand.blackjack:
        outcomes[Outcome.WIN] = sum(dealer_probs) - dealer_probs[5] # Win's against all dealer's hands expect when dealer has BJ
        outcomes[Outcome.PUSH] = dealer_probs[5] # push against BJ

    # Player has 21 but not BJ
    elif value == 21:
        outcomes[Outcome.WIN] = sum(dealer_probs) - (dealer_probs[4]) - dealer_probs[5] # here we have 21 so we push against 21, lose to dealer's BJ and win all other times
        outcomes[Outcome.PUSH] = dealer_probs[4] # push against 21
        outcomes[Outcome.LOSE] = dealer_probs[5] # lose against BJ

    #Any hand that didn't bust, is not BJ nor 21
    else:
        for x in range(len(dealer_probs)-3):
            if value > x + 17:
                outcomes[Outcome.WIN] += dealer_probs[x]
            elif value == x + 17:
                outcomes[Outcome.PUSH] += dealer_probs[x]
            else:
                outcomes[Outcome.LOSE] += dealer_probs[x]

        outcomes[Outcome.WIN] += dealer_probs[6] # and beats dealer's busted hands
        outcomes[Outcome.LOSE] += dealer_probs[4] + dealer_probs[5] # loses against BJ and 21

    assert(round(sum(outcomes),2) == 1) # probabilities of all different outcomes should add to 1

    return outcomes

def single_action_rewards(hand, dealer):
    '''
    Returns the EV for each possible move looking one step into the future.
    I believe this is how basic strategy was created.
    '''

    dealer_probs = dealer.dealer_outcome_probs()
    expected_value = [0, 0, 0, 0] # hit | stand | double | split

    hit = basic_hit(hand, dealer, len(hand.cards), dealer_probs)
    expected_value[Action.HIT] = hit

    stand = basic_stand(hand, dealer_probs)
    expected_value[Action.STAND] = stand

    double = 2*hit # 1 action look ahead makes double and hit the same action
    expected_value[Action.DOUBLE] = double

    if hand.can_split():
        split = 2*basic_split(hand, dealer, dealer_probs)
        expected_value[Action.SPLIT] = split
        # print(f"SPLIT {round(100*split,2)}% ", end="")

    # print("")

    print(expected_value)

    return expected_value

def __get_expected_reward(hand, dealer_probs, index):
    discount = 1 # 0.1**(len(hand.cards)-index)
    probability_of_hand = prob_cards(hand, index)
    outcome_probabilities = prob_outcomes(hand, dealer_probs)

    return probability_of_hand*(outcome_probabilities[Outcome.WIN] - outcome_probabilities[Outcome.LOSE])*discount

def basic_hit(hand, index, dealer_probs):
    '''
    Returns the probability of winning if player hits

    This function looks a single step ahead. IE It hits and then regardless
    of the value of the hand it stands and plays out the dealer
    '''

    expected_reward = 0

    # Hand is already perfect no need to hit - hitting would not necessarily
    # make you lose but there's no advantage so we return a lose
    if hand.blackjack:
        return -1

    elif hand.sum == 21:
        return __get_expected_reward(hand, dealer_probs, index)

    # the hand is hit with each possible card rank
    for rank in Rank:
        new_hand = deepcopy(hand)
        new_hand.add_card(Card(rank, Suit.Spade)) # arbitrary suit
        expected_reward += __get_expected_reward(new_hand, dealer_probs, index)

    return expected_reward

def basic_stand(hand, dealer_probs):
    '''
    Returns the probability of winning if player stands
    '''
    outcome_probs = prob_outcomes(hand, dealer_probs)

    return outcome_probs[Outcome.WIN] - outcome_probs[Outcome.LOSE]

def basic_split(hand, dealer, dealer_probs):
    '''
    Returns the probability of winning a hand if chosen action is split
    I don't think I need to simulate both hands, they are identical
    there will be a slight change in shoe dynamics after playing the first hand
    but it shouldn't matter too much
    '''

    expected_reward = 0

    for rank in Rank:
        new_hand = deepcopy(hand)
        new_hand.split_hand()
        new_hand.add_card(Card(rank, Suit.Spade))
        expected_reward += __get_expected_reward(new_hand, dealer_probs, 1)
    return expected_reward

def complete_action_rewards(hand, dealer):

    dealer_probs = dealer.outcome_probs()
    print(dealer_probs)

    assert(round(sum(dealer_probs),2) == 1.00)

    expected_reward = [-1, -1, -1, -1] # hit | stand | double | split

    # Can not hit if you have blackjack
    if hand.blackjack:
        expected_reward[Action.HIT] = -1
    else:
        hit = complete_hit(hand, dealer, len(hand.cards), dealer_probs)
        expected_reward[Action.HIT] = hit

    stand = basic_stand(hand, dealer_probs) # stand is same in every case
    expected_reward[Action.STAND] = stand

    double = complete_double(hand, dealer_probs)
    expected_reward[Action.DOUBLE] = double

    print(expected_reward)

    return expected_reward

def complete_hit(hand, dealer, index, dealer_probs):
    '''
    Returns the probability of winning a hand if action is to hit
    '''

    win = 0

    # busted
    if hand.sum > 21:
        return __get_expected_reward(hand, dealer_probs, index)

    elif hand.sum == 21:
        return __get_expected_reward(hand, dealer_probs, index)

    # special rule that you can't hit after splitting aces
    elif hand.split_aces:
        return __get_expected_reward(hand, dealer_probs, 1)

    #This is the 6 card charlie rule, you automatically win
    elif hand.sum <= 21 and len(hand.cards) >= 6:
        prob = prob_cards(hand, index)
        return prob # charlies win 100% of the time they are dealt

    # For each rank we could draw after hitting
    if len(hand.cards) == index:
        for rank in range(Rank(0), Rank.King + 1):
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(Rank(rank), Suit.Spade))

            win += complete_hit(new_hand, dealer, index, dealer_probs)
    else:
        for rank in range(hand.cards[-1].rank, Rank.King + 1):
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(Rank(rank), Suit.Spade))

            win += complete_hit(new_hand, dealer, index, dealer_probs)

    if len(hand.cards) > index:
        win += __get_expected_reward(hand, dealer_probs, index)

    return win

def complete_double(hand, dealer_probs):
    '''
    Returns the probability of winning a hand if action is to double down
    '''
    return 2*basic_hit(hand, 2, dealer_probs)

def complete_split(hand, dealer):
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
        win += complete_hit(new_hand, dealer, 1, dealer_probs) # then calls hit to run all simulations after hit

    return win
