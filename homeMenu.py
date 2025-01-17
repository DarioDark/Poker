# External libraries
import os

# Internal libraries
from gameManager import GameManager

class HomeMenu:
    def __init__(self):
        os.system("cls")
        print(""" 
         ____        _
        |  _ \ ___  | | _____ _ __ 
        | |_) / _ \ | |/ / _ \ '__|
        |  __/ (_) ||   <  __/ |   
        |_|   \___/ |_|\_\___|_|          
        """)
        print("Welcome to the Python Poker game!")
        print("=================================")
        player_nbr: int = 0
        while player_nbr <= 0 or player_nbr > 8:
            player_nbr = int(input("Pleaser enter the number of bots to play against (min: 1 | max: 8): "))

        self.game = GameManager(player_nbr + 1)