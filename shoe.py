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
        assert(self.cards_in_shoe >= 0)
        assert(self.ranks_left[card.rank] >= 0)

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

    def __deepcopy__(self, memo):
        cls = self.__class__ # Extract the class of the object
        result = cls.__new__(cls) # Create a new instance of the object based on extracted class
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))

        return result

    def __str__(self):
        return str(self.DECKS) + " deck shoe - " + str(self.cards_in_shoe) + "/" + str(self.DECKS*52) + " cards remain"
