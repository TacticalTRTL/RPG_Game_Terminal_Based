"""
auth.py
User registration and login.

Passwords are never saved as plain text. We save a SHA-256 "hash" instead.
A hash is a scrambled version of the password that can't be turned back,
but the same password always makes the same hash, so we can compare them.
"""

import getpass
import hashlib

from colorama import Fore

from database import create_user, get_user, user_exists
from utils import pause

MAX_LOGIN_TRIES = 3


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_username(username):
    """3-15 characters, only letters, numbers or underscores."""
    if not 3 <= len(username) <= 15:
        return False
    return username.replace("_", "").isalnum()


def register():
    """Create a new account. Returns the username, or None if cancelled."""
    print(Fore.CYAN + "--- REGISTER ---  (leave the name blank to cancel)")

    while True:
        username = input(Fore.WHITE + "Choose a username: ").strip().lower()
        if username == "":
            return None
        if not is_valid_username(username):
            print(Fore.RED + "Username must be 3-15 letters, numbers or underscores.")
        elif user_exists(username):
            print(Fore.RED + "That username is taken. Try another.")
        else:
            break

    while True:
        # getpass hides what you type (nothing shows up - that's normal!)
        password = getpass.getpass("Choose a password (min 4 characters, hidden): ")
        if len(password) < 4:
            print(Fore.RED + "Password must be at least 4 characters.")
            continue
        confirm = getpass.getpass("Type it again: ")
        if password != confirm:
            print(Fore.RED + "Passwords don't match. Try again.")
            continue
        break

    create_user(username, hash_password(password))
    print(Fore.GREEN + f"Account '{username}' created!")
    pause()
    return username


def login():
    """Log in. Returns the username, or None after too many failed tries."""
    print(Fore.CYAN + "--- LOGIN ---")

    for attempt in range(1, MAX_LOGIN_TRIES + 1):
        username = input(Fore.WHITE + "Username: ").strip().lower()
        password = getpass.getpass("Password (hidden): ")

        user = get_user(username)
        if user is not None and user["password"] == hash_password(password):
            print(Fore.GREEN + f"Welcome back, {username}!")
            pause()
            return username

        # Same message whether the name or password was wrong (more secure)
        tries_left = MAX_LOGIN_TRIES - attempt
        print(Fore.RED + f"Wrong username or password. {tries_left} tries left.")

    pause()
    return None
