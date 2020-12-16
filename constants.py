from enum import IntEnum

class Action(IntEnum):
    HIT = 0
    STAND = 1
    DOUBLE = 2
    SPLIT = 3

class Outcome(IntEnum):
    WIN = 0
    PUSH = 1
    LOSE = 2

class Dealer_Outcome(IntEnum):
    SUM_17 = 0
    SUM_18 = 1
    SUM_19 = 2
    SUM_20 = 3
    SUM_21 = 4
    BJ = 5
    BUST = 6
