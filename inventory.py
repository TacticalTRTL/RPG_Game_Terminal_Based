"""
inventory.py
The player's inventory is a dictionary: {item name: how many}
Example: {"Potion": 3, "Wolf Pelt": 1}

This file has the functions that add, remove, show and use items.
"""

from colorama import Fore, Style

from item import ITEMS, USABLE_TYPES, item_color
from utils import ask_number, clear_screen, pause


def add_item(player, name, amount=1):
    """Put items into the inventory."""
    player.inventory[name] = player.inventory.get(name, 0) + amount


def remove_item(player, name, amount=1):
    """Take items out. Returns False if the player doesn't have enough."""
    if player.inventory.get(name, 0) < amount:
        return False
    player.inventory[name] -= amount
    # Delete the entry completely when the count reaches 0
    if player.inventory[name] == 0:
        del player.inventory[name]
    return True


def has_item(player, name):
    return player.inventory.get(name, 0) > 0


def print_inventory(player):
    """Print every item with its count and description."""
    if not player.inventory:
        print(Fore.LIGHTBLACK_EX + "  (your bag is empty)")
        return
    for name, count in player.inventory.items():
        color = item_color(name)
        print(color + f"  {name} x{count}" + Fore.WHITE + f"  - {ITEMS[name]['description']}")


def use_item(player, name):
    """Use one item and return a message saying what happened."""
    info = ITEMS[name]
    remove_item(player, name)

    if info["type"] == "heal":
        healed = player.heal(info["value"])
        return Fore.GREEN + f"You drink the {name} and recover {healed} HP."
    if info["type"] == "attack":
        player.attack += info["value"]
        return Fore.RED + f"You feel stronger! Attack +{info['value']}."
    if info["type"] == "defense":
        player.defense += info["value"]
        return Fore.BLUE + f"Your skin hardens! Defense +{info['value']}."

    return "Nothing happens."


def use_item_menu(player):
    """
    Let the player pick a usable item from a numbered list.
    Returns a message if an item was used, or None if they cancelled.
    (combat.py uses the None to know the player's turn wasn't spent)
    """
    usable = [name for name in player.inventory if ITEMS[name]["type"] in USABLE_TYPES]

    if not usable:
        print(Fore.RED + "You have no usable items.")
        pause()
        return None

    print()
    for number, name in enumerate(usable, start=1):
        print(item_color(name) + f"  {number}. {name} x{player.inventory[name]}"
              + Fore.WHITE + f" - {ITEMS[name]['description']}")
    print(Fore.WHITE + "  0. Cancel")

    choice = ask_number("Use which item? ", 0, len(usable))
    if choice == 0:
        return None
    return use_item(player, usable[choice - 1])


def show_inventory_screen(player):
    """The inventory screen opened with the I key on the map."""
    while True:
        clear_screen()
        print(Fore.MAGENTA + Style.BRIGHT + "=== INVENTORY ===")
        print(Fore.YELLOW + f"Gold: {player.gold}")
        print(Fore.GREEN + f"HP: {player.hp}/{player.max_hp}")
        print()
        print_inventory(player)
        print()
        print(Fore.WHITE + "1. Use an item")
        print(Fore.WHITE + "2. Back to the map")

        choice = ask_number("Choose: ", 1, 2)
        if choice == 2:
            return

        message = use_item_menu(player)
        if message:
            print(message)
            pause()
