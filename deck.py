# External libraries
import random

# Internal libraries
from card import Card, CardSuits


class Deck(list): # list[Card]
    def __init__(self) -> None:
        super().__init__()
        self.build_deck()

    def build_deck(self, shuffle: bool=True) -> None:
        self.clear()
        self.extend([Card(value=value, suit=suit) for suit in list(CardSuits) for value in range(2, 15)])
        if shuffle:
            self.shuffle()

    def shuffle(self) -> None:
        random.shuffle(self)

    def draw(self) -> Card:
        return self.pop()
