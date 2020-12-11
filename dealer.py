from hand import Hand
from card import Card, Rank, Suit
from shoe import Shoe
from copy import deepcopy
import probability

class Dealer():

    # Dealer defaults to the strategy I need for my application
    def __init__(self, shoe, stand=17, hit_soft=False):
        # Dealer's strategy can be defined here
        self.hand = None
        self.up_card = None
        self.shoe = shoe
        self.stand_min = stand # What's the minimum value the dealer stands on?
        self.hit_soft = hit_soft # does dealer hit on the soft min standing hand value ?
        self.dealer_outcome_probabilities = [0]*7

    def deal_card(self, card):
        '''
        Deals the dealer their up facing card
        '''
        self.up_card = card
        self.hand = Hand([card])

    def reset(self):
        '''
        Resets the dealer's hand
        '''
        self.hand = None
        self.up_card = None

    def dealer_outcome_probs(self):
        '''
        Returns the probabilities of possible outcomes for the dealer
        '''

        # dealer needs to have a hand to perform request
        # also check if it needs to be performed again
        if self.hand is not None:
            self.dealer_outcome_probabilities = [0]*7
            self.__dealer_outcome_probs(self.hand)

            return self.dealer_outcome_probabilities
        else:
            print("No dealer hand provided")
            return None

    def __dealer_outcome_probs(self, hand):
        '''
        Generates the probabilities of all possible outcomes for the dealer by
        playing out the dealer's hand according to the dealer's pre-defined strategy

        There are 7 possible hand outcomes and they are stored in dealer_probabilities
        p[0] = P(hand_value == 17)
        p[1] = P(hand_value == 18)
        p[2] = P(hand_value == 19)
        p[3] = P(hand_value == 20)
        p[4] = P(hand_value == 21)
        p[5] = P(hand_value == BJ) # 21 with only 2 cards
        p[6] = P(hand_value > 21) # busted
        '''
        value = hand.value
        index = 1 # always 1 since once the dealer starts playing we have no control

        # dealer reached stopping condition add the probability of getting this hand to list
        if value > self.stand_min or (value == self.stand_min and not self.hit_soft):

            #Dealer has BJ
            if hand.blackjack:
                self.dealer_outcome_probabilities[5] += probability.probability_of_hand(self.shoe, hand, index)

            #Dealer busted
            elif value > 21:
                self.dealer_outcome_probabilities[6] += probability.probability_of_hand(self.shoe, hand, index)

            #Dealer has some value between 17 and 21 but not BJ
            else:
                self.dealer_outcome_probabilities[value-17] += probability.probability_of_hand(self.shoe, hand, index)

            return # base condition return

        # otherwise dealer hits
        else:
            # need to hit dealer with every possible rank to explore all possible outcomes
            for rank in Rank:
                new_hand = deepcopy(hand)
                new_hand.add_card(Card(rank, Suit.Spade)) # suit is arbitrary
                self.__dealer_outcome_probs(new_hand)

        return # end
