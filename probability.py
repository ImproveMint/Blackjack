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

    Assumes cards have not been drawn from shoe! That is because this
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

def action_ev(hand, dealer, shoe=None):
    '''
    Returns the expected value/reward of each possible action given a hand and the
    dealer's upcard

    Assumptions: Infinite shoe
    '''

    dealer_probs = dealer.outcome_probs()

    #Initialized to a value that will never be chosen IE must be updated
    expected_reward = [-2, -2, -2, -2] # hit | stand | double | split

    # Can not hit if you have blackjack
    if hand.can_hit():
        expected_reward[Action.HIT] = hit(hand, len(hand.cards), dealer_probs)

    # Can always stand
    expected_reward[Action.STAND] = stand(hand, dealer_probs)

    if hand.can_double():
        expected_reward[Action.DOUBLE] = double(hand, dealer_probs)

    if hand.can_split():
        expected_reward[Action.SPLIT] = split(hand, dealer_probs)

    return expected_reward

def hit(hand, index, dealer_probs):
    '''
    Returns the expected reward/value of hitting

    Assumptions:    Infinite shoe
    '''
    ev = 0

    # Hit the hand with every rank in the deck Ace through King
    for rank in Rank:
        new_hand = deepcopy(hand)
        card = Card(rank, Suit.Spade)
        new_hand.add_card(card)

        # 4 cases:
        # Hit busted hand
        if new_hand.sum > 21:
            # print("BUST")
            # print(new_hand)
            ev += prob_cards(new_hand, index)*-1

        # Hit made hand 21
        elif new_hand.sum == 21:
            # print("21!")
            # print(new_hand)
            ev += __expected_reward(new_hand, dealer_probs, index)

        # 6 card charlie rule
        elif len(new_hand.cards) >= 6:
            # print("Charlie!")
            # print(new_hand)
            ev += prob_cards(new_hand, index)

        # Hit results in another decision - explore better option (recursive)
        elif not hand.double and not hand.split_aces:
            # from here we can either hit or stand and we want the better of the 2
            # print("New action!")
            # print(new_hand)
            ev += max(hit(new_hand, index+1, dealer_probs), stand(new_hand, dealer_probs))*prob_card(card)

        # Hit results in another decision but only decision avaiable is to stand
        else:
            # print("Standing")
            # print(new_hand)
            ev += stand(new_hand, dealer_probs)*prob_card(card)

    return ev

def stand(hand, dealer_probs):
    '''
    Returns the expected reward/value of standing
    '''
    return __expected_reward(hand, dealer_probs, len(hand.cards))

def double(hand, dealer_probs):
    '''
    Returns the expected reward/value of doubling down
    '''
    hand.double_down()
    ev = 2*hit(hand, 2, dealer_probs)
    hand.double = False
    return ev

def split(hand, dealer_probs):
    '''
    Returns the expected reward/value of splitting
    '''
    hand.split_hand() # Split hand - removes a card

    ev = 2*hit(hand, 1, dealer_probs) # then calls hit to run all simulations after hit
    hand.add_card(hand.cards[0])
    return ev

def __expected_reward(hand, dealer_probs, index):
    '''
    Returns the combined expected value of a hand against all possible outcomes
    of the dealer
    '''
    probability_of_hand = prob_cards(hand, index)
    outcome_probabilities = prob_outcomes(hand, dealer_probs)

    return probability_of_hand*(outcome_probabilities[Outcome.WIN] - outcome_probabilities[Outcome.LOSE])
