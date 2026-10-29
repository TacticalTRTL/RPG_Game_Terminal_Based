"""
game_map.py
The three maps, the portals between them, and the code that draws the map.

(Named game_map.py instead of map.py because "map" is already a built-in
Python function and we don't want to hide it.)

Map legend (the letters used in the map strings below):
  #  wall        (blocks you)
  T  tree        (blocks you)
  R  rock        (blocks you)
  (space)        outside the map (blocks you) - lets maps have odd shapes
  .  ground
  M  monster     (walk into it to fight)
  B  boss        (the Dark Lord)
  $  shop
  C  chest
  O  portal to another map
  1-5  NPCs
  The player is only drawn on screen, never stored in the map.

The letters are swapped for emoji when the map is drawn (see TILE_EMOJI).
"""

from colorama import Fore, Style

from quest import current_objective
from utils import clear_screen

MAPS = {
    "village": {
        "title": "ELDERWOOD VILLAGE",
        "tiles": [
            "     ###############",
            "     #..T......T...#",
            "######...1.........#####",
            "#.............$........#",
            "#...####...........2...O",
            "#...#C.#..T............#",
            "#...#..#.......3.....###",
            "######..............#",
            "     #..T...........#",
            "     ################",
        ],
    },
    "forest": {
        "title": "WHISPERING FOREST",
        "tiles": [
            "  ####################",
            "  #..T....M.....T...C#",
            "###..TT.......TT..M..#",
            "O.......4...........T#",
            "###..M.....TTT.......#",
            "  #......T..T.T...M..####",
            "  #..TT........T....5....O",
            "  ##..M....##......TT..###",
            "   #......####..M......#",
            "   #####################",
        ],
    },
    "cave": {
        "title": "SHADOW CAVE",
        "tiles": [
            "##########################",
            "#....R.....#.....R....M..#",
            "O..M...R...#..M..........#",
            "#......#.......#####..R..#",
            "####...#...R...#.C.#.....#",
            "   #...#####...#.B.......#",
            "   #..M.......R#...#..M..#",
            "   #######################",
        ],
    },
}

# Portals: (map, row, col) of the O tile -> (destination map, row, col to appear at)
PORTALS = {
    ("village", 4, 23): ("forest", 3, 1),    # village east exit -> forest west side
    ("forest", 3, 0): ("village", 4, 22),    # forest west exit  -> back to village
    ("forest", 6, 25): ("cave", 2, 1),       # forest east exit  -> cave
    ("cave", 2, 0): ("forest", 6, 24),       # cave exit         -> back to forest
}

# What's inside each chest: (map, row, col) -> gold and items.
# Each chest can only be looted once (player.opened_chests remembers which).
CHESTS = {
    ("village", 5, 5): {"gold": 30, "items": {"Potion": 2}},
    ("forest", 1, 20): {"gold": 25, "items": {"Strength Tonic": 1}},   # also holds Lily's locket
    ("cave", 4, 17): {"gold": 50, "items": {"Hi-Potion": 2, "Iron Skin Elixir": 1}},
}

# Where new players start, and where you wake up after losing a battle
START = ("village", 3, 2)

# Tiles you can't walk onto, and what to call them in messages
BLOCKED = {
    "#": "a wall",
    "T": "a tree",
    "R": "a rock",
    " ": "the edge of the world",
}

# The maps above are still written with letters because they're easy to edit.
# When drawing, each letter is swapped for an emoji from this dictionary.
# (Only simple one-character emoji are used - fancy combined emoji can
#  break the spacing in some terminals.)
PLAYER_EMOJI = "🤺"
NPC_EMOJI = "🧙"
TILE_EMOJI = {
    "#": "🧱",   # wall
    "T": "🌲",   # tree
    "R": "🗿",   # rock
    "M": "👹",   # monster
    "B": "🐲",   # boss
    "$": "🏪",   # shop
    "C": "📦",   # chest
    "O": "🚪",   # portal / exit
}


def get_tile(map_name, row, col):
    """Return the tile at (row, col). Anything outside the map counts as ' '."""
    tiles = MAPS[map_name]["tiles"]
    if row < 0 or row >= len(tiles):
        return " "
    if col < 0 or col >= len(tiles[row]):
        return " "
    return tiles[row][col]


def tile_to_text(tile):
    """
    Turn one map letter into what gets printed on screen.
    An emoji is about 2 terminal columns wide, so plain text tiles get
    a space after them ("." -> ". ") to take up the same 2 columns.
    That keeps every row lined up.
    """
    if tile.isdigit():
        return NPC_EMOJI            # NPCs are stored as 1-5 but all look like a wizard
    if tile in TILE_EMOJI:
        return TILE_EMOJI[tile]
    if tile == ".":
        return Fore.LIGHTBLACK_EX + ". "   # dim gray ground
    return "  "                     # a space = outside the map, just blank


def draw_map(player, message=""):
    """Clear the screen and draw the current map, stats, legend and message."""
    clear_screen()
    data = MAPS[player.current_map]

    print(Fore.CYAN + Style.BRIGHT + f"=== {data['title']} ===")
    print()

    for row_number, row in enumerate(data["tiles"]):
        line = ""
        for col_number, tile in enumerate(row):
            if row_number == player.row and col_number == player.col:
                line += PLAYER_EMOJI
            else:
                line += tile_to_text(tile)
        print(line)

    print()
    # Status bar
    print(Fore.WHITE + f"{player.username}  "
          + Fore.YELLOW + f"Lv {player.level}  "
          + Fore.GREEN + f"HP {player.hp}/{player.max_hp}  "
          + Fore.CYAN + f"XP {player.xp}/{player.xp_to_next_level()}  "
          + Fore.YELLOW + f"Gold {player.gold}")
    print(Fore.CYAN + "Quest: " + current_objective(player))
    print()
    # Legend
    print(Fore.WHITE + f"{PLAYER_EMOJI} You  {NPC_EMOJI} NPC  {TILE_EMOJI['M']} Monster  "
          f"{TILE_EMOJI['B']} Boss  {TILE_EMOJI['$']} Shop  {TILE_EMOJI['C']} Chest  "
          f"{TILE_EMOJI['O']} Exit")
    print(Fore.WHITE + f"{TILE_EMOJI['#']} Wall  {TILE_EMOJI['T']} Tree  {TILE_EMOJI['R']} Rock")
    print(Fore.WHITE + "WASD=Move  I=Inventory  C=Character  K=Skills  J=Quests  Q=Save & Quit")

    if message:
        print()
        print(message)
