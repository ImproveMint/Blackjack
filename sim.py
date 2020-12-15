'''
sim.py

Then it will evolve to an simulator that tests different strategies
'''

from card import Card, Rank, Suit
from hand import Hand
from dealer import Dealer
from shoe import Shoe
from player import Player
import probability, strategy, random
from copy import deepcopy

c0 = Card(Rank.Ace, Suit.Spade)
c1 = Card(Rank.Two, Suit.Heart)
c2 = Card(Rank.Three, Suit.Diamond)
c3 = Card(Rank.Four, Suit.Club)
c4 = Card(Rank.Five, Suit.Heart)
c5 = Card(Rank.Six, Suit.Diamond)
c6 = Card(Rank.Seven, Suit.Club)
c7 = Card(Rank.Eight, Suit.Spade)
c8 = Card(Rank.Nine, Suit.Heart)
c9 = Card(Rank.Ten, Suit.Diamond)
c10 = Card(Rank.Jack, Suit.Club)
c11 = Card(Rank.Queen, Suit.Spade)
c12 = Card(Rank.King, Suit.Heart)

class Sim():
    def __init__(self):
        self.DECKS = 8
        self.shoe = Shoe(8)
        self.p1 = Player("Complete_Strategy", 10000)
        self.p2 = Player("Basic_Strategy", 10000)
        self.dealer = Dealer(self.shoe)
        self.sims = 0

    def run(self):
        for x in range(10000):

            print(f"*** Hand {self.sims+1}***")
            self.sims+=1;

            print(self.p1)
            print(self.p2)

            self.p1.bet()
            self.p2.bet()

            self.deal_cards()

            while not self.p1.is_done() or not self.p2.is_done():
                card = Card(Rank(random.randint(Rank.Ace, Rank.King)), Suit.Spade)
                action_b = strategy.infinite_basic_action(self.p1.hand, self.dealer)
                action_c = strategy.infinite_complete_action(self.p2.hand, self.dealer)
                self.p1.process_action(action_b, card)
                self.p2.process_action(action_c, card)

            self.dealer.playout_hand()

            self.p1.payout(self.dealer.hand)
            self.p2.payout(self.dealer.hand)

            self.dealer.reset()
            self.shoe.reset_shoe() # why am I reseting shoe everytime yet still calculating deal probs every hand?

            print("\n")

    def deal_cards(self):
        players_hand = self.random_hand(2)
        self.p1.add_hand(players_hand)
        self.p2.add_hand(deepcopy(players_hand))
        self.dealer.deal_card(Card(Rank(random.randint(Rank.Ace, Rank.King)), Suit.Spade))

    def random_hand(self, size):
        cards = []
        for _ in range(size):
            card = Card(Rank(random.randint(Rank.Ace, Rank.King)), Suit.Spade)
            cards.append(card)
            self.shoe.draw(card)

        return Hand(cards)

if __name__ == "__main__":
    sim = Sim()
    sim.run()
