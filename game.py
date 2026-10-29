"""
game.py
The main game loop: draw the map, read a key, move the player, and handle
whatever the player walks into (NPC, shop, chest, portal, monster, boss).
"""

from colorama import Fore, Style

import game_map
from combat import battle
from database import save_player
from inventory import add_item, has_item, show_inventory_screen
from monster import Boss, random_monster
from npc import talk_to_npc
from quest import show_quest_log
from shop import open_shop
from skill import show_skills_screen
from story import show_victory
from utils import clear_screen, get_key, pause

# Key -> (change in row, change in column)
MOVES = {
    "w": (-1, 0),   # up
    "s": (1, 0),    # down
    "a": (0, -1),   # left
    "d": (0, 1),    # right
}


def play(player):
    """Run the game until the player presses Q."""
    message = Fore.WHITE + "Use W A S D to move."

    while True:
        game_map.draw_map(player, message)
        key = get_key()
        message = ""

        if key in MOVES:
            d_row, d_col = MOVES[key]
            message = try_move(player, d_row, d_col)
        elif key == "i":
            show_inventory_screen(player)
        elif key == "c":
            player.show_progress()
        elif key == "k":
            show_skills_screen(player)
        elif key == "j":
            show_quest_log(player)
        elif key == "q":
            save_player(player)
            clear_screen()
            print(Fore.GREEN + "Game saved! Log back in any time to continue.")
            pause()
            return
        else:
            message = Fore.RED + "Invalid key! Use W/A/S/D to move, or I, C, K, J, Q."


def try_move(player, d_row, d_col):
    """Try to step one tile. Returns a message to show under the map."""
    new_row = player.row + d_row
    new_col = player.col + d_col
    tile = game_map.get_tile(player.current_map, new_row, new_col)

    # Walls, trees, rocks, edge of the map
    if tile in game_map.BLOCKED:
        return Fore.RED + f"You bump into {game_map.BLOCKED[tile]}."

    # NPCs, the shop, chests and the boss work like "bumping" into them:
    # the player does not move onto the tile.
    if tile.isdigit():
        talk_to_npc(player, tile)
        return ""
    if tile == "$":
        open_shop(player)
        return Fore.YELLOW + "\"Come back soon!\""
    if tile == "C":
        return open_chest(player, new_row, new_col)
    if tile == "B":
        return fight_boss(player)

    # These tiles DO move the player
    if tile == "O":
        return use_portal(player, new_row, new_col)
    if tile == "M":
        return fight_monster(player, new_row, new_col)

    # Plain ground: just move
    player.row = new_row
    player.col = new_col
    return ""


def open_chest(player, row, col):
    """Give the player the chest's gold and items (only the first time)."""
    messages = []

    # Special case: the forest chest holds Lily's locket while her quest is active.
    # This is checked separately so you can still get the locket even if you
    # already looted the chest before taking the quest.
    if (player.current_map == "forest" and player.quests["locket_quest"] == "active"
            and not has_item(player, "Silver Locket")):
        add_item(player, "Silver Locket")
        messages.append(Fore.MAGENTA + Style.BRIGHT + "You found a Silver Locket! Bring it back to Lily.")

    # JSON (TinyDB) can't store tuples, so each chest is remembered as a
    # string like "village,5,5"
    chest_id = f"{player.current_map},{row},{col}"
    if chest_id not in player.opened_chests:
        player.opened_chests.append(chest_id)
        contents = game_map.CHESTS[(player.current_map, row, col)]

        player.gold += contents["gold"]
        found = [f"{contents['gold']} gold"]
        for item_name, amount in contents["items"].items():
            add_item(player, item_name, amount)
            found.append(f"{item_name} x{amount}")

        messages.append(Fore.YELLOW + Style.BRIGHT + "You open the chest and find: " + ", ".join(found))
        save_player(player)

    if not messages:
        return Fore.LIGHTBLACK_EX + "The chest is empty."
    # Join with a newline so each message shows on its own line under the map
    return "\n".join(messages)


def use_portal(player, row, col):
    """Move the player to another map."""
    dest_map, dest_row, dest_col = game_map.PORTALS[(player.current_map, row, col)]

    # The cave stays locked until Hermit Mara breaks the seal (main quest step 3)
    if dest_map == "cave" and player.quests["main_step"] < 3:
        return Fore.MAGENTA + "A dark seal blocks the cave. Maybe someone in the forest can break it..."

    player.current_map = dest_map
    player.row = dest_row
    player.col = dest_col
    save_player(player)   # auto-save every time you change maps
    return Fore.LIGHTCYAN_EX + Style.BRIGHT + f"You travel to the {game_map.MAPS[dest_map]['title']}."


def fight_monster(player, row, col):
    monster = random_monster(player.current_map)
    result = battle(player, monster)

    if result == "win":
        # Step onto the monster's spot
        player.row = row
        player.col = col
        save_player(player)
        return Fore.GREEN + f"The {monster.name} is defeated."
    if result == "flee":
        return Fore.YELLOW + "You got away safely."
    return handle_defeat(player)


def fight_boss(player):
    step = player.quests["main_step"]
    if step < 3:
        return Fore.MAGENTA + "A terrible presence... you are not ready to face it."
    if step == 4:
        return Fore.LIGHTBLACK_EX + "The Dark Lord's throne sits empty."

    result = battle(player, Boss(), can_run=False)
    if result == "win":
        save_player(player)
        show_victory(player)
        return Fore.MAGENTA + Style.BRIGHT + "Peace has returned to Elderwood!"
    return handle_defeat(player)


def handle_defeat(player):
    """After losing: lose 1/4 of your gold, wake up in the village with half HP."""
    lost_gold = player.gold // 4
    player.gold -= lost_gold
    player.hp = player.max_hp // 2
    player.current_map, player.row, player.col = game_map.START
    save_player(player)

    clear_screen()
    print(Fore.RED + "Everything goes dark...")
    print(Fore.WHITE + "You wake up back in Elderwood Village.")
    print(Fore.YELLOW + f"You lost {lost_gold} gold.")
    pause()
    return Fore.RED + "Rest up and buy potions before trying again!"
