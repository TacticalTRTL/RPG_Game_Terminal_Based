"""
utils.py
Small helper functions used by many other files:
  - clear_screen()  -> wipes the terminal
  - get_key()       -> reads ONE key press without needing Enter
  - pause()         -> waits for the player to press Enter
  - ask_number()    -> asks for a number and keeps asking until it is valid
  - ask_yes_no()    -> asks a y/n question and keeps asking until it is valid
"""

import os
import sys

from colorama import Fore


def clear_screen():
    """Clear the terminal. Windows uses 'cls', Mac/Linux use 'clear'."""
    os.system("cls" if os.name == "nt" else "clear")


def get_key():
    """
    Read a single key as soon as it is pressed (no Enter needed).
    The professor's example only works on Mac/Linux (termios), so this
    version checks the operating system first and also works on Windows.
    """
    if os.name == "nt":
        # ---- Windows ----
        import msvcrt
        key = msvcrt.getwch()
        # Arrow keys / F-keys send two characters. Read the second one and ignore it.
        if key in ("\x00", "\xe0"):
            msvcrt.getwch()
            return ""
    else:
        # ---- Mac / Linux ----
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # In "raw" mode Ctrl+C shows up as the character \x03 instead of an error,
    # so we raise the error ourselves to let the game quit cleanly.
    if key == "\x03":
        raise KeyboardInterrupt

    return key.lower()


def pause(message="Press ENTER to continue..."):
    """Stop and wait for the player to press Enter."""
    input(Fore.WHITE + message)


def ask_number(prompt, low, high):
    """
    Ask the player for a whole number between low and high (inclusive).
    Input validation: keeps asking until the answer is valid.
    """
    while True:
        answer = input(Fore.WHITE + prompt).strip()

        # .isdigit() is False for letters, blanks, decimals and negative numbers
        if not answer.isdigit():
            print(Fore.RED + "Please type a number.")
            continue

        number = int(answer)
        if low <= number <= high:
            return number

        print(Fore.RED + f"Please type a number from {low} to {high}.")


def ask_yes_no(prompt):
    """Ask a yes/no question. Returns True for yes, False for no."""
    while True:
        answer = input(Fore.WHITE + prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print(Fore.RED + "Please type y or n.")
