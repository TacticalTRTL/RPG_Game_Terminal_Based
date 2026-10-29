"""
skill.py
Skills use INHERITANCE:

    Skill            <- parent class (name, description, cooldown)
     |- PowerStrike  <- big physical hit
     |- Fireball     <- magic damage that ignores defense
     |- Heal         <- restores HP
     |- IceShard     <- damage + freezes the monster for one turn

Every child class calls super().__init__() to set the shared stats,
then OVERRIDES use() to give the skill its own effect.

Cooldown = how many turns you must wait before using the skill again.
"""

from colorama import Fore, Style

from utils import clear_screen, pause


class Skill:
    """Parent class for every skill."""

    def __init__(self, name, description, cooldown):
        self.name = name
        self.description = description
        self.cooldown = cooldown

    def use(self, player, monster):
        """Child classes replace this. Returns a message describing what happened."""
        return "Nothing happens."


class PowerStrike(Skill):
    def __init__(self):
        super().__init__("Power Strike", "A heavy blow that does 2x your Attack.", 2)

    def use(self, player, monster):
        damage = monster.take_damage(player.attack * 2)
        return Fore.YELLOW + f"POWER STRIKE! The {monster.name} takes {damage} damage."


class Fireball(Skill):
    def __init__(self):
        super().__init__("Fireball", "12 + Attack fire damage. Ignores defense.", 3)

    def use(self, player, monster):
        damage = monster.take_damage(12 + player.attack, ignore_defense=True)
        return Fore.RED + Style.BRIGHT + f"FIREBALL! The {monster.name} burns for {damage} damage."


class Heal(Skill):
    def __init__(self):
        super().__init__("Heal", "Restore 40% of your max HP.", 4)

    def use(self, player, monster):
        healed = player.heal(int(player.max_hp * 0.4))
        return Fore.GREEN + Style.BRIGHT + f"HEAL! You recover {healed} HP."


class IceShard(Skill):
    def __init__(self):
        super().__init__("Ice Shard", "Attack + 4 damage and FREEZES the monster for 1 turn.", 4)

    def use(self, player, monster):
        damage = monster.take_damage(player.attack + 4)
        monster.frozen = True   # combat.py checks this and skips the monster's turn
        return Fore.CYAN + Style.BRIGHT + f"ICE SHARD! {damage} damage and the {monster.name} is frozen!"


# One object of each skill, looked up by name.
# The player only saves skill NAMES (strings) in the database,
# and we use this dictionary to get the real skill object back.
ALL_SKILLS = {
    "Power Strike": PowerStrike(),
    "Fireball": Fireball(),
    "Heal": Heal(),
    "Ice Shard": IceShard(),
}

# Which level the player must reach to learn each skill
LEARN_AT_LEVEL = {
    2: "Fireball",
    3: "Heal",
    4: "Ice Shard",
}


def get_skill(name):
    return ALL_SKILLS[name]


def show_skills_screen(player):
    """Skills screen opened with the K key on the map."""
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "=== SKILLS ===")
    print()
    print(Fore.WHITE + "Learned:")
    for name in player.skills:
        skill = get_skill(name)
        print(Fore.GREEN + f"  {skill.name}" + Fore.WHITE
              + f" (cooldown {skill.cooldown}) - {skill.description}")

    print()
    print(Fore.WHITE + "Not learned yet:")
    for level, name in LEARN_AT_LEVEL.items():
        if name not in player.skills:
            print(Fore.LIGHTBLACK_EX + f"  {name} - learned at level {level}")
    print()
    pause()
