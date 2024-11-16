from project import validDice, calculateScore, is2Pair, is3ofAKind
from project import isFullHouse, isStraight, is4ofAKind, is5ofAKind
import pytest
import dice


def test_is2Pair():
    assert is2Pair([1,1,2,2,3]) == True
    assert is2Pair([1,1,2,3,3]) == True
    assert is2Pair([1,2,1,2,3]) == True
    assert is2Pair([1,1,5,4,3]) == False
    assert is2Pair([1,2,3,4,5]) == False
    assert is2Pair([1,1,1,5,5]) == False
    assert is2Pair([1,1,1,1,5]) == False
    assert is2Pair([1,1,1,1,1]) == False

def test_is3ofAKind():
    assert is3ofAKind([1,1,1,2,3]) == True
    assert is3ofAKind([1,1,1,3,3]) == True
    assert is3ofAKind([1,2,1,3,1]) == True
    assert is3ofAKind([1,1,5,4,3]) == False
    assert is3ofAKind([1,2,3,4,5]) == False
    assert is3ofAKind([1,1,1,1,5]) == False
    assert is3ofAKind([1,1,1,1,1]) == False

def test_isFullHouse():
    assert isFullHouse([1,1,2,2,2]) == True
    assert isFullHouse([1,1,1,3,3]) == True
    assert isFullHouse([1,2,1,2,1]) == True
    assert isFullHouse([1,1,5,4,3]) == False
    assert isFullHouse([1,2,3,4,5]) == False
    assert isFullHouse([1,1,1,1,5]) == False
    assert isFullHouse([1,1,1,1,1]) == False
    assert isFullHouse([1,1,3,3,6]) == False

def test_isStraight():
    assert isStraight([1,2,3,4,5]) == True
    assert isStraight([2,3,4,5,6]) == True
    assert isStraight([1,1,5,4,3]) == False
    assert isStraight([1,2,3,4,6]) == False
    assert isStraight([1,3,4,5,6]) == False
    assert isStraight([1,1,1,1,1]) == False

def test_is4ofAKind():
    assert is4ofAKind([1,1,1,1,2]) == True
    assert is4ofAKind([1,2,2,2,2]) == True
    assert is4ofAKind([3,3,1,3,3]) == True
    assert is4ofAKind([1,2,3,4,6]) == False
    assert is4ofAKind([1,1,1,2,2]) == False
    assert is4ofAKind([1,1,1,1,1]) == False
    assert is4ofAKind([1,1,2,3,3]) == False

def test_is5ofAKind():
    assert is5ofAKind([1,1,1,1,1]) == True
    assert is5ofAKind([2,2,2,2,2]) == True
    assert is5ofAKind([5,5,5,5,5]) == True
    assert is5ofAKind([1,2,3,4,6]) == False
    assert is5ofAKind([1,1,1,2,2]) == False
    assert is5ofAKind([1,1,1,1,2]) == False
    assert is5ofAKind([1,1,2,3,3]) == False

def test_calculateScore():
    d = dice.Dice()
    die = dice.Die(1)
    d.addDie(die)
    die = dice.Die(2)
    d.addDie(die)
    die = dice.Die(3)
    d.addDie(die)
    die = dice.Die(4)
    d.addDie(die)
    with pytest.raises(ValueError):
        calculateScore(d)
    die = dice.Die(5)
    d.addDie(die)
    w, winStr = calculateScore(d)
    assert w ==20
    assert winStr == "a Straight"

    d.replaceDie(1,1)
    d.replaceDie(2,2)
    d.replaceDie(3,2)
    d.replaceDie(4,3)
    w, winStr = calculateScore(d)
    assert w == 5
    assert winStr == "2 Pair"

    d.replaceDie(4, 2)
    w, winStr = calculateScore(d)
    assert w == 15
    assert winStr == "a Full House"

    d.replaceDie(0, 2)
    w, winStr = calculateScore(d)
    assert w == 25
    assert winStr == "4 of a Kind"

    d.replaceDie(1, 2)
    w, winStr = calculateScore(d)
    assert w == 35
    assert winStr == "5 of a Kind"

def test_validDice():
    assert validDice("1 2 4") == True
    assert validDice("3") == True
    assert validDice("5 2 3 1") == True
    assert validDice ("1 2 3 4 5 6") == False
    assert validDice("") == False
    assert validDice("1 cat") == False
    assert validDice("2@5") == False
    assert validDice("dog") == False
