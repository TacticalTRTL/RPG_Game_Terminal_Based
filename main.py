"""
main.py
Start the game from here:   uv run main.py

Flow:
  title screen -> Register / Login -> load save (or make a new character
  and show the story intro) -> game.play() -> back to this menu
"""

from colorama import Fore, init

from auth import login, register
from database import load_player_data, save_player
from game import play
from player import Player
from story import show_intro, show_title
from utils import ask_number

# autoreset=True puts the color back to normal after every print()
init(autoreset=True)


def start_game(username):
    """Load the player's save, or create a new character if there isn't one."""
    saved = load_player_data(username)

    if saved is None:
        player = Player(username)
        show_intro(username)
        save_player(player)
    else:
        player = Player.from_dict(saved)

    play(player)


def main():
    while True:
        show_title()
        print(Fore.WHITE + "1. Register")
        print(Fore.WHITE + "2. Login")
        print(Fore.WHITE + "3. Quit")
        print()

        choice = ask_number("Choose: ", 1, 3)

        if choice == 1:
            username = register()
            if username:
                start_game(username)   # log straight in after registering
        elif choice == 2:
            username = login()
            if username:
                start_game(username)
        else:
            print(Fore.CYAN + "Farewell, adventurer!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Ctrl+C anywhere quits cleanly (progress is auto-saved after battles
        # and map changes, and when you press Q)
        print()
        print(Fore.CYAN + "Game closed. Farewell, adventurer!")
