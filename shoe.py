'''
Need this to be fully automated in terms of decision making

0. What is my chance of winning the next hand?
1. Do I bet? (I guess anytime it's greater than 50% I should bet)
2. How much do I bet? (Kelly criterion?) utility function?
3. What is my next action

Other considerations
-Side bets
-Should I take insurance?
-I think I'll ignore suits all together for now as they only affect some of the side bets'
-Optimization can be made where 4 cards have the same value
'''

from card import Card, Rank, Suit
from hand import Hand
from copy import deepcopy

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
        self.dealer_probabilities = [0]*7

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

        assert(sum(self.ranks_left) < 52*self.DECKS)
        assert(self.cards_in_shoe < 52*self.DECKS)

    def action_probabilities(self, hand, dealer):
        self.dealer_probabilities = [0]*7
        self.playout_dealer(dealer)

        hit = self.__hit(hand, dealer, len(hand.hand))
        print(f"HIT {round(100*hit,2)}% ", end="")

        stand = self.__stand(hand, dealer)
        print(f"STAND {round(100*stand,2)}% ", end="")

        double = self.__double_down(hand, dealer)
        print(f"DOUBLE {round(100*double,2)}% ", end="")

        if hand.can_split():
            split = self.__split(hand, dealer)
            print(f"SPLIT {round(100*split,2)}% ", end="")

        print("")

    def __split(self, hand, dealer):
        '''
        Returns the probability of winning a hand if chosen action is split
        I don't think I need to simulate both hands, they are identical
        there will be a slight change in shoe dynamics after playing the first hand
        but it shouldn't matter too much
        '''

        hand.split_hand()
        win = 0

        for rank in Rank:
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(rank, Suit.Spade))
            win += self.__hit(new_hand, dealer, len(new_hand.hand)-1)

        return win

    def __hit(self, hand, dealer, index):
        '''
        Returns the probability of winning a hand if action is to hit
        '''

        # busted
        if hand.value > 21:
            return 0

        #This is the 6 card charlie rule, you automatically win
        elif hand.value <= 21 and len(hand.hand) >= 6:
            return 1*self.probability_of_hand(hand, index)

        win = 0

        # For each rank we could draw after hitting
        for rank in Rank:
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(rank, Suit.Spade))

            # special case so that we can reuse this method for split actions
            if new_hand.split_aces:
                temp = self.probability_of_hand(new_hand, index)*self.__stand(new_hand, dealer)
                win += temp
                print(temp)

            else:
                win += self.__hit(new_hand, dealer, index)
                p = self.probability_of_hand(new_hand, index)
                s = self.__stand(new_hand, dealer)
                win += p*s

        return win

    def __double_down(self, hand, dealer):
        '''
        Returns the probability of winning a hand if action is to double down
        '''

        #This function can NOT be called if hand consist of more than 2 cards
        assert(len(hand.hand) == 2)
        #this function should not be called if hand value is 21 or busted
        assert(hand.value < 21)

        win = 0

        # For each rank we could draw after doubling down
        # goal is to find what percentage of time we win vs lose
        for rank in Rank:
            new_hand = deepcopy(hand)
            new_hand.add_card(Card(rank, Suit.Spade))

            prob = self.draw_probability(Card(rank, Suit.Spade))

            win+=prob*self.win_prob(new_hand)

            #print(f"Win prob {round(self.win_prob(new_hand, self.dealer_probabilities)*100, 2)}% with a {new_hand.value}")

        return win

    def __stand(self, hand, dealer):
        '''
        Returns the probability of winning if action is to stand
        '''

        return self.win_prob(hand)

    def win_prob(self, hand):
        '''
        Returns the probability of winning with a hand against all possible
        outcomes of the dealer. P(win) + P(lose) = 1. So, I believe by calculating
        probabilty of winning we also get losing probability
        '''
        value = hand.value
        win = 0

        # Player busted
        if value > 21:
            win = 0

        # Player has BJ and so only pushes against a dealer's BJ
        elif hand.blackjack:
            win = sum(self.dealer_probabilities) - self.dealer_probabilities[5]/2# it's a push if both have BJ so I think divided in 2 is equivalent

        elif value == 21:
            win = sum(self.dealer_probabilities) - (self.dealer_probabilities[4]/2) - self.dealer_probabilities[5] # here we have 21 so we push against 21, lose to dealer's BJ and win all other times

        #Any hand that didn't bust and is not blackjack
        else:
            for x in range(len(self.dealer_probabilities)-3):
                if value > x + 17:
                    win += self.dealer_probabilities[x]
                elif value == x + 17:
                    win += (self.dealer_probabilities[x]/2)
            win += self.dealer_probabilities[6] #Beats all busted hands

        return win

    def playout_dealer(self, dealers_hand):
        '''
        Plays out the dealer's hand according to a specific set of rules dependent
        on the casino. While simultaneously building a list of outcome probabilities
        for the dealer

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
        index = 1 # Always 1 since once the dealer starts playing we have no control

        # Dealer reached stopping condition
        if value >= 17:

            #Dealer has BJ
            if dealers_hand.blackjack:
                self.dealer_probabilities[5] += self.probability_of_hand(dealers_hand, index)

            #Dealer busted
            elif value > 21:
                self.dealer_probabilities[6] += self.probability_of_hand(dealers_hand, index)

            #Dealer has some value between 17 and 21 but not BJ
            else:
                self.dealer_probabilities[value-17] += self.probability_of_hand(dealers_hand, index)

            return self.dealer_probabilities

        #Another card needs to be drawn for the dealer
        else:
            for rank in Rank:
                new_hand = deepcopy(dealers_hand)
                new_hand.add_card(Card(rank, Suit.Spade)) # suit is arbitrary
                self.playout_dealer(new_hand)

        return self.dealer_probabilities

    def probability_of_hand(self, hand, index):
        '''
        This returns the probability of drawing a specific hand starting with some
        card(s) given by the index.
        '''
        self.cards_in_shoe

        # make copies so that variables can be set back to orginal values after calculations
        copy_cards_in_shoe = self.cards_in_shoe
        copy_ranks_left = deepcopy(self.ranks_left)
        count = self.r_count

        prob = 1

        for card in range(index, len(hand.hand)):
            prob*=self.draw_probability(hand.hand[card])
            self.draw(hand.hand[card])

        # reinstate original shoe statistic values
        self.cards_in_shoe = copy_cards_in_shoe
        self.ranks_left = copy_ranks_left
        self.r_count = count

        return prob
