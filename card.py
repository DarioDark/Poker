# External libraries
from enum import Enum, IntEnum
from dataclasses import dataclass


class CardValues(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class CardSuits(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


@dataclass(frozen=True, slots=True)
class Card:
    value: int
    suit: CardSuits

    def __str__(self) -> str:
        if self.value < 11:
            return f"{self.value} of {self.suit.value}"
        return f"{CardValues(self.value).name.capitalize()} of {self.suit.value}"

    def __repr__(self) -> str:
        if self.value < 11:
            return f"{self.value} of {self.suit.value}"
        return f"{CardValues(self.value).name.capitalize()} of {self.suit.value}"
    
    def __lt__(self, other) -> bool:
        return self.value < other.value
    
    def __le__(self, other) -> bool:
        return self.value <= other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __ge__(self, other) -> bool:
        return self.value >= other.value
    
    def __gt__(self, other) -> bool:
        return self.value > other.value
