from card import Card
from combinationHandler import CardCombinations
from player import Player, PlayerAction

from random import randint

class Bot(Player): # TODO : print actions like a real player (maybe move the print somewhere to not repeat it)
    def __init__(self, name) -> None:
        super().__init__(name=name)
        self.possible_actions: list[PlayerAction] = []
        self.combination_history: list[CardCombinations] = []
        self.action_history: list[PlayerAction] = []
        self.action_dict : dict[CardCombinations, callable] = {
            CardCombinations.HIGH_CARD: self.play_high_card,
            CardCombinations.PAIR: self.play_pair,
            CardCombinations.TWO_PAIR: self.play_two_pair,
            CardCombinations.THREE_OF_A_KIND: self.play_three_of_a_kind,
            CardCombinations.FOUR_OF_A_KIND: self.play_four_of_a_kind,
            CardCombinations.FULL_HOUSE: self.play_full_house,
            CardCombinations.STRAIGHT: self.play_straight,
            CardCombinations.FLUSH: self.play_flush,
            CardCombinations.STRAIGHT_FLUSH: self.play_straight_flush,
            CardCombinations.ROYAL_FLUSH: self.play_royal_flush
        }

    @property
    def safe_action(self):   
        if PlayerAction.CHECK in self.possible_actions:
            return PlayerAction.CHECK
        return PlayerAction.FOLD

    @property
    def follow_action(self):
        if PlayerAction.CALL in self.possible_actions:
            return PlayerAction.CALL
        return PlayerAction.CHECK

    @property
    def risk_action(self):
        if PlayerAction.RAISE in self.possible_actions:
            return PlayerAction.RAISE
        return PlayerAction.ALL_IN


    # Plays according to the bot's combination
    def play_high_card(self, table, combination_cards) -> PlayerAction:
        # Bluff mechanic (15% chance)
        if max(card.value for card in self.hand) <= 7:
            if randint(1, 100) <= 15: 
                return PlayerAction.ALL_IN
            
        # Only Pre-flop
        if len(table) == 0:
            if all(card.value >= 11 for card in self.hand):
                return self.risk_action
            if any(card.value >= 11 for card in self.hand):
                return self.follow_action
            if all(card.suit == self.hand[0].suit for card in self.hand):
                return self.follow_action

        return self.safe_action

    def play_pair(self, table, combination_cards) -> PlayerAction:
        if len(table) == 0: # Only Pre-flop
            if combination_cards[0].value >= 13: 
                return PlayerAction.ALL_IN
        if combination_cards[0].value >= 11:
            return self.risk_action
        if combination_cards[0].value >= 7:
            return self.follow_action
        return self.safe_action

    def play_two_pair(self, table, combination_cards) -> PlayerAction:
        if combination_cards[0][0].value >= 11:
            return self.risk_action
        if combination_cards[0][0].value >= 4:
            return self.follow_action
        return self.safe_action

    def play_three_of_a_kind(self, table, combination_cards) -> PlayerAction:
        # Check if the bot has 2 out of the 3 cards in its hand
        if all(card.value == combination_cards[0].value for card in self.hand): 
            if combination_cards[0].value >= 9:
                return self.risk_action
            return self.follow_action
        return self.safe_action

    def play_four_of_a_kind(self, table, combination_cards) -> PlayerAction:
        # Check if the bot has 2 out of the 4 cards in its hand
        if all(card.value == combination_cards[0].value for card in self.hand): 
            if combination_cards[0].value >= 9:
                return PlayerAction.ALL_IN
        return self.risk_action

    def play_full_house(self, table, combination_cards) -> PlayerAction:
        # Check if the bot has at least one card from the three of a kind and one card from the pair in its hand
        has_three_of_a_kind = any(card.value == combination_cards[0].value for card in self.hand)
        has_pair = any(card.value == combination_cards[-1].value for card in self.hand)

        if has_three_of_a_kind and has_pair:
            return self.risk_action
        return self.follow_action

    def play_straight(self, table, combination_cards) -> PlayerAction:
        return self.risk_action
    
    # TODO : Add "waiting" mechanic : raising bit by bit or checking until the last turn
    def play_flush(self, table, combination_cards) -> PlayerAction:
        return PlayerAction.ALL_IN
    
    def play_straight_flush(self, table, combination_cards) -> PlayerAction:
        return PlayerAction.ALL_IN
    
    def play_royal_flush(self, table, combination_cards) -> PlayerAction:
        return PlayerAction.ALL_IN


    # Information methods
    def print_data(self, highest_player_bet, table, combination, combination_cards) -> None:
        print("--------------------------------------------------------------------------------------------------")
        print("Player", self.name)
        print("The highest bet is:", highest_player_bet)
        print("Your current bet is:", self.current_bet)
        print("You have", self.total_tokens, "tokens.\n")
        print("Your hand:", self.hand, " | Table:", table)
        print("Your current combination:", combination.name.replace("_", " "), " | Cards:", combination_cards)

    def update_possible_actions(self, highest_player_bet: int) -> list[PlayerAction]:
        self.possible_actions: list[PlayerAction] = self.define_possible_actions(highest_player_bet)
                
    def choose_action(self, table: list[Card], highest_player_bet: int) -> PlayerAction:
        """Does some math to find an optimal-ish play"""
        # Processing the data
        combination: CardCombinations = self.get_combination(table)[0]
        combination_cards: list[Card] = self.get_combination(table)[1]

        self.update_possible_actions(highest_player_bet)
        print("highest_player_bet:", highest_player_bet)
        self.print_data(highest_player_bet, table, combination, combination_cards)

        # Choosing the action
        new_action: PlayerAction = self.action_dict[combination](table, combination_cards)
        
        # Only Post-flop
        if len(table) > 0:
            # Does not raise more than once with the same combination
            if combination != self.combination_history[-1]:
                new_action = self.risk_action

            elif combination == self.combination_history[-1] and PlayerAction.RAISE in self.action_history:
                new_action = self.follow_action

            # Does not call more than once with a low combination
            elif self.action_history.count(PlayerAction.CALL) >= 1 and combination.value <= 3:
                new_action = self.safe_action

            # Does not call more than twice with a medium combination
            elif self.action_history.count(PlayerAction.CALL) >= 2 and combination.value <= 6:
                new_action = self.safe_action


        # Updating the history
        self.combination_history.append(combination)
        self.action_history.append(new_action)

        return new_action
