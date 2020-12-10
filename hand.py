from card import Card, Rank, Suit

class Hand():
    def __init__(self, hand):
        self.hand = hand
        self.soft = False
        self.double = False
        self.value = self.__calculate_blackjack_value()
        self.blackjack = self.__is_blackjack()

    def __calculate_blackjack_value(self):
        '''
        Returns the blackjack value of this hand
        '''
        ace_value = 11
        num_aces = 0
        hand_value = 0

        for card in self.hand:

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

        return hand_value

    def __is_blackjack(self):
        if len(self.hand) == 2 and self.value == 21:
            return True
        else:
            return False

    def add_card(self, card):
        self.hand.append(card)
        self.value = self.__calculate_blackjack_value()

    def double_down(self, card):
        self.add_card(card)
        self.double = True
