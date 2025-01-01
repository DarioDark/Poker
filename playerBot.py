from card import Card
from combinationHandler import CardCombinations
from player import Player, PlayerAction

class Bot(Player):
    def __init__(self) -> None:
        super().__init__()

    def choose_action(self, table: list[Card], highest_player_bet: int) -> PlayerAction:
        """Does some math to find an optimal-ish play"""
        cards: list[Card] = self.hand + table

        # Setup of the possible actions
        possible_actions: list[PlayerAction] = self.define_possible_actions(highest_player_bet)
        safest_action: PlayerAction = PlayerAction.FOLD
        follow_action: PlayerAction = PlayerAction.CHECK
        risky_action: PlayerAction = PlayerAction.RAISE
        
        if PlayerAction.CHECK in possible_actions:
            safest_action = PlayerAction.CHECK
        if PlayerAction.CALL in possible_actions:
            follow_action: PlayerAction = PlayerAction.CALL


        # Processing the data to make the right choice
        combination: CardCombinations = self.get_combination()[0]
        combination_cards: list[Card] = self.get_combination()[1]
        
        # TODO : global RAISE and ALL IN mechanic
        if combination == CardCombinations.HIGH_CARD:
            return safest_action
            
        elif combination == CardCombinations.PAIR:
            if combination_cards[0].value < 11:
                return safest_action
            return follow_action

        elif combination == CardCombinations.TWO_PAIR:
            if combination_cards[0][0].value < 11:
                return safest_action
        
        elif combination == CardCombinations.THREE_OF_A_KIND:
            if combination_cards[0].value < 6:
                return safest_action
            # TODO : check if the pair is : 2 in hand + 1 on table -> RAISE
            
        elif combination == CardCombinations.FOUR_OF_A_KIND:
            ... # TODO : check if the colmbination is : 2 in hand + 2 on table -> RAISE
            
        elif combination == CardCombinations.FULL_HOUSE:
            ... # TODO : Raise
        
        elif combination == CardCombinations.STRAIGHT:
            ... # TODO : Raise 
        
        elif combination == CardCombinations.STRAIGHT_FLUSH:
            ... # TODO : Raise
            
        elif combination == CardCombinations.FLUSH:
            ... # TODO : Raise unless the straight is like 2 -> 7 (a bit weak depending on the table)4
            
        elif combination == CardCombinations.ROYAL_FLUSH:
            return PlayerAction.ALL_IN
