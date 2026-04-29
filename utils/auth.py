import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup_user(name, email, password):
    users = load_users()
    if email in users:
        return False, "Email already registered!"
    users[email] = {"name": name, "password": password}
    save_users(users)
    return True, "Account created successfully!"

def login_user(email, password):
    users = load_users()
    if email not in users:
        return False, "User not found!"
    if users[email]["password"] != password:
        return False, "Incorrect password!"
    return True, users[email]["name"]