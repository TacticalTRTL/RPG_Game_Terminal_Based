"""
quest.py
Quest progress is stored in a simple dictionary on the player (player.quests)
so it is easy to save to TinyDB.

MAIN QUEST - "The Dark Lord" (main_step goes 0 -> 4)
  0: Talk to Elder Rowan
  1: Defeat 3 monsters in the forest
  2: Find Hermit Mara in the forest (she breaks the cave seal)
  3: Defeat the Dark Lord in the Shadow Cave   <- FINAL BOSS
  4: Done - you won!

SIDE QUEST 1 - "Slime Trouble" (Farmer Bob): defeat 3 Slimes -> 50 gold
SIDE QUEST 2 - "The Lost Locket" (Lily): find the locket in a forest chest
                                         -> 40 XP + 2 Potions
Side quest status is one of: "not_started", "active", "done"
"""

from colorama import Fore, Style

from utils import clear_screen, pause

MAIN_STEPS = [
    "Talk to Elder Rowan in Elderwood Village.",
    "Defeat 3 monsters in the Whispering Forest.",
    "Find Hermit Mara in the Whispering Forest.",
    "Enter the Shadow Cave and defeat the Dark Lord!",
    "Quest complete - Elderwood is saved!",
]

KILLS_NEEDED_MAIN = 3
SLIMES_NEEDED = 3


def new_quest_state():
    """Quest progress for a brand-new character."""
    return {
        "main_step": 0,
        "main_kills": 0,
        "slime_quest": "not_started",
        "slime_kills": 0,
        "locket_quest": "not_started",
    }


def current_objective(player):
    """One line describing what the player should do next for the main quest."""
    q = player.quests
    text = MAIN_STEPS[q["main_step"]]
    if q["main_step"] == 1:
        text += f" ({q['main_kills']}/{KILLS_NEEDED_MAIN})"
    return text


def on_monster_killed(player, monster):
    """Called by combat.py after every win. Updates quests, returns messages."""
    q = player.quests
    messages = []

    # Main quest step 1: any monster counts
    if q["main_step"] == 1:
        q["main_kills"] += 1
        if q["main_kills"] >= KILLS_NEEDED_MAIN:
            q["main_step"] = 2
            messages.append(Fore.CYAN + Style.BRIGHT
                            + "MAIN QUEST: The forest is safer! Now find Hermit Mara.")
        else:
            messages.append(Fore.CYAN + f"Main quest: {q['main_kills']}/{KILLS_NEEDED_MAIN} monsters defeated.")

    # Side quest: Slime Trouble
    if q["slime_quest"] == "active" and monster.name == "Slime":
        if q["slime_kills"] < SLIMES_NEEDED:
            q["slime_kills"] += 1
            messages.append(Fore.YELLOW + f"Slime Trouble: {q['slime_kills']}/{SLIMES_NEEDED} Slimes.")
            if q["slime_kills"] == SLIMES_NEEDED:
                messages.append(Fore.YELLOW + "Go back to Farmer Bob for your reward!")

    # Final step: the boss
    if monster.name == "Dark Lord":
        q["main_step"] = 4

    return messages


def show_quest_log(player):
    """Quest screen opened with the J key on the map."""
    q = player.quests
    clear_screen()
    print(Fore.CYAN + Style.BRIGHT + "=== QUEST LOG ===")
    print()

    # Main quest: show finished steps in green, current in yellow, future hidden
    print(Fore.CYAN + Style.BRIGHT + "MAIN QUEST: The Dark Lord")
    for number, step in enumerate(MAIN_STEPS[:4]):
        if number < q["main_step"]:
            print(Fore.GREEN + f"  [X] {step}")
        elif number == q["main_step"]:
            print(Fore.YELLOW + f"  [ ] {current_objective(player)}")
        else:
            print(Fore.LIGHTBLACK_EX + "  [ ] ???")
    if q["main_step"] == 4:
        print(Fore.MAGENTA + Style.BRIGHT + "  COMPLETE - you saved Elderwood!")
    print()

    # Side quests
    print(Fore.YELLOW + Style.BRIGHT + "SIDE QUESTS")
    slime = q["slime_quest"]
    if slime == "not_started":
        print(Fore.LIGHTBLACK_EX + "  Slime Trouble - talk to Farmer Bob in the village")
    elif slime == "active":
        print(Fore.YELLOW + f"  Slime Trouble - defeat Slimes ({q['slime_kills']}/{SLIMES_NEEDED}), then see Bob")
    else:
        print(Fore.GREEN + "  Slime Trouble - DONE")

    locket = q["locket_quest"]
    if locket == "not_started":
        print(Fore.LIGHTBLACK_EX + "  The Lost Locket - talk to Lily in the village")
    elif locket == "active":
        print(Fore.YELLOW + "  The Lost Locket - find the locket in a forest chest, return it to Lily")
    else:
        print(Fore.GREEN + "  The Lost Locket - DONE")
    print()
    pause()
