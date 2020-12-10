'''
Need this to be fully automated in terms of decision making

0. What is my chance of winning the next hand?
1. Do I bet? (I guess anytime it's greater than 50% I should bet)
2. How much do I bet? (Kelly criterion?) utility function?
3. What is my next action

Other considerations
-Side bets
-Should I take insurance?
-I think I'll ignore suits all together for now as they only affect some of the side bets
'''

from card import Card, Rank, Suit
from hand import Hand
import copy

class Shoe():
    '''
    Maintains statistics about the shoe
    '''
    def __init__(self, decks):
        # should probably add rules about game here
        self.DECKS = decks
        self.cards_in_shoe = 52*self.DECKS
        self.ranks_left = [4*self.DECKS]*13 # how many cards of each rank remains in the shoe
        self.r_count = 0 # running count

    def draw_probability(self, card):
        '''
        Returns the probability that the next card drawn from the shoe will be 'card'
        '''
        return self.ranks_left[card.rank]/self.cards_in_shoe

    def running_count(self):
        '''
        Returns the 'running count' of the shoe as defined by the Hi-Lo System
        '''
        return self.r_count

    def true_count(self):
        '''
        Returns the 'true count' of the shoe as defined by the Hi-Lo system
        Essentially it is a measure of how biased the shoe is to have low or
        high cards

        A true count > 0 indicates the deck has more high cards
        A true count < 0 indicates the deck has more low cards
        '''
        return self.r_count/(self.cards_in_shoe/52)

    def draw(self, card):
        '''
        This function draws 'card' from the shoe and updates the shoe's
        statistics

        Must call this function to keep shoe statistics up to date
        '''

        self.cards_in_shoe-=1
        self.ranks_left[card.rank]-=1
        self.r_count+=card.cc_value()

        # post conditions
        assert(self.cards_in_shoe > 0)
        assert(self.ranks_left[card.rank] > 0)

    def __add_card(self, card):
        '''
        Allows us to add a card back into the shoe. This is used to undo the
        effects simulations have on the shoe statistics
        '''
        self.cards_in_shoe+=1
        self.ranks_left[card.rank]+=1
        self.r_count-=card.cc_value()

    def optimal_strategy(self):
        '''
        Returns the optimal strategy based on the statistics of the shoe
        '''
        # should verify optimal strategy with basic strategy.
        pass

    def optimal_action(self, hand, dealer_card):
        '''
        Returns the optimal action based on the statistics of the shoe,
        the player's hand and the dealer's card
        '''
        # should verify optimal strategy with basic strategy.
        # of the valid actions which has the greatest reward


        actionEV = [0]*4 # Is the expected value from taking each action

        self.__actions(hand, dealer, actionEV)


        # check if these actions are valid and then search the entire subtree

    def __actions(self, hand, dealer, actionEV):

        #Here we have to run all possible actions given a state

        hand_value = hand.blackjack_value()

        # player busted
        if hand_value > 21:
            return -1

        # have BJ
        elif hand.blackjack and not hand.double:
            #playout dealer
            pass

        # 21 not a BJ
        elif hand_value == 21 and not hand.blackjack and not hand.double:
            #playout dealer
            pass

        # Any other value
        elif hand_value < 21:
            # When hit is possible it runs all possible outcomes of hitting
            if not hand.double:
                new_hand = hand(hand.hand)
                for card in Card:
                    new_hand.add_card(card)
                    __actions(new_hand, dealer, actionEV)

            # Option to double down
            elif len(hand.hand) == 2:
                    new_hand = hand(hand.hand)
                    new_hand.double = True
                    for card in Card:
                        new_hand.add_card(card)
                        __actions(new_hand, dealer, actionEV)



        else:
            print("There shouldn't be any other cases. Bug")

        #if split:

    def double_down(self, hand, dealer):
        '''
        Returns the probability of winning a hand if action is to double down
        '''

        win = 0

        #Double check we can and 'should' double
        if len(hand.hand) == 2 and hand.value < 21:

            dealer_probs = [0]*7
            self.dealer_playout(dealer, dealer_probs) # By calculating this once we greatly reduce computation but lose a bit of accuracy

            # For each rank we could draw after doubling down
            # goal is to find what percentage of time we win vs lose
            for rank in Rank:
                new_hand = Hand(copy.deepcopy(hand.hand))
                new_hand.double = True
                new_hand.add_card(Card(rank, Suit.Spade))

                prob = self.draw_probability(Card(rank, Suit.Spade)) # removing a card ! need to add back

                win+=prob*self.win_prob(new_hand, dealer_probs)

                self.__add_card(Card(rank, Suit.Spade)) # add card back into shoe
                #print(f"Win prob {round(self.win_prob(new_hand, dealer_probs)*100, 2)}% with a {new_hand.value}")

        return win

    def win_prob(self, hand, d):
        '''
        Returns the probability of winning with a hand against all possible
        outcomes of the dealer. P(win) + P(lose) = 1. I believe so by calculating
        probabilty of winning we also get losing probability
        '''
        value = hand.value
        win = 0

        if value > 21:
            return win

        elif hand.blackjack:
            win = sum(d) - d[5]/2# it's a push if both have BJ so I think divided in 2 is equivalent

        elif value == 21:
            win = sum(d) - (d[4]/2) - d[5] # here we have 21 so we push against 21, lose to dealer's BJ and win all other times
        #Any hand that didn't bust and is not blackjack
        else:
            for x in range(len(d)-3):
                if value > x + 17:
                    win += d[x]
                elif value == x + 17:
                    win += (d[x]/2)
            win += d[6] #Beats all busted hands

        return win

    def dealer_playout(self, dealers_hand, probabilities):
        '''
        Plays out the dealer's hand according to a specific set of rules dependent
        on the casino. While simultaneously building a list of probabilities of
        the different outcomes for the dealer

        There are 7 possible outcomes for the dealer and are stored in the prob. list
        p[0] = P(hand_value == 17)
        p[1] = P(hand_value == 18)
        p[2] = P(hand_value == 19)
        p[3] = P(hand_value == 20)
        p[4] = P(hand_value == 21)
        p[5] = P(hand_value == BJ) # 21 with only 2 cards
        p[6] = P(hand_value > 21) # busted
        '''
        value = dealers_hand.value
        index = 1

        # Dealer reached stopping condition
        if value >= 17:

            #Dealer has BJ
            if dealers_hand.blackjack:
                probabilities[5] += self.probability_of_hand(dealers_hand, index)

            #Dealer busted
            elif value > 21:
                probabilities[6] += self.probability_of_hand(dealers_hand, index)

            #Dealer has some value between 17 and 21 but not BJ
            else:
                probabilities[value-17] += self.probability_of_hand(dealers_hand, index)

            return probabilities

        #Another card needs to be drawn for the dealer
        else:
            for rank in Rank:
                new_hand = Hand(copy.deepcopy(dealers_hand.hand))
                new_hand.add_card(Card(rank, Suit.Spade)) # suit is arbitrary
                self.dealer_playout(new_hand, probabilities)

        return probabilities

    def probability_of_hand(self, hand, index):
        '''
        This returns the probability of drawing a specific hand starting with some
        card(s) given by the index.
        '''
        self.cards_in_shoe

        # make copies so that variables can be set back to orginal values after calculations
        copy_cards_in_shoe = self.cards_in_shoe
        copy_ranks_left = copy.deepcopy(self.ranks_left)

        prob = 1

        for card in range(index, len(hand.hand)):
            prob*=self.draw_probability(hand.hand[card])
            self.draw(hand.hand[card])

        # reinstate original shoe statistic values
        self.cards_in_shoe = copy_cards_in_shoe
        self.ranks_left = copy_ranks_left

        return prob
