"""
shop.py
The shop: buy items with gold, or sell items for half their price.
"""

from colorama import Fore, Style

from inventory import add_item, remove_item
from item import ITEMS, SHOP_STOCK, item_color, sell_price
from utils import ask_number, clear_screen, pause


def buy_menu(player):
    print()
    for number, name in enumerate(SHOP_STOCK, start=1):
        info = ITEMS[name]
        print(item_color(name) + f"  {number}. {name}" + Fore.YELLOW + f" - {info['price']} gold"
              + Fore.WHITE + f"  ({info['description']})")
    print(Fore.WHITE + "  0. Cancel")

    choice = ask_number("Buy which item? ", 0, len(SHOP_STOCK))
    if choice == 0:
        return

    name = SHOP_STOCK[choice - 1]
    price = ITEMS[name]["price"]
    if player.gold < price:
        print(Fore.RED + "You don't have enough gold!")
    else:
        player.gold -= price
        add_item(player, name)
        print(Fore.GREEN + f"You bought a {name} for {price} gold.")
    pause()


def sell_menu(player):
    # Quest items can't be sold
    sellable = [name for name in player.inventory if ITEMS[name]["type"] != "quest"]
    if not sellable:
        print(Fore.RED + "You have nothing to sell.")
        pause()
        return

    print()
    for number, name in enumerate(sellable, start=1):
        print(item_color(name) + f"  {number}. {name} x{player.inventory[name]}"
              + Fore.YELLOW + f" - sells for {sell_price(name)} gold")
    print(Fore.WHITE + "  0. Cancel")

    choice = ask_number("Sell which item? ", 0, len(sellable))
    if choice == 0:
        return

    name = sellable[choice - 1]
    remove_item(player, name)
    player.gold += sell_price(name)
    print(Fore.GREEN + f"You sold a {name} for {sell_price(name)} gold.")
    pause()


def open_shop(player):
    """Shop menu loop. Called when the player walks into the $ tile."""
    while True:
        clear_screen()
        print(Fore.YELLOW + Style.BRIGHT + "=== GRETA'S GENERAL STORE ===")
        print(Fore.WHITE + "\"Welcome, welcome! Have a look around.\"")
        print()
        print(Fore.YELLOW + f"Your gold: {player.gold}")
        print()
        print(Fore.WHITE + "1. Buy")
        print(Fore.WHITE + "2. Sell")
        print(Fore.WHITE + "3. Leave")

        choice = ask_number("Choose: ", 1, 3)
        if choice == 1:
            buy_menu(player)
        elif choice == 2:
            sell_menu(player)
        else:
            return
