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

from card import Card
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
        self.r_count+=(card.cc_value(card))

        # post conditions
        assert(self.cards_in_shoe > 0)
        assert(self.ranks_left[card.rank] > 0)
