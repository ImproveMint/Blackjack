'''
game.py contains all the information for a given round of blackjack to playout

-Dealer's upcard
-Shoe
-Player's hand(s)
'''
from hand import Hand
from card import Card, Rank, Suit
from shoe import Shoe
from copy import deepcopy
import probability, random
from constants import Dealer_Outcome

class Game():
    def __init__(self, hand, upcard, shoe=None, stand=17, hit_soft=False):
        self.shoe = shoe
        self.hand = None
        self.upcard = None
        self.dealer = None

        # Table Rules
        self.stand_min = 17 # the minimum value the dealer stands on
        self.hit_soft = hit_soft # does dealer hit soft 17
        self.DaS = False # Double after Split not implemented
        self.SaS = False # Split after split not implemented
        self.HSA = False # Hit split aces not implemented
        self.charlie = 6 # auto win if your hand consist of this many cards and haven't busted not implemented

        self.dealer_outcome_probabilities = [0]*7
        self.update_needed = True

        self.new_game(hand, upcard)

    def new_game(self, hand, upcard):
        '''
        Resets the game, deals a new hand
        '''
        self.hand = hand
        self.upcard = upcard
        self.dealer = Hand([upcard])
        self.dealer.index = 1;

        if self.shoe is not None:
            self.shoe.draw_hand(hand)
            self.shoe.draw_card(upcard)
            self.update_needed = True
            self.calculate_outcome_probs()

    def playout_dealer(self):
        # Assumes infinite deck

        while self.hand.sum < self.stand_min:
            card = Card(Rank(random.randint(Rank.Ace, Rank.King)), Suit.Spade)
            self.hand.add_card(card)

        return self.hand.sum

    def calculate_outcome_probs(self):
        '''
        Returns the probabilities of possible outcomes for the dealer
        '''
        if self.update_needed:
            self.dealer_outcome_probabilities = [0]*7
            copy = deepcopy(self.dealer)
            self.__dealer_outcome_probs(copy)
            self.update_needed = False
            print(sum(self.dealer_outcome_probabilities))

        return self.dealer_outcome_probabilities

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
        value = hand.sum
        index = 1 # always 1 since we knew the dealer's single up card prior

        # dealer reached stopping condition add the probability of getting this hand to list
        if value > self.stand_min or (value == self.stand_min and not self.hit_soft) : # by not exploring hands with > 5 cards we save significant computation for events that extremely unlikely. In this case 99.9% of hands are still accounted for if we do > 4 then 99% of hands are accounted for and it's much faster

            #Dealer has BJ
            if hand.blackjack:
                self.dealer_outcome_probabilities[Dealer_Outcome.BJ] += probability.prob_cards(hand, self.shoe)

            #Dealer busted
            elif value > 21:
                # print(f"DO {hand} index {hand.index} len {len(hand.cards)} prob {probability.prob_cards(hand, self.shoe)}")
                self.dealer_outcome_probabilities[Dealer_Outcome.BUST] += probability.prob_cards(hand, self.shoe)

            #Dealer has 21 but not BJ
            elif value == 21:
                # print(f"DO {hand} index {hand.index}")
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_21] += probability.prob_cards(hand, self.shoe)

            elif value == 20:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_20] += probability.prob_cards(hand, self.shoe)

            elif value == 19:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_19] += probability.prob_cards(hand, self.shoe)

            elif value == 18:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_18] += probability.prob_cards(hand, self.shoe)

            elif value == 17:
                self.dealer_outcome_probabilities[Dealer_Outcome.SUM_17] += probability.prob_cards(hand, self.shoe)

            return

        # otherwise dealer hits
        else:
            # need to hit dealer with every possible rank to explore all possible outcomes
            for rank in Rank:
                new_hand = deepcopy(hand)
                new_hand.add_card(Card(rank, Suit.Spade)) # suit is arbitrary
                self.__dealer_outcome_probs(new_hand)

        return # end

    def __deepcopy__(self, memo):
        cls = self.__class__ # Extract the class of the object
        result = cls.__new__(cls) # Create a new instance of the object based on extracted class
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))

        return result
