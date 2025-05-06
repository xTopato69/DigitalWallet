import json
import os
from typing import Dict, Optional
from ..models.user import User, SilverUser, GoldUser, PlatinumUser
from ..utils.security import hash_password, verify_password


class AuthService:
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file #users_file: Path to the users data file
        self.users: Dict[str, User] = self._load_users()


    def _load_users(self) -> Dict[str, User]:
        if os.path.exists(self.users_file) and os.path.getsize(self.users_file) > 0:
            with open(self.users_file, "r") as file:
                data = json.load(file)
                return {u["username"]: User.from_dict(u) for u in data}
        return {}


    def _save_users(self) -> None:
        with open(self.users_file, "w") as file:
            json.dump([u.to_dict() for u in self.users.values()], file, indent=4)


# Register a new user.
    def signup(self, username: str, password: str, user_type: str) -> Optional[User]: #Optional[User]: Created user object if successful, None otherwise
        if username in self.users:
            print("Username already exists. Try logging in.")
            return None

        password_hash = hash_password(password)
        
        user_classes = {
            "silver": SilverUser,
            "gold": GoldUser,
            "platinum": PlatinumUser
        }
        
        user_class = user_classes.get(user_type.lower(), SilverUser)
        user = user_class(username, password_hash)
        
        self.users[username] = user
        self._save_users()
        print(f"Account created successfully for {username}!")
        return user


    def login(self, username: str, password: str) -> Optional[User]:
        if username not in self.users:
            print("Username not found!")
            return None

        user = self.users[username]
        if verify_password(password, user.password_hash):
            print(f"Welcome back, {username}!")
            return user
        else:
            print("Incorrect password!")
            return None


# Get a user by username.
    def get_user(self, username: str) -> Optional[User]:
        return self.users.get(username) 