"""
player.py
The Player class holds everything about the character:
HP, XP, level, gold, attack/defense, skills, inventory, location and quests.

to_dict() / from_dict() turn the player into a plain dictionary and back.
TinyDB can only store dictionaries, so that is how we save and load.
"""

from colorama import Fore, Style

import game_map
from quest import current_objective, new_quest_state
from skill import LEARN_AT_LEVEL
from utils import clear_screen, pause


class Player:
    def __init__(self, username):
        self.username = username
        self.level = 1
        self.xp = 0
        self.max_hp = 50
        self.hp = 50
        self.attack = 8
        self.defense = 3
        self.gold = 30
        self.skills = ["Power Strike"]          # skill NAMES (strings)
        self.inventory = {"Potion": 2}          # {item name: count}
        # Location: which map, and row/col on that map
        self.current_map, self.row, self.col = game_map.START
        self.quests = new_quest_state()
        self.opened_chests = []                 # chests already looted, like "village,5,5"

    # ---------------- HP ----------------

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        """Heal without going over max HP. Returns how much was actually healed."""
        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - old_hp

    # ---------------- XP & levels ----------------

    def xp_to_next_level(self):
        """Level 1 needs 50 XP, level 2 needs 100 XP, level 3 needs 150..."""
        return self.level * 50

    def gain_xp(self, amount):
        """Add XP and level up (possibly more than once). Returns messages."""
        messages = [Fore.CYAN + f"You gain {amount} XP."]
        self.xp += amount

        # "while" instead of "if" in case a big XP reward gives 2 levels at once
        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            messages.extend(self.level_up())
        return messages

    def level_up(self):
        self.level += 1
        self.max_hp += 12
        self.attack += 3
        self.defense += 2
        self.hp = self.max_hp     # full heal on level up
        messages = [Fore.YELLOW + Style.BRIGHT
                    + f"*** LEVEL UP! You are now level {self.level}! (HP, Attack, Defense up) ***"]

        # Learn a new skill if this level unlocks one
        if self.level in LEARN_AT_LEVEL:
            new_skill = LEARN_AT_LEVEL[self.level]
            if new_skill not in self.skills:
                self.skills.append(new_skill)
                messages.append(Fore.MAGENTA + Style.BRIGHT + f"You learned a new skill: {new_skill}!")
        return messages

    # ---------------- Saving / loading ----------------

    def to_dict(self):
        """Turn the player into a dictionary so TinyDB can save it."""
        return {
            "username": self.username,
            "level": self.level,
            "xp": self.xp,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "gold": self.gold,
            "skills": self.skills,
            "inventory": self.inventory,
            "current_map": self.current_map,
            "row": self.row,
            "col": self.col,
            "quests": self.quests,
            "opened_chests": self.opened_chests,
        }

    @classmethod
    def from_dict(cls, data):
        """Build a Player from a saved dictionary (the opposite of to_dict)."""
        player = cls(data["username"])
        for key, value in data.items():
            setattr(player, key, value)   # setattr(player, "gold", 50) is the same as player.gold = 50
        return player

    # ---------------- Character screen ----------------

    def show_progress(self):
        """Character screen opened with the C key on the map."""
        clear_screen()
        needed = self.xp_to_next_level()
        filled = int(20 * self.xp / needed)
        xp_bar = "#" * filled + "-" * (20 - filled)

        print(Fore.CYAN + Style.BRIGHT + "=== CHARACTER ===")
        print()
        print(Fore.WHITE + f"Name:     {self.username}")
        print(Fore.YELLOW + f"Level:    {self.level}")
        print(Fore.CYAN + f"XP:       {self.xp}/{needed}  [{xp_bar}]")
        print(Fore.GREEN + f"HP:       {self.hp}/{self.max_hp}")
        print(Fore.RED + f"Attack:   {self.attack}")
        print(Fore.BLUE + f"Defense:  {self.defense}")
        print(Fore.YELLOW + f"Gold:     {self.gold}")
        print()
        print(Fore.MAGENTA + "Skills:   " + ", ".join(self.skills))
        item_count = sum(self.inventory.values())
        print(Fore.MAGENTA + f"Items:    {item_count} (press I on the map to see them)")
        print()
        print(Fore.WHITE + f"Location: {game_map.MAPS[self.current_map]['title']}")
        print(Fore.WHITE + f"Quest:    {current_objective(self)}")
        print()
        pause()
