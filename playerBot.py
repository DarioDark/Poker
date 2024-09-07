from player import Player, PlayerAction
from card import Card

class Bot(Player):
    def __init__(self) -> None:
        super().__init__()

    def choose_action(self, table: list[Card]) -> PlayerAction:
        action = None # Does some math to find an optimal-ish play
        return action
