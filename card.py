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
        if Rank.Ten <= self.rank and self.rank <= Rank.King:
            return 10
        # Otherwise value is face value plus offset
        else:
            return self.rank + offset

    def cc_value(self):
        '''
        Returns the card counting value of the card from the Hi-Lo System
        '''
        if self.rank == Rank.Ace or Rank.Ten <= self.rank and self.rank <= Rank.King:
            return -1
        elif Rank.Seven <= self.rank and self.rank <= Rank.Nine:
            return 0
        else:
            return 1

    def __repr__(self):
        s = ""

        if self.rank == Rank.Ace:
            s += "A"
        elif self.rank == Rank.Jack:
            s += "J"
        elif self.rank == Rank.Queen:
            s += "Q"
        elif self.rank == Rank.King:
            s += "K"
        else:
            s += str(self.rank.value + 1)

        return s

    def __str__(self):
        s = str(self.rank) + " " + str(self.suit)
        return s
