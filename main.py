from shoe import Shoe
from card import Card, Rank, Suit

decks = 8
shoe = Shoe(decks)

c = Card(Rank.Ten, Suit.Spade)
print(shoe.draw_probability(c))
