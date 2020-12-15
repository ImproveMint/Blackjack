from card import Card, Rank, Suit
from copy import deepcopy

class Hand():
    def __init__(self, cards):
        self.cards = cards
        self.soft = False
        self.double = False
        self.split = False
        self.split_aces = False
        self.value = 0
        self.blackjack = False

        # call these functions to initialize certain values
        self.__calculate_blackjack_value()

    def __calculate_blackjack_value(self):
        '''
        Calculates the blackjack value of this hand
        '''
        ace_value = 11
        num_aces = 0
        hand_value = 0

        for card in self.cards:

            if card.rank == Rank.Ace:
                num_aces+=1
            else:
                hand_value += card.blackjack_value()

        if num_aces > 0:
            if (hand_value + (num_aces - 1) + ace_value) > 21:
                self.soft = False
                hand_value += num_aces
            else:
                self.soft = True
                hand_value += ((num_aces - 1) + ace_value)

        self.value = hand_value
        self.__is_blackjack() # called here because if the value changed BJ might change

    def __is_blackjack(self):
        if len(self.cards) == 2 and self.value == 21:
            self.blackjack = True

    def add_card(self, card):
        self.cards.append(card)
        self.__calculate_blackjack_value()

    def double_down(self, card):
        self.add_card(card)
        self.double = True

    def split_hand(self):
        assert(len(self.cards) == 2)
        assert(self.cards[0].blackjack_value() == self.cards[1].blackjack_value())

        self.split = True

        if self.cards[0].rank == Rank.Ace:
            self.split_aces = True

        self.cards.pop()

        self.value = self.__calculate_blackjack_value()

    def can_split(self):
        if len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank and not self.split:
            return True
        return False

    def __str__(self):
        s = ""
        for card in self.cards:
            s += card.__repr__() + " "
        return s

    def __deepcopy__(self, memo):
        cls = self.__class__ # Extract the class of the object
        result = cls.__new__(cls) # Create a new instance of the object based on extracted class
        memo[id(self)] = result

        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))

        return result
