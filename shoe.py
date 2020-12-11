'''
HUGE - I am able to produce very nearly the basic strategy chart with shoe2.py

basic strategy seems to look one move ahead. But this is akin to playing chess
by thinking 1 move ahead. It seems very obvious that by looking ahead to all
possible outcome we have a better chance of winning

^^This might be WRONG! but intuitively it makes sense! I'm freaking out
because I don't know why no one knows about this/talks about it etc.
A researcher must have come across this.

If there's a strategy without counting cards that puts the game of BJ in
your favour then of course casinos wouldn't want you to know about it as they
would either start losing money or have to change the rules of the game.

But even though it's not favourable for the casinos is it even possible that
they could somehow hide the true optimal strategy from nearly everyone.

Certainly some must know...
that or I'm wrong.

Will run simulations with basic strategy vs my strategy and compare
'''


'''
Need this to be fully automated in terms of decision making

0. What is my chance of winning the next hand?
1. Do I bet? (I guess anytime it's greater than 50% I should bet)
2. How much do I bet? (Kelly criterion?) utility function?
3. What is my next action

I need to create a simulation of I don't know 100000 hands and pit 3 strategies
against each other starting with the same seed so that all hands for each strategy
is the game

-Basic Strategy
-My all outcomes strategy

Once I determine with certaining which is best (should be Basic Strategy)
pit basic strategy against card counting dynamic strategy bot

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
        
    def reset_shoe(self):
        self.cards_in_shoe = 52*self.DECKS
        self.ranks_left = [4*self.DECKS]*13
        self.r_count = 0 # running count

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

    def reinstate_card(self, card):
        '''
        Adds a card back into the shoe. This is used to undo any changes made to
        the shoe during simulations
        '''
        self.cards_in_shoe+=1
        self.ranks_left[card.rank]+=1
        self.r_count-=card.cc_value()

        # should never exceed original values
        assert(sum(self.ranks_left) <= 52*self.DECKS)
        assert(self.cards_in_shoe <= 52*self.DECKS)
