"""
story.py
All the "cut-scene" text: the title screen, the intro story for a new
character, and the victory ending after the Final Boss is defeated.
"""

from colorama import Fore, Style

from utils import clear_screen, pause

GAME_TITLE = "SHADOWS OVER ELDERWOOD"


def show_title():
    """The title banner shown on the main menu."""
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print(Fore.CYAN + Style.BRIGHT + GAME_TITLE.center(50))
    print(Fore.CYAN + Style.BRIGHT + "=" * 50)
    print()


def show_intro(player_name):
    """The story intro. Shown once, when a brand-new character is created."""
    # Each item in this list is one "page" of the story.
    pages = [
        "Long ago, the village of Elderwood lived in peace.",
        "Then the DARK LORD awoke deep inside the Shadow Cave,\n"
        "beyond the Whispering Forest.",
        "Monsters now roam the forest, and the villagers\n"
        "are too afraid to leave their homes.",
        f"You, {player_name}, are a young adventurer who has just\n"
        "arrived in Elderwood looking for work...",
        "Find ELDER ROWAN in the village. He will know what to do.",
    ]

    for page in pages:
        clear_screen()
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print(Fore.CYAN + Style.BRIGHT + GAME_TITLE.center(50))
        print(Fore.CYAN + Style.BRIGHT + "=" * 50)
        print()
        print(Fore.YELLOW + page)
        print()
        pause()

    # A quick "how to play" page after the story
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "HOW TO PLAY")
    print()
    print(Fore.WHITE + "  W A S D  -> move (no Enter needed)")
    print(Fore.WHITE + "  Walk into a 🧙 to talk to an NPC")
    print(Fore.WHITE + "  Walk into a 👹 to fight a monster")
    print(Fore.WHITE + "  Walk into the 🏪 to visit the shop")
    print(Fore.WHITE + "  Walk through a 🚪 to travel to another area")
    print(Fore.WHITE + "  I = Inventory   C = Character   K = Skills   J = Quests")
    print(Fore.WHITE + "  Q = Save and quit")
    print()
    pause("Press ENTER to begin your adventure...")


def show_victory(player):
    """Ending screen after the Dark Lord is defeated."""
    clear_screen()
    print(Fore.YELLOW + Style.BRIGHT + "*" * 50)
    print(Fore.YELLOW + Style.BRIGHT + "VICTORY!".center(50))
    print(Fore.YELLOW + Style.BRIGHT + "*" * 50)
    print()
    print(Fore.GREEN + "The Dark Lord lets out one final scream and fades away.")
    print(Fore.GREEN + "Sunlight pours into the Shadow Cave for the first time in years.")
    print()
    print(Fore.CYAN + f"{player.username}, the people of Elderwood will never forget you!")
    print()
    print(Fore.WHITE + f"Final level: {player.level}   Gold: {player.gold}")
    print()
    print(Fore.MAGENTA + Style.BRIGHT + "YOU WIN THE GAME!")
    print(Fore.WHITE + "(You can keep exploring, or press Q on the map to save and quit.)")
    print()
    pause()
