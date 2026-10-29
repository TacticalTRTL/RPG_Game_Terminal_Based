# Shadows Over Elderwood — Terminal RPG (ET 2100 Assignment 10)

## Setup (one time)
Open a terminal in the `Code` folder (the one with `pyproject.toml`) and run:

```
uv add colorama tinydb
```

## Run
```
cd rpg_game_2
uv run main.py
```
Run it in a real terminal (VS Code terminal, PowerShell, Windows Terminal) — the
instant W/A/S/D keys won't work in some "Run" output panes.

Saves go into `game_data.json` in this folder. Delete that file to wipe all
accounts and saves.

## Files
| File | What it does |
|---|---|
| `main.py` | Start here. Main menu → register/login → load or create character |
| `game.py` | Main game loop: keys, movement, what happens when you walk into things |
| `game_map.py` | The 3 maps, portals between them, drawing the map |
| `player.py` | `Player` class: HP, XP, levels, save/load as a dictionary |
| `monster.py` | `Monster` parent class + Slime, Goblin, Wolf, Skeleton, Orc, Boss |
| `skill.py` | `Skill` parent class + Power Strike, Fireball, Heal, Ice Shard |
| `combat.py` | Turn-based battles, cooldowns, rewards |
| `item.py` | Every item's stats and price |
| `inventory.py` | Add / remove / use items, inventory screen |
| `shop.py` | Buy and sell |
| `quest.py` | Main quest + 2 side quests, quest log |
| `npc.py` | The 5 NPCs and their dialogue |
| `database.py` | All TinyDB code (users table + saves table) |
| `auth.py` | Register and login with hashed passwords |
| `story.py` | Title, intro story, victory screen |
| `utils.py` | Clear screen, single key press, input validation helpers |

## Walkthrough
1. Talk to **Elder Rowan** (village) → main quest starts.
2. Go east to the forest, beat 3 monsters.
3. Talk to **Hermit Mara** in the forest → cave seal breaks.
4. Go east through the forest to the **Shadow Cave**, level up to ~4.
5. Beat the **Dark Lord** (🐲) → you win.

Side quests: **Farmer Bob** (kill 3 Slimes → 50 gold), **Lily** (find the
locket in the forest chest → 40 XP + 2 Potions).
