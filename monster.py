"""
monster.py
Monsters use INHERITANCE:

    Monster        <- parent class (HP, attack, rewards, basic attack)
     |- Slime      <- weak, sometimes just wobbles and misses
     |- Goblin     <- sometimes attacks TWICE
     |- Wolf       <- sometimes does a strong bite (1.5x damage)
     |- Skeleton   <- high defense, bone throw ignores your defense
     |- Orc        <- big HP, sometimes goes into a rage (2x damage)
     |- Boss       <- the Dark Lord: Dark Blast every 3rd turn, heals once

Each child calls super().__init__() with different stats, and most of them
OVERRIDE attack_player() to get their own special behavior.
"""

import random

from colorama import Fore, Style


class Monster:
    """Parent class for every monster."""

    def __init__(self, name, max_hp, attack, defense, xp_reward, gold_min, gold_max, drops):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.xp_reward = xp_reward
        self.gold_min = gold_min
        self.gold_max = gold_max
        # drops is a list of (item name, chance from 0.0 to 1.0)
        self.drops = drops
        # Set to True by the Ice Shard skill -> monster skips its next turn
        self.frozen = False

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount, ignore_defense=False):
        """Lower HP. Defense reduces the damage unless ignore_defense is True.
        Always does at least 1 damage. Returns the damage actually done."""
        if ignore_defense:
            damage = amount
        else:
            damage = amount - self.defense
        damage = max(1, damage)
        self.hp = max(0, self.hp - damage)
        return damage

    def hit_player(self, player, multiplier=1.0, ignore_defense=False):
        """Helper used by every monster: work out damage and hurt the player."""
        raw = int((self.attack + random.randint(-1, 2)) * multiplier)
        if ignore_defense:
            damage = max(1, raw)
        else:
            damage = max(1, raw - player.defense)
        player.take_damage(damage)
        return damage

    def attack_player(self, player):
        """Normal attack. Child classes override this for special behavior."""
        damage = self.hit_player(player)
        return Fore.RED + f"The {self.name} attacks you for {damage} damage."

    def roll_gold(self):
        return random.randint(self.gold_min, self.gold_max)

    def roll_drops(self):
        """Return a list of item names this monster dropped."""
        dropped = []
        for item_name, chance in self.drops:
            if random.random() < chance:
                dropped.append(item_name)
        return dropped


# ------------------------------------------------------------
# Regular monsters
# ------------------------------------------------------------

class Slime(Monster):
    def __init__(self):
        super().__init__("Slime", max_hp=20, attack=5, defense=1, xp_reward=12,
                         gold_min=3, gold_max=8,
                         drops=[("Slime Gel", 0.6), ("Potion", 0.15)])

    def attack_player(self, player):
        # 20% chance the slime just wobbles around and misses
        if random.random() < 0.2:
            return Fore.GREEN + "The Slime wobbles around harmlessly."
        return super().attack_player(player)


class Goblin(Monster):
    def __init__(self):
        super().__init__("Goblin", max_hp=28, attack=7, defense=2, xp_reward=18,
                         gold_min=6, gold_max=12,
                         drops=[("Goblin Ear", 0.5), ("Potion", 0.2)])

    def attack_player(self, player):
        # 25% chance to stab twice
        if random.random() < 0.25:
            first = self.hit_player(player)
            second = self.hit_player(player)
            return Fore.RED + f"The Goblin stabs TWICE for {first} + {second} damage!"
        return super().attack_player(player)


class Wolf(Monster):
    def __init__(self):
        super().__init__("Wolf", max_hp=32, attack=9, defense=2, xp_reward=22,
                         gold_min=5, gold_max=10,
                         drops=[("Wolf Pelt", 0.5), ("Potion", 0.15)])

    def attack_player(self, player):
        # 30% chance of a savage bite (1.5x damage)
        if random.random() < 0.3:
            damage = self.hit_player(player, multiplier=1.5)
            return Fore.RED + Style.BRIGHT + f"The Wolf's SAVAGE BITE does {damage} damage!"
        return super().attack_player(player)


class Skeleton(Monster):
    def __init__(self):
        super().__init__("Skeleton", max_hp=45, attack=12, defense=6, xp_reward=35,
                         gold_min=12, gold_max=20,
                         drops=[("Old Bone", 0.5), ("Hi-Potion", 0.15)])

    def attack_player(self, player):
        # 25% chance to throw a bone that ignores your defense
        if random.random() < 0.25:
            damage = self.hit_player(player, ignore_defense=True)
            return Fore.RED + f"The Skeleton throws a BONE for {damage} damage (ignores defense)!"
        return super().attack_player(player)


class Orc(Monster):
    def __init__(self):
        super().__init__("Orc", max_hp=60, attack=15, defense=5, xp_reward=45,
                         gold_min=15, gold_max=28,
                         drops=[("Orc Tusk", 0.5), ("Hi-Potion", 0.2)])

    def attack_player(self, player):
        # 20% chance to rage for double damage
        if random.random() < 0.2:
            damage = self.hit_player(player, multiplier=2.0)
            return Fore.RED + Style.BRIGHT + f"The Orc goes into a RAGE and smashes you for {damage}!"
        return super().attack_player(player)


# ------------------------------------------------------------
# Final Boss
# ------------------------------------------------------------

class Boss(Monster):
    """The Dark Lord. Defeating him wins the game."""

    def __init__(self):
        super().__init__("Dark Lord", max_hp=200, attack=18, defense=8, xp_reward=200,
                         gold_min=200, gold_max=200, drops=[])
        self.turn = 0              # counts the boss's turns
        self.has_healed = False    # the boss can only heal once

    def attack_player(self, player):
        self.turn += 1

        # Once, when below 30% HP, the boss heals itself instead of attacking
        if self.hp < self.max_hp * 0.3 and not self.has_healed:
            self.has_healed = True
            self.hp = min(self.max_hp, self.hp + 30)
            return Fore.MAGENTA + Style.BRIGHT + "The Dark Lord drinks shadow energy and heals 30 HP!"

        # Every 3rd turn: Dark Blast (2x damage, ignores defense)
        if self.turn % 3 == 0:
            damage = self.hit_player(player, multiplier=2.0, ignore_defense=True)
            return Fore.MAGENTA + Style.BRIGHT + f"DARK BLAST! You take {damage} damage!"

        return super().attack_player(player)


# Which monsters can appear on each map
MONSTERS_BY_MAP = {
    "forest": [Slime, Goblin, Wolf],
    "cave": [Skeleton, Orc],
}


def random_monster(map_name):
    """Pick a random monster CLASS for this map and create one (the () at the end)."""
    monster_class = random.choice(MONSTERS_BY_MAP[map_name])
    return monster_class()
