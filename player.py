class Player():
    def __init__(self, name, bankroll):
        self.name = name
        self.bankroll = bankroll
        self.hand = None
        self.bet_size = 0
        self.stand = False
        self.bust = False

    def won(self, amount):
        print(f"Won ${amount} bankroll: ${self.bankroll + amount}")
        self.bankroll+=amount

    def bet(self):

        if self.bankroll == 0:
            print("Busted")
            exit()

        elif self.bankroll < 10:
            amount = self.bankroll

        else:
            amount = round(self.bankroll*0.06,0)

        self.bankroll -= amount
        self.bet_size = amount

        return amount

    def add_hand(self, hand):
        self.hand = hand

    def payout(self, dh):
        print(f"{self.name} has {self.hand.value} vs {dh.value} bet: ${self.bet_size}")

        if not self.bust and self.hand.value >= dh.value:
            #Dealer busted
            if dh.value > 21:
                self.won(self.bet_size*2)

            elif dh.blackjack and self.hand.blackjack:
                self.won(self.bet_size)

            elif dh.blackjack and self.hand.value == 21:
                print("LOST")
            elif self.hand.blackjack:
                self.won(self.bet_size*2.5)
            elif self.hand.value == dh.value:
                self.won(self.bet_size)
            elif self.hand.value >= dh.value:
                self.won(self.bet_size*2)

        elif not self.bust and dh.value > 21:
            self.won(self.bet_size*2)
        else:
            print("LOST")

        self.hand = None
        self.bust = False
        self.stand = False
        self.bet_size = 0

    def is_done(self):
        if self.stand or self.bust:
            return True
        else:
            return False

    def process_action(self, action, card):

        if self.is_done():
            return
        else:
            if action == 'H':
                self.hand.add_card(card)

            elif action == 'S':
                self.stand = True

            elif action == 'D':
                if len(self.hand.cards) == 2:
                    self.hand.add_card(card)
                    self.bet_size*=2
                    self.stand = True
                else:
                    self.process_action('H', card)

            elif action == 'd':
                if len(self.hand.cards) == 2:
                    self.hand.add_card(card)
                    self.bet_size*=2
                    self.stand = True
                else:
                    self.process_action('S')

            elif action == 'P':
                #split
                self.hand.split_hand()
                self.hand.add_card(card)
                self.bet_size*=2

                # Only get 1 card if you split on aces
                if self.hand.split_aces:
                    self.stand = True

            if self.hand.value > 21:
                self.bust = True

            elif self.hand.value == 21:
                self.stand = True

            return

    def __str__(self):
        return self.name + " ($" + str(self.bankroll) + ")"
