from combinationHandler import CardCombinations
from player import Player, PlayerAction
from card import Card, CardSuits
from deck import Deck
from playerBot import Bot


class GameManager:
    def __init__(self, player_nbr: int) -> None:
        # Data setup
        # self.players: list[Player] = [Bot() for _ in range(player_nbr - 1)] + [Player()]
        self.players = [Player("A"), Player("B"), Player("C")]
        self.active_players = self.players # The players that are still in the game (haven't folded or lost all their money)
        self.turns: int = 0

        # Blinds setup
        self.blinds_amount: list[int] = [500, 1000, 2000, 5000]
        self.current_blind_index: int = 0
        
        # Card setup
        self.deck: Deck = Deck()
        self.table: list[Card] = [Card(2, CardSuits.HEARTS), Card(5, CardSuits.DIAMONDS), Card(12, CardSuits.SPADES)]


    # Properties
    @property
    def total_bet(self) -> int:
        return sum(player.current_bet for player in self.players)
    
    @property
    def highest_bet(self) -> int:
        return max([player.current_bet for player in self.players] + [self.blinds_amount[self.current_blind_index]])

    @property
    def current_blind_index(self) -> None:
        return self.turn // len(self.blinds_amount)


    # Reset methods (usually start/end of a round)
    def reset_players_bet(self) -> None:
        """Reset the current bet of each player"""
        for player in self.players:
            player.current_bet = 0

    def reset_checked_players(self) -> None:
        """Reset the checked state of each player"""
        for player in self.players:
            player.checked = False

    def reset_all_ined_players(self) -> None:
        """Reset the all ined state of each player"""
        for player in self.players:
            player.all_ined = False

    def rotate_blinds_roles(self) -> None:
        """Rotate the blinds roles among the players"""
        self.players.append(self.players.pop(0)) # Instead of rotating the blinds to the left, we just rotate the players anticlockwise (to the right)

    def distribute_starting_bets(self) -> None:
        """Distribute the starting bets (small blind and big blind) according to the current blinds amount and roles"""
        self.active_players[0].bet(int(self.blinds_amount[self.current_blind_index] / 2)) # Small blind
        self.active_players[1].bet(int(self.blinds_amount[self.current_blind_index])) # Big blind

    def put_card_on_table(self) -> None:
        """Draw a card from the deck and put it on the table (3 for the "flop"), up to 5 cards"""
        if len(self.table) == 0:
            for _ in range(3):
                self.table.append(self.deck.draw())
        elif len(self.table) < 5:
            self.table.append(self.deck.draw())


    # Player methods
    def get_players_combinations(self) -> dict[Player: tuple[CardCombinations, list[Card]]]:
        return {player: player.get_combination(self.table) for player in self.active_players}
    
    def get_players_combination_power(self) -> dict[Player: int]:
        return {player: player.get_combination_power(self.table) for player in self.active_players}

    def process_player_action(self, player: Player, action: PlayerAction) -> None:
        if action == PlayerAction.FOLD:
            self.active_players.remove(player)

        elif action == PlayerAction.CHECK:
            player.checked = True

        elif action == PlayerAction.CALL:
            player.checked = True
            player.call_bet(self.highest_bet)

        elif action == PlayerAction.RAISE:
            player.checked = True
            player.raise_bet(self.highest_bet, self.blinds_amount[self.current_blind_index])
            
        elif action == PlayerAction.ALL_IN:
            player.checked = True
            player.all_ined = True     
            player.all_in_bet()   

    def players_play_turn(self) -> None:
        playing = True
        while playing:
            turn = True
            while turn:
                for player in self.active_players:
                    # If there is only one player left, he wins
                    if len(self.active_players) == 1:
                        playing = False
                        turn = False
                        break

                    # If all the players have checked, the turn ends
                    if player.checked:
                        turn = False
                        break

                    action: PlayerAction = player.choose_action(self.table, self.highest_bet)
                    self.process_player_action(player, action)

            if len(self.table) == 5:
                return
            
            # If the turn ends, we put a card on the table and reset the checked players
            self.put_card_on_table()
            self.reset_checked_players()

    def define_winner(self) -> Player:
        """Define the winner of the round"""
        # We get the player(s) with the best combinations
        players_combinations: dict[Player: tuple[CardCombinations, list[Card]]] = self.get_players_combinations()
        players_combinations_power: dict[str: int] = self.get_players_combination_power()
        maximum_power: int = max(players_combinations_power.values())
        players_at_equality_power = {key: players_combinations_power[key] for key in players_combinations_power.keys() if players_combinations_power[key] == maximum_power}
        
        # If there is only one player with the best combination, he wins
        if len(players_at_equality_power) == 1:
            for equal_player in players_at_equality_power:
                for player in players_combinations:
                    if equal_player == player:
                        return player
        else:
            # We get the players with the best combinations and we check cards by cards to see who has the best cards
            players_at_equality_combinations = {key: players_combinations[key] for key in players_combinations.keys() if key in players_at_equality_power}
            # TODO: when revealing the winner and it's winning combination, show the card/combination of cards (list) that got hime the win (in case of an equality on the first two cards it should show the third card, etc.)
            return max(players_at_equality_combinations, key=lambda k: tuple(players_at_equality_combinations[k]))          
                            
    def process_winner(self, winner: Player) -> None:
        """Process the winner of the round and give him the tokens"""
        print(f"Player {winner} won with a {self.get_players_combinations()[winner][0].name.replace("_", " ")} !")
        if winner.all_ined:
            winner.total_tokens += winner.current_bet
        else:
            winner.total_tokens += self.total_bet


    # Round methods
    def round_start(self) -> None:
        """Start a new round"""
        self.active_players: list[Player] = [player for player in self.players if player.total_tokens > 0]
        self.deck.build_deck(shuffle=True)
        self.table.clear()
        self.distribute_starting_bets()

        # Draw 2 cards for each player
        for player in self.active_players:
            player.hand.clear()
            player.draw_card(self.deck, 2)

    def play_round(self) -> None:
        """Play a entire round from start to finish"""
        self.round_start()
        self.players_play_turn()

        winner: Player = self.define_winner()
        self.process_winner(winner)
        
        self.rotate_blinds_roles()
        self.reset_checked_players()
        self.reset_all_ined_players()
        self.reset_players_bet()

        self.turns += 1

    def play(self) -> None:
        while len(self.players) > 1:
            self.play_round()
        print(f"Player {self.players[0]} won the game with {self.players[0].total_tokens} tokens !")
