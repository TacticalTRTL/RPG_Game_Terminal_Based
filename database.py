"""
database.py
Everything that talks to TinyDB lives here.

TinyDB stores data in a normal JSON file (game_data.json, created next to
this file). It has two "tables":
  users  -> {"username": ..., "password": <hashed password>}
  saves  -> {"username": ..., "data": <player.to_dict()>}
"""

import os

from tinydb import Query, TinyDB

# Put game_data.json in the same folder as this file, no matter which folder
# you run the game from.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_data.json")

db = TinyDB(DB_PATH, indent=2)
users_table = db.table("users")
saves_table = db.table("saves")

# Query() is how TinyDB searches, e.g. User.username == "player1"
User = Query()


# ---------------- Accounts ----------------

def user_exists(username):
    return users_table.contains(User.username == username)


def create_user(username, password_hash):
    users_table.insert({"username": username, "password": password_hash})


def get_user(username):
    """Return the user's record (a dict) or None if not found."""
    return users_table.get(User.username == username)


# ---------------- Game saves ----------------

def save_player(player):
    """Save the player. upsert = update if it exists, insert if it doesn't."""
    saves_table.upsert({"username": player.username, "data": player.to_dict()},
                       User.username == player.username)


def load_player_data(username):
    """Return the saved player dictionary, or None if there is no save yet."""
    record = saves_table.get(User.username == username)
    if record is None:
        return None
    return record["data"]
