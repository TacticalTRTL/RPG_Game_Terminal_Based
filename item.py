"""
item.py
Every item in the game is described here in one dictionary.

Item "types":
  heal    -> restores HP when used
  attack  -> permanently raises Attack when used
  defense -> permanently raises Defense when used
  loot    -> dropped by monsters, only useful for selling
  quest   -> needed for a quest, cannot be used or sold
"""

from colorama import Fore

ITEMS = {
    # ---- Things you can buy in the shop ----
    "Potion": {
        "type": "heal", "value": 30, "price": 15,
        "description": "Restores 30 HP.",
    },
    "Hi-Potion": {
        "type": "heal", "value": 80, "price": 40,
        "description": "Restores 80 HP.",
    },
    "Strength Tonic": {
        "type": "attack", "value": 2, "price": 60,
        "description": "Permanently raises Attack by 2.",
    },
    "Iron Skin Elixir": {
        "type": "defense", "value": 2, "price": 60,
        "description": "Permanently raises Defense by 2.",
    },

    # ---- Monster drops (sell them for gold) ----
    "Slime Gel":  {"type": "loot", "value": 0, "price": 10, "description": "Sticky goo from a Slime."},
    "Goblin Ear": {"type": "loot", "value": 0, "price": 16, "description": "Proof you beat a Goblin."},
    "Wolf Pelt":  {"type": "loot", "value": 0, "price": 20, "description": "A thick, warm pelt."},
    "Old Bone":   {"type": "loot", "value": 0, "price": 24, "description": "A rattly Skeleton bone."},
    "Orc Tusk":   {"type": "loot", "value": 0, "price": 36, "description": "A huge, heavy tusk."},

    # ---- Quest items ----
    "Silver Locket": {
        "type": "quest", "value": 0, "price": 0,
        "description": "Lily's lost locket. Bring it back to her!",
    },
}

# Items the shop sells (in this order)
SHOP_STOCK = ["Potion", "Hi-Potion", "Strength Tonic", "Iron Skin Elixir"]

# Item types the player is allowed to "use"
USABLE_TYPES = ("heal", "attack", "defense")

# One color per item type so the inventory is easier to read
TYPE_COLORS = {
    "heal": Fore.GREEN,
    "attack": Fore.RED,
    "defense": Fore.BLUE,
    "loot": Fore.LIGHTBLACK_EX,
    "quest": Fore.MAGENTA,
}


def sell_price(item_name):
    """The shop buys items back for half of their price."""
    return ITEMS[item_name]["price"] // 2


def item_color(item_name):
    """Return the color used to display an item."""
    return TYPE_COLORS.get(ITEMS[item_name]["type"], Fore.WHITE)
