from hand import Hand
from card import Card, Rank, Suit
from shoe import Shoe
from copy import deepcopy
import probability, random
from constants import Dealer_Outcome
import numpy

class Dealer():

    dealer_outcome_probs_infinite = numpy.array([   [0.13078889978591976, 0.13078889978591976, 0.13078889978591976, 0.13078889978591976, 0.05386582286284283, 0.3076923076923077, 0.11528627030116942],
                                                    [0.13980913952773533, 0.13490735037469442, 0.12965543342500774, 0.12402645577124097, 0.11799348450595983, 0, 0.3536081363953539],
                                                    [0.13503398781114, 0.13048232645474486, 0.12558053730170396, 0.12032862035201726, 0.11469964269825049, 0, 0.3738748853821393],
                                                    [0.1304897358495983, 0.12593807449320316, 0.12138641313680804, 0.11648462398376716, 0.11123270703408046, 0, 0.3944684455025419],
                                                    [0.12225128527055074, 0.12225128527055078, 0.11769962391415566, 0.11314796255776056, 0.10824617340471966, 0, 0.41640366958226205],
                                                    [0.16543817650334652, 0.10626657887021022, 0.10626657887021022, 0.10171491751381516, 0.09716325615742008, 0, 0.42315049208499683],
                                                    [0.3685661937942386, 0.137796963025008, 0.0786253653918717, 0.0786253653918717, 0.07407370403547664, 0, 0.262312408361533],
                                                    [0.12856654444917, 0.3593357752184008, 0.12856654444917012, 0.06939494681603388, 0.06939494681603389, 0, 0.24474124225119132],
                                                    [0.11999544148589202, 0.11999544148589202, 0.3507646722551228, 0.1199954414858921, 0.06082384385275591, 0, 0.22842515943444525],
                                                    [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.3421935692918448, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918],
                                                    [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.3421935692918448, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918],
                                                    [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.3421935692918448, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918],
                                                    [0.11142433852261402, 0.11142433852261402, 0.11142433852261402, 0.3421935692918448, 0.03450126159953709, 0.07692307692307693, 0.21210907661769918]])

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

    def playout_hand(self):
        # Assumes infinite deck

        while self.hand.sum < self.stand_min:
            card = Card(Rank(random.randint(Rank.Ace, Rank.King)), Suit.Spade)
            self.hand.add_card(card)

        return self.hand.sum

    def outcome_probs(self):
        return Dealer.dealer_outcome_probs_infinite[int(self.hand.cards[0].rank)]

    def calculate_outcome_probs(self):
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

        Assumes infinite shoe
        '''
        value = hand.sum
        index = 1 # always 1 since we knew the dealer's single up card prior

        # dealer reached stopping condition add the probability of getting this hand to list
        if value > self.stand_min or (value == self.stand_min and not self.hit_soft):

            #Dealer has BJ
            if hand.blackjack:
                self.dealer_outcome_probabilities[Dealer_Outcome.BJ] += probability.prob_cards(hand, index)

            #Dealer busted
            elif value > 21:
                self.dealer_outcome_probabilities[Dealer_Outcome.BUST] += probability.prob_cards(hand, index)

            #Dealer has 21 but not BJ
            elif value == 21:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_21] += probability.prob_cards(hand, index)

            elif value == 20:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_20] += probability.prob_cards(hand, index)

            elif value == 19:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_19] += probability.prob_cards(hand, index)

            elif value == 18:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_18] += probability.prob_cards(hand, index)

            elif value == 17:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_17] += probability.prob_cards(hand, index)

            return

        # otherwise dealer hits
        else:
            # need to hit dealer with every possible rank to explore all possible outcomes
            for rank in Rank:
                new_hand = deepcopy(hand)
                new_hand.add_card(Card(rank, Suit.Spade)) # suit is arbitrary
                self.__dealer_outcome_probs(new_hand)

        return # end
