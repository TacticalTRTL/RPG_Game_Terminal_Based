"""
npc.py
The 5 NPCs. Each one has its own talk function, and what they say depends
on how far along the quests are.

  1 Elder Rowan  (village) - gives the main quest
  2 Farmer Bob   (village) - side quest "Slime Trouble"
  3 Lily         (village) - side quest "The Lost Locket"
  4 Hermit Mara  (forest)  - breaks the seal on the Shadow Cave
  5 Guard Tom    (forest)  - gives tips about the cave and the boss
"""

from colorama import Fore, Style

from inventory import add_item, has_item, remove_item
from quest import SLIMES_NEEDED
from utils import ask_yes_no, clear_screen, pause


def say(name, text):
    """Print one line of NPC dialogue."""
    print(Fore.YELLOW + Style.BRIGHT + f"{name}: " + Style.RESET_ALL + Fore.WHITE + text)


def talk_elder(player):
    q = player.quests
    name = "Elder Rowan"
    if q["main_step"] == 0:
        say(name, "Ah, a traveler! Thank the stars.")
        say(name, "The Dark Lord has awoken in the Shadow Cave and his monsters fill the forest.")
        say(name, "Go east into the Whispering Forest and defeat 3 monsters to prove yourself.")
        q["main_step"] = 1
        print()
        print(Fore.CYAN + Style.BRIGHT + "MAIN QUEST STARTED: The Dark Lord")
    elif q["main_step"] == 1:
        say(name, f"The forest still crawls with monsters. ({q['main_kills']}/3 defeated)")
    elif q["main_step"] == 2:
        say(name, "Well done! Now find Hermit Mara in the forest. Only she can open the cave.")
    elif q["main_step"] == 3:
        say(name, "The cave is open. Be brave... and bring plenty of potions.")
    else:
        say(name, "You saved us all! Elderwood will sing songs about you.")


def talk_farmer(player):
    q = player.quests
    name = "Farmer Bob"
    if q["slime_quest"] == "not_started":
        say(name, "Those blasted Slimes keep eating my cabbages!")
        say(name, f"Squash {SLIMES_NEEDED} Slimes in the forest and I'll pay you 50 gold.")
        if ask_yes_no("Accept the quest?"):
            q["slime_quest"] = "active"
            q["slime_kills"] = 0
            print(Fore.YELLOW + Style.BRIGHT + "SIDE QUEST STARTED: Slime Trouble")
        else:
            say(name, "Suit yourself. My cabbages will remember this.")
    elif q["slime_quest"] == "active":
        if q["slime_kills"] >= SLIMES_NEEDED:
            say(name, "You did it! My cabbages are safe. Here's your pay!")
            player.gold += 50
            q["slime_quest"] = "done"
            print(Fore.YELLOW + Style.BRIGHT + "SIDE QUEST COMPLETE! +50 gold")
        else:
            say(name, f"Still slimy out there... ({q['slime_kills']}/{SLIMES_NEEDED} Slimes)")
    else:
        say(name, "Best cabbage harvest in years, thanks to you!")


def talk_lily(player):
    q = player.quests
    name = "Lily"
    if q["locket_quest"] == "not_started":
        say(name, "*sniff* I dropped my mother's silver locket in the forest...")
        say(name, "I think a monster put it in a chest. Could you find it?")
        if ask_yes_no("Accept the quest?"):
            q["locket_quest"] = "active"
            print(Fore.YELLOW + Style.BRIGHT + "SIDE QUEST STARTED: The Lost Locket")
        else:
            say(name, "Oh... okay.")
    elif q["locket_quest"] == "active":
        if has_item(player, "Silver Locket"):
            remove_item(player, "Silver Locket")
            say(name, "My locket! Thank you, thank you! Please take these.")
            add_item(player, "Potion", 2)
            print(Fore.YELLOW + Style.BRIGHT + "SIDE QUEST COMPLETE! +2 Potions")
            for line in player.gain_xp(40):
                print(line)
            q["locket_quest"] = "done"
        else:
            say(name, "Please hurry... look for a chest in the forest.")
    else:
        say(name, "I'll never take this locket off again!")


def talk_hermit(player):
    q = player.quests
    name = "Hermit Mara"
    if q["main_step"] < 2:
        say(name, "Hmph. The Elder hasn't sent you, has he? Come back when you've proven yourself.")
    elif q["main_step"] == 2:
        say(name, "So you're the one the Elder trusts. Very well.")
        say(name, "*She waves her staff and the air hums* ... The seal on the Shadow Cave is broken.")
        say(name, "Take this Hi-Potion. You'll need it. The cave is past the east exit.")
        add_item(player, "Hi-Potion")
        q["main_step"] = 3
        print()
        print(Fore.CYAN + Style.BRIGHT + "MAIN QUEST UPDATED: Defeat the Dark Lord!")
    elif q["main_step"] == 3:
        say(name, "What are you waiting for? The Dark Lord grows stronger every day.")
    else:
        say(name, "The darkness is gone. Maybe I'll finally get some sleep.")


def talk_guard(player):
    q = player.quests
    name = "Guard Tom"
    if q["main_step"] < 3:
        say(name, "Halt! The Shadow Cave is sealed by dark magic. Only Hermit Mara can break it.")
    elif q["main_step"] == 3:
        say(name, "Word of advice: the Dark Lord unleashes a DARK BLAST every third turn.")
        say(name, "Heal up BEFORE it hits. Be level 4 or higher and bring Hi-Potions.")
    else:
        say(name, "Guess I'm out of a job now. Not that I'm complaining!")


# NPC number on the map -> (name, talk function)
NPCS = {
    "1": ("Elder Rowan", talk_elder),
    "2": ("Farmer Bob", talk_farmer),
    "3": ("Lily", talk_lily),
    "4": ("Hermit Mara", talk_hermit),
    "5": ("Guard Tom", talk_guard),
}


def talk_to_npc(player, npc_number):
    """Called by game.py when the player walks into an NPC."""
    name, talk_function = NPCS[npc_number]
    clear_screen()
    print(Fore.YELLOW + Style.BRIGHT + f"=== Talking to {name} ===")
    print()
    talk_function(player)
    print()
    pause()
