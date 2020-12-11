from shoe import Shoe
from card import Card, Rank, Suit
from hand import Hand
from dealer import Dealer
from probability import Probability

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

def hand_class_test(hand,value,soft, bj):

    passed = True

    if hand.value != value:
        print(f"\tFAILED: hand value expected {value} but returned '{hand.value}'")
        passed = False

    if hand.soft != soft:
        print(f"\tFAILED: soft expected {soft} but returned '{hand.soft}'")
        passed = False

    if hand.blackjack != bj:
        print(f"\tFAILED: blackjack expected {bj} but returned '{hand.blackjack}'")
        passed = False

    if passed:
        print("\tSUCCESS: All tests passed!")

def test_hand_class():

    hand1 = Hand([c0, c10])
    hand2 = Hand([c11, c4, c5])
    hand3 = Hand([c0, c0, c12])
    hand4 = Hand([c0, c0, c0])

    print("Testing random hands")
    hand_class_test(hand1, 21, True, True)
    hand_class_test(hand2, 21, False, False)
    hand_class_test(hand3, 12, False, False)
    hand_class_test(hand4, 13, True, False)

    print("Testing if Hand class can accept single card")
    hand5 = Hand([c0])
    hand_class_test(hand5, 11, True, False)

    print("Testing if Hand class can add card that makes blackjack")
    hand5.add_card(c10)
    hand_class_test(hand5, 21, True, True)

    print("Testing if Hand class can add card that gives 21 but not BJ")
    hand6 = Hand([c4, c5])
    hand_class_test(hand6, 11, False, False)

    hand6.add_card(c11)
    hand_class_test(hand6, 21, False, False)

def test_dealer_class():
    print("Testing dealer outcome probabilities:")

    exp2 = [0.13058415942623405, 0.12574023141128113, 0.12152073663186165, 0.11642966156349394, 0.11141335620272531, 0, 0.39431185476440145]
    dealer_class_test(c3, exp2)

    exp1 = [0.1305738023850187, 0.13081247963824286, 0.13064487057259502, 0.13087841330635158, 0.05378158025900594, 0.3076923076923077, 0.11561654614647492]
    dealer_class_test(c0, exp1)

    exp3 = [0.11142653527996113, 0.11124386070333868, 0.1114489527312293, 0.34204970160714654, 0.034558153222771115, 0.07692307692307693, 0.2123497195324762]
    dealer_class_test(c9, exp3)

def dealer_class_test(card, exp):

    shoe = Shoe(8)
    prob = Probability(shoe)
    dealer = Dealer(shoe, prob)
    dealer.deal_card(card)
    probs = dealer.dealer_outcome_probs()

    # make sure probability isn't greated than one
    if round(sum(probs), 2) != 1.0:
        print(f"FAIL: dealer outcome probabilites < or > 1 : '{sum(probs)}'")
        return

    if exp == probs:
        print("\tSUCCESS: dealer outcome probabilites as expected")
    else:
        print("\tFAIL: dealer outcome probabilites NOT as expected")

def test_probability_class():
    shoe = Shoe(8)
    prob = Probability(shoe)

    hand = Hand([c9, c4])
    dealer = Hand([c6])

    prob1 = prob.probability_of_hand(hand, 0)
    exp1 = 0.0059314179796107515
    prob2 = prob.probability_of_card(c0)
    exp2 = 0.07692307692307693

    if prob1 == exp1:
        print("SUCCESS: probability class return correct probability")
    else:
        print(f"FAIL: probability return '{prob1}' probability expected '{exp1}'")

    if prob2 == exp2:
        print("SUCCESS: probability class return correct probability")
    else:
        print(f"FAIL: probability return '{prob2}' probability expected '{exp2}'")

if __name__ == "__main__":
    test_hand_class()
    test_dealer_class()
    test_probability_class()
