"""
combat.py
Turn-based battles.

Each turn:
  1. The player picks Attack / Skill / Item / Run.
  2. If the monster is still alive, it attacks (unless it is frozen).
  3. Skill cooldowns go down by 1.

battle() returns "win", "lose" or "flee" so game.py knows what to do next.
"""

import random

from colorama import Fore, Style

from inventory import add_item, use_item_menu
from quest import on_monster_killed
from skill import get_skill
from utils import ask_number, clear_screen, pause


def hp_bar(current, maximum, color):
    """Make a bar like [##########----------] for HP."""
    length = 20
    filled = int(length * current / maximum)
    return color + "[" + "#" * filled + "-" * (length - filled) + "]"


def draw_battle(player, monster, log):
    """Draw the battle screen: both HP bars and the last few messages."""
    clear_screen()
    print(Fore.RED + Style.BRIGHT + "=" * 46)
    print(Fore.RED + Style.BRIGHT + "BATTLE!".center(46))
    print(Fore.RED + Style.BRIGHT + "=" * 46)
    print()
    print(Fore.CYAN + Style.BRIGHT + f"{player.username} (Lv {player.level})")
    print(hp_bar(player.hp, player.max_hp, Fore.GREEN) + Fore.WHITE + f" {player.hp}/{player.max_hp} HP")
    print()
    print(Fore.RED + Style.BRIGHT + monster.name + (Fore.CYAN + "  (FROZEN)" if monster.frozen else ""))
    print(hp_bar(monster.hp, monster.max_hp, Fore.RED) + Fore.WHITE + f" {monster.hp}/{monster.max_hp} HP")
    print()
    print(Fore.WHITE + "-" * 46)
    # Only show the last 5 messages so the screen doesn't get too long
    for line in log[-5:]:
        print(line)
    print(Fore.WHITE + "-" * 46)


def choose_skill(player, cooldowns):
    """Show the skill list. Returns the chosen Skill object, or None to cancel."""
    print()
    for number, name in enumerate(player.skills, start=1):
        skill = get_skill(name)
        if cooldowns[name] > 0:
            print(Fore.LIGHTBLACK_EX + f"  {number}. {name} (ready in {cooldowns[name]} turns)")
        else:
            print(Fore.GREEN + f"  {number}. {name}" + Fore.WHITE + f" - {skill.description}")
    print(Fore.WHITE + "  0. Cancel")

    choice = ask_number("Use which skill? ", 0, len(player.skills))
    if choice == 0:
        return None

    name = player.skills[choice - 1]
    if cooldowns[name] > 0:
        print(Fore.RED + f"{name} is still cooling down!")
        pause()
        return None
    return get_skill(name)


def give_rewards(player, monster):
    """XP, gold and item drops after a win. Also updates quests."""
    messages = [Fore.GREEN + Style.BRIGHT + f"You defeated the {monster.name}!"]

    gold = monster.roll_gold()
    player.gold += gold
    messages.append(Fore.YELLOW + f"You found {gold} gold.")

    for item_name in monster.roll_drops():
        add_item(player, item_name)
        messages.append(Fore.MAGENTA + f"The {monster.name} dropped: {item_name}")

    messages.extend(on_monster_killed(player, monster))
    messages.extend(player.gain_xp(monster.xp_reward))
    return messages


def battle(player, monster, can_run=True):
    """Fight until someone wins or the player runs away."""
    # Every skill starts ready (0 turns to wait) at the start of each battle
    cooldowns = {name: 0 for name in player.skills}
    log = [Fore.RED + f"A {monster.name} appears!"]

    while True:
        draw_battle(player, monster, log)
        print(Fore.WHITE + "1. Attack   2. Skill   3. Item   4. Run")
        choice = ask_number("Choose an action: ", 1, 4)

        used_skill = None
        action_message = None   # stays None if the player cancels a menu

        if choice == 1:
            # Basic attack with a little randomness
            damage = monster.take_damage(player.attack + random.randint(-2, 2))
            action_message = Fore.CYAN + f"You hit the {monster.name} for {damage} damage."

        elif choice == 2:
            used_skill = choose_skill(player, cooldowns)
            if used_skill:
                action_message = used_skill.use(player, monster)

        elif choice == 3:
            action_message = use_item_menu(player)

        elif choice == 4:
            if not can_run:
                log.append(Fore.RED + "You can't run from the Dark Lord!")
                continue
            if random.random() < 0.5:
                return "flee"
            action_message = Fore.RED + "You tried to run but couldn't get away!"

        # The player cancelled a menu, so no turn was used
        if action_message is None:
            continue
        log.append(action_message)

        # ---- Did the monster die? ----
        if not monster.is_alive():
            draw_battle(player, monster, log)
            print()
            for line in give_rewards(player, monster):
                print(line)
            print()
            pause()
            return "win"

        # ---- Monster's turn ----
        if monster.frozen:
            log.append(Fore.CYAN + f"The {monster.name} is frozen solid and can't move!")
            monster.frozen = False
        else:
            log.append(monster.attack_player(player))

        # ---- Did the player die? ----
        if not player.is_alive():
            draw_battle(player, monster, log)
            print()
            print(Fore.RED + Style.BRIGHT + "You have been defeated...")
            pause()
            return "lose"

        # ---- Lower every cooldown by 1, then start the skill just used ----
        for name in cooldowns:
            if cooldowns[name] > 0:
                cooldowns[name] -= 1
        if used_skill:
            cooldowns[used_skill.name] = used_skill.cooldown
