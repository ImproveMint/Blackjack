'''
This class calculates useful probabilities for the game of blackjack
'''
from copy import deepcopy
from card import Card, Rank, Suit
from hand import Hand
from shoe import Shoe
from constants import Action, Outcome
import numpy

dealer_inf_probs = numpy.array([[0.13078889978591976, 0.13078889978591976, 0.13078889978591976, 0.13078889978591976, 0.05386582286284283, 0.30769230769230770, 0.11528627030116942], # Ace
                                [0.13980913952773533, 0.13490735037469442, 0.12965543342500774, 0.12402645577124097, 0.11799348450595983, 0.00000000000000000, 0.35360813639535390], # Two
                                [0.13503398781114000, 0.13048232645474486, 0.12558053730170396, 0.12032862035201726, 0.11469964269825049, 0.00000000000000000, 0.37387488538213930],
                                [0.13048973584959830, 0.12593807449320316, 0.12138641313680804, 0.11648462398376716, 0.11123270703408046, 0.00000000000000000, 0.39446844550254190],
                                [0.12225128527055074, 0.12225128527055078, 0.11769962391415566, 0.11314796255776056, 0.10824617340471966, 0.00000000000000000, 0.41640366958226205],
                                [0.16543817650334652, 0.10626657887021022, 0.10626657887021022, 0.10171491751381516, 0.09716325615742008, 0.00000000000000000, 0.42315049208499683],
                                [0.36856619379423860, 0.13779696302500800, 0.07862536539187170, 0.07862536539187170, 0.07407370403547664, 0.00000000000000000, 0.26231240836153300],
                                [0.12856654444917000, 0.35933577521840080, 0.12856654444917012, 0.06939494681603388, 0.06939494681603389, 0.00000000000000000, 0.24474124225119132],
                                [0.11999544148589202, 0.11999544148589202, 0.35076467225512280, 0.11999544148589210, 0.06082384385275591, 0.00000000000000000, 0.22842515943444525],
                                [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.34219356929184480, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918],
                                [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.34219356929184480, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918],
                                [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.34219356929184480, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918],
                                [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.34219356929184480, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918]])

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

def prob_cards(hand, shoe=None):
    '''
    Returns the probability of drawing some permutation of cards.
    Eg the probability of drawing an ace and then a king is (4/52)*(4/51) for a single deck shoe.
    If an index is provided it will ignore the cards that are before the index.

    Assumes cards have not been drawn from shoe! That is because this
    function's purpose is to simulate different outcomes.
    '''

    prob = 1 #intial probability of 1 and is updated as we go

    # if no shoe is provided assume infinite shoe
    if shoe == None:
        for card in range(hand.index, len(hand.cards)):
            prob*=prob_card(card)

    # if shoe is provided then take into account removal effects
    else:
        # make copy so we don't change original shoe probabilities
        shoe_copy = deepcopy(shoe)

        for card in range(hand.index, len(hand.cards)):
            prob*=prob_card(hand.cards[card], shoe)
            shoe_copy.draw_card(hand.cards[card])

    assert(prob >= 0)

    return prob

def prob_outcomes(game):
    '''
    Returns the probability of winning, drawing and losing a hand against all
    possible hand combinations for the dealers

    To call this function player needs a hand and dealer needs an up card
    '''

    # If no shoe provided assume infinite deck
    if game.shoe is None:
        dealer_probs = dealer_inf_probs[int(game.upcard.rank)]
    else:
        dealer_probs = game.calculate_outcome_probs()

    outcomes = [0, 0, 0] # Win | Draw | Lose , respectively
    value = game.hand.sum # lookup once to save time

    # Player busted
    if value > 21:
        outcomes[Outcome.LOSE] = 1 # Lose 100% of the time

    # Player has BJ and so only pushes against a dealer's BJ
    elif game.hand.blackjack:
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

    # assert(round(sum(outcomes),2) == 1) # probabilities of all different outcomes should add to 1
    return outcomes

