from shoe import Shoe
from card import Card, Rank, Suit
from hand import Hand

def hand_class_test(hand,value,soft, bj):

    passed = True

    if hand.value != value:
        print(f"FAILED: hand value expected {value} but returned '{hand.value}'")
        passed = False

    if hand.soft != soft:
        print(f"FAILED: soft expected {soft} but returned '{hand.soft}'")
        passed = False

    if hand.blackjack != bj:
        print(f"FAILED: blackjack expected {bj} but returned '{hand.blackjack}'")
        passed = False

    if passed:
        print("SUCCESS: All tests passed!")

def test_hand_class():
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

    hand1 = Hand([c0, c10])
    value1 = 21
    soft1 = True # technically is soft but you would never hit.
    blackjack1 = True

    hand2 = Hand([c11, c4, c5])
    value2 = 21
    soft2 = False
    blackjack2 = False

    hand3 = Hand([c0, c0, c12])
    value3 = 12
    soft3 = False
    blackjack3 = False

    hand4 = Hand([c0, c0, c0])
    value4 = 13
    soft4 = True
    blackjack4 = False

    hand_class_test(hand1, value1, soft1, blackjack1)
    hand_class_test(hand2, value2, soft2, blackjack2)
    hand_class_test(hand3, value3, soft3, blackjack3)
    hand_class_test(hand4, value4, soft4, blackjack4)

if __name__ == "__main__":
    test_hand_class()
