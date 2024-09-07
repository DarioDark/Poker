from enum import Enum
from card import Card
from combinationHandler import CombinationHandler, CardCombinations
from deck import Deck

class PlayerAction(Enum):
    FOLD = "Fold"
    CHECK = "Check"
    CALL = "Call"
    RAISE = "Raise"
    ALL_IN = "All in"
    NONE = "None"


class Player:
    def __init__(self, name: str, starting_tokens: int = 10_000) -> None:
        self.name: str = name
        self.hand: list[Card] = []

        # Betting setup
        self.total_tokens: int = starting_tokens
        self.current_bet: int = 0
        self.checked: bool = False # Is set to true once the player "Checks" (with a raise, a call, an all_in or a check) during a round to see when every player has checked
        self.all_ined: bool = False # Is set to true when the player goes all in

    def __repr__(self) -> str:
        return self.name

    def draw_card(self, deck: Deck, nbr_of_cards: int = 1) -> None:
        """Draw a card from the deck and add it to the player's hand"""
        for _ in range(nbr_of_cards):
            self.hand.append(deck.draw())


    # Card methods
    def get_combination(self, table: list[Card]) -> tuple[CardCombinations, list[Card]]:
        """Return the best combination of cards the player has"""
        cards = self.hand + table
        return CombinationHandler(cards).combination
    
    def get_combination_power(self, table: list[Card]):
        """Return the power of the best combination of cards the player has"""
        cards = self.hand + table
        return CombinationHandler(cards).power


    # Action methods
    def define_possible_actions(self, highest_player_bet: int) -> list[PlayerAction]:
        """Define the possible actions the player can do depending on the current state of the game"""
        # If the player has no more tokens, he can't do anything other than waiting for the other players to finish the round
        if self.total_tokens == 0:
            return [PlayerAction.NONE]
        
        # We reset the checked state 
        if highest_player_bet > self.current_bet:
            self.checked = False
        
        possible_actions = [PlayerAction.FOLD, PlayerAction.ALL_IN]
        if self.total_tokens >= highest_player_bet:
            possible_actions.insert(1, PlayerAction.RAISE)
        if highest_player_bet > self.current_bet and self.total_tokens > highest_player_bet - self.current_bet:
            possible_actions.insert(1, PlayerAction.CALL)
        if self.current_bet == highest_player_bet:
            possible_actions.insert(1, PlayerAction.CHECK)
        return possible_actions
        
    def choose_action(self, table: list[Card], highest_player_bet: int) -> PlayerAction:
        """Choose an action to do depending on the current state of the game"""
        print("--------------------------------------------------------------------------------------------------")
        print("Player", self.name)
        print("The highest bet is:", highest_player_bet)
        print("Your current bet is:", self.current_bet)
        print("You have", self.total_tokens, "tokens.\n")

        possible_actions: list[PlayerAction] = self.define_possible_actions(highest_player_bet)
        # If the player has no more tokens, he can't do anything other than waiting for the other players to finish the round
        if possible_actions[0] == PlayerAction.NONE:
            print("You have no more tokens. You can't play anymore.")
            return PlayerAction.NONE
        
        # While the player doesn't choose a valid action, we ask him to choose one
        while True:
            try:
                best_combination: CardCombinations = self.get_combination(table)[0]
                best_combination_cards: list[Card] = self.get_combination(table)[1]

                print("Your hand:", self.hand, " | Table:", table)
                print("Your current combination:", best_combination.name.replace("_", " "), " | Cards:", best_combination_cards)
                print("Choose an action:", list(map(lambda x: x.value.capitalize(), possible_actions)))
                
                action = PlayerAction(str(input("Action: ")).capitalize())
                if action in possible_actions:
                    return action
                
                print("Invalid action. Please choose one of the following:", possible_actions)

            except ValueError:
                print("Invalid action. Please choose one of the following:", possible_actions)


    # Betting methods
    def bet(self, amount: int) -> None:
        """Bet a certain amount of tokens"""
        if amount > self.total_tokens: # If the blinds are higher than the player's total tokens, the player goes all in
            amount = self.total_tokens

        self.current_bet += amount
        self.total_tokens -= amount

    def call_bet(self, highest_bet: int) -> int:
        """Bet enough tokens to match the highest bet"""
        amount: int = highest_bet - self.current_bet
        self.bet(amount)
        return amount
        

    def raise_bet(self, highest_bet: int, current_blind: int) -> int:
        """Calls the bet and raises it by a certain amount of tokens chosen by the player"""
        possible_raises: tuple[int, int, int] = (current_blind, current_blind*2, current_blind*4)
        while True:
            try:
                print("Choose an amount to raise:", possible_raises)
                amount: int = int(input("Amount: ")) + (highest_bet - self.current_bet)

                if not amount in possible_raises:
                    print("Invalid amount. Please enter a number among these ones :", possible_raises)
                    continue

                if amount > self.total_tokens:
                    print("You can't bet more than you have.")
                    continue

                if amount < highest_bet:
                    print("You can't bet less than the highest bet.")
                
                    continue

                self.bet(amount)
                return amount
            
            except ValueError:
                print("Invalid amount. Please enter a number.")

    def all_in_bet(self) -> int:
        """Bet all the tokens the player has left"""
        amount: int = self.total_tokens
        self.bet(amount)
        return amount