def action_ev(game):
    '''
    Returns the expected value/reward of each possible action given a hand and the
    dealer's upcard
    '''

    game_copy = deepcopy(game) # copy game to run different situations

    #Initialized to a value that will never be chosen IE must be updated
    expected_reward = [-2, -2, -2, -2] # hit | stand | double | split

    # Can not hit if you have blackjack
    if game_copy.hand.can_hit():
        #print("################################ HIT ##############################################")
        expected_reward[Action.HIT] = hit(game_copy)

    # Can always stand
    #print("################################ STAND ##############################################")
    expected_reward[Action.STAND] = stand(game_copy)

    if game_copy.hand.can_double():
        #print("################################ DOUBLE ##############################################")
        expected_reward[Action.DOUBLE] = double(game_copy)

    if game_copy.hand.can_split():
        #print("################################ SPLIT ##############################################")
        expected_reward[Action.SPLIT] = split(game_copy)

    return expected_reward

def hit(game):
    '''
    Returns the expected reward/value of hitting

    Assumptions:    Infinite shoe
    '''
    ev = 0

    # Hit the hand with every rank in the deck Ace through King
    for rank in Rank:
        new_game = deepcopy(game)
        card = Card(rank, Suit.Spade)
        new_game.hand.add_card(card)

        # 5 cases:
        # Case 1: 6 card charlie rule
        if len(new_game.hand.cards) >= 6:
            e = prob_cards(new_game.hand, new_game.shoe)
            ev += e
            # print(f"Hand {new_game.hand} index '{new_game.hand.index}' CHARLIE {e}")

        # Case 2: Hit busted hand
        elif new_game.hand.sum > 21:
            e = prob_cards(new_game.hand, new_game.shoe)*-1
            ev += e
            # print(f"Hand {new_game.hand} index '{new_game.hand.index}' BUST {e}")

        # Case 3: Hit made hand 21
        elif new_game.hand.sum == 21:
            e = __expected_reward(new_game)
            ev += e
            # print(f"Hand {new_game.hand} index '{new_game.hand.index}' 21 {e}")

        # Case 4: Hit results in another decision - explore better option (recursive)
        elif not new_game.hand.double and not new_game.hand.split_aces:
            # from here we can either hit or stand and we want the better of the 2
            new_game.hand.index+=1
            h = hit(new_game)*prob_card(card)
            s = stand(new_game)*prob_card(card)
            # if h > s:
            #     print(f"Hand {new_game.hand} index '{new_game.hand.index}' Decision HIT {h}")
            # else:
            #     print(f"Hand {new_game.hand} index '{new_game.hand.index}' Decision STAND {s}")
            ev += max(h, s)


        # Cae 5: Hit results in another decision but only decision available is to stand
        # This is for doubles and ace splits
        else:
            e = stand(new_game)*prob_card(card)
            ev+= e
            # print(f"Hand {new_game.hand} index '{new_game.hand.index}' STAND {e}")

    return ev

def stand(game):
    '''
    Returns the expected reward/value of standing
    '''
    game.hand.index = len(game.hand.cards)
    return __expected_reward(game)

def double(game):
    '''
    Returns the expected reward/value of doubling down
    '''
    game.hand.double_down()
    ev = 2*hit(game)
    game.hand.double = False
    return ev

def split(game):
    '''
    Returns the expected reward/value of splitting
    '''
    game.hand.split_hand() # Split hand - removes a card

    ev = 2*hit(game) # then calls hit to run all simulations after hit
    game.hand.add_card(game.hand.cards[0])
    return ev

def __expected_reward(game):
    '''
    Returns the combined expected value of a hand against all possible outcomes
    of the dealer
    '''
    probability_of_hand = prob_cards(game.hand, game.shoe)
    outcome_probabilities = prob_outcomes(game)

    # print(f"Hand: {probability_of_hand}  coutcome prob {outcome_probabilities}")

    return probability_of_hand*(outcome_probabilities[Outcome.WIN] - outcome_probabilities[Outcome.LOSE])
