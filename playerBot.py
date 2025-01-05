from card import Card
from combinationHandler import CardCombinations
from player import Player, PlayerAction

class Bot(Player): # TODO : print actions like a real player (maybe move the print somewhere to not repeat it)
    def __init__(self, name) -> None:
        super().__init__(name=name)

    def choose_action(self, table: list[Card], highest_player_bet: int) -> PlayerAction:
        """Does some math to find an optimal-ish play"""
        
        # Processing the data to make the right choice
        combination: CardCombinations = self.get_combination(table)[0]
        combination_cards: list[Card] = self.get_combination(table)[1]
        
        # Setup of the possible actions
        possible_actions: list[PlayerAction] = self.define_possible_actions(highest_player_bet)
        safest_action: PlayerAction = PlayerAction.FOLD
        follow_action: PlayerAction = PlayerAction.CHECK
                
        if PlayerAction.CHECK in possible_actions:
            safest_action = PlayerAction.CHECK
        if PlayerAction.CALL in possible_actions:
            follow_action: PlayerAction = PlayerAction.CALL
        
        print("--------------------------------------------------------------------------------------------------")
        print("Player", self.name)
        print("The highest bet is:", highest_player_bet)
        print("Your current bet is:", self.current_bet)
        print("You have", self.total_tokens, "tokens.\n")
        print("Your hand:", self.hand, " | Table:", table)
        print("Your current combination:", combination.name.replace("_", " "), " | Cards:", combination_cards)


        # TODO : global RAISE and ALL IN mechanic
        if combination == CardCombinations.HIGH_CARD:
            return safest_action
            
        elif combination == CardCombinations.PAIR:
            if combination_cards[0].value >= 11:
                return follow_action
            return safest_action

        elif combination == CardCombinations.TWO_PAIR:
            if combination_cards[0][0].value >= 11:
                return follow_action
            return safest_action
        
        elif combination == CardCombinations.THREE_OF_A_KIND:
            if all(card.value == combination_cards[0].value for card in self.hand): # Check to make sure the bot has 2 out of the 3 cards in hand
                return follow_action
            return safest_action
            
        elif combination == CardCombinations.FOUR_OF_A_KIND:
            if all(card.value == combination_cards[0].value for card in self.hand): # Check to make sure the bot has 2 out of the 4 cards in hand
                return follow_action
            return safest_action
            
        elif combination == CardCombinations.FULL_HOUSE:
            if all(card.value == combination_cards[0][0].value for card in self.hand) and all(card.value == combination_cards[1][0].value for card in self.hand): # Check to make sure the bot has at least 1 of the three kind and one of the pair in his hand
                return follow_action
            return safest_action
        
        elif combination == CardCombinations.STRAIGHT:
            return PlayerAction.RAISE
            
        elif combination == CardCombinations.FLUSH:
            return PlayerAction.RAISE
            
        elif combination == CardCombinations.STRAIGHT_FLUSH:
            return PlayerAction.RAISE
            
        elif combination == CardCombinations.ROYAL_FLUSH:
            return PlayerAction.ALL_IN
