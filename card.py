from enum import IntEnum

class Rank(IntEnum):
    Ace = 0
    Two = 1
    Three = 2
    Four = 3
    Five = 4
    Six = 5
    Seven = 6
    Eight = 7
    Nine = 8
    Ten = 9
    Jack = 10
    Queen = 11
    King = 12

class Suit(IntEnum):
    Spade = 0
    Heart = 1
    Diamond = 2
    Club = 3

class Card():
    def __init__(self, rank, suit):
        self.rank = Rank(rank)
        self.suit = Suit(suit)

    def blackjack_value(self):
        '''
        Returns the blackjack value of this card
        Returns 1 for Ace
        '''
        offset = 1

        # If it's 10 or face card value is 10
        if Rank.Ten <= self.Rank and self.Rank <= Rank.King:
            return 10
        # Otherwise value is face value plus offset
        else:
            return self.Rank + offset

    def cc_value(self, card):
        '''
        Returns the card counting value of the card from the Hi-Lo System
        '''
        if card.rank == Rank.Ace or Rank.Ten <= card.rank and card.rank <= Rank.King:
            return -1
        elif Rank.Seven <= card.rank and card.rank <= Rank.Nine:
            return 0
        else:
            return 1
