# Internal libraries
from homeMenu import HomeMenu

if __name__ == "__main__":
    H = HomeMenu()
    try:
        H.game.play()
    except:
        print("An error occured. The game will now stop.")
        exit()