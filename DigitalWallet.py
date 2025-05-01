import json
import os
import hashlib # for password hashing
from datetime import datetime

# Base User Class haru


class User:
    def __init__(self, username, password_hash, user_type="Silver"):
        self.username = username
        self.password_hash = password_hash # password lai hash garne for security consideration
        self.user_type = user_type
        self.__balance = 0.0
        self.transactions = []
        self.monthly_sent = 0
        self.last_payment_month = self.current_month()
        self.transaction_cap = self.set_transaction_cap()

    def set_transaction_cap(self):# transaction cap haru set gareko for different user types
        tier = self.user_type.lower()
        if tier == "silver":
            return 30000
        elif tier == "gold":
            return 150000
        elif tier == "platinum":
            return 500000
        return 30000  # default

    def current_month(self): # current month ko date format ma return garnako lagi
        return datetime.now().strftime("%Y-%m")

    def deposit(self, amount):# deposit amount lai check garne for positive value
        if amount > 0:
            self.__balance += amount
            self.transactions.append(f"Deposited: Rs {amount}")
            print(f"Deposited Rs {amount} successfully!")
        else:
            print("Deposit amount must be positive!")

    def withdraw(self, amount):# withdraw amount lai check garne for positive value
        if amount > self.__balance:
            print("Insufficient funds!")
        else:
            self.__balance -= amount
            self.transactions.append(f"Withdrew: Rs {amount}")
            print(f"Withdrew Rs {amount} successfully!")

    def get_fee(self): # transaction fee haru set gareko for different user types
        if self.user_type.lower() == "silver":
            return 10
        elif self.user_type.lower() == "gold":
            return 5
        elif self.user_type.lower() == "platinum":
            return 0
        return 10

    def pay(self, receiver, amount): # payment amount lai check garne for positive value
        fee = self.get_fee()
        total = amount + fee

        
        current_month = self.current_month() # current month ko date format ma return garnako lagi
        if self.last_payment_month != current_month:
            self.monthly_sent = 0
            self.last_payment_month = current_month

        if self.monthly_sent + amount > self.transaction_cap:
            print(f"Monthly payment cap exceeded! Your limit is Rs {self.transaction_cap}/month.")
            return False

        if total > self.__balance:
            print("Insufficient funds! (including fee)")
            return False

        self.__balance -= total
        receiver._update_balance(amount)
        self.monthly_sent += amount

        self.transactions.append(f"Paid {receiver.username}: Rs {amount} (Fee: Rs {fee})")
        receiver.transactions.append(f"Received Rs {amount} from {self.username}")

        print(f"Payment of Rs {amount} to {receiver.username} successful! (Fee: Rs {fee})")
        return True

    def show_balance(self):
        print(f"{self.username}'s balance: Rs {self.__balance}")

    def show_transactions(self):
        print(f"Transactions for {self.username}:")
        for transaction in self.transactions:
            print("-", transaction)

    def get_balance(self):
        return self.__balance

    def _update_balance(self, amount):
        self.__balance += amount

    def to_dict(self): # user ko data lai dictionary ma convert garne for saving
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "user_type": self.user_type,
            "balance": self.__balance,
            "transactions": self.transactions,
            "monthly_sent": self.monthly_sent,
            "last_payment_month": self.last_payment_month,
        }

    @classmethod
    def from_dict(cls, data): # user ko data lai dictionary bata object ma convert garne for loading
        user = cls(data["username"], data["password_hash"], data["user_type"])
        user.__balance = data["balance"]
        user.transactions = data["transactions"]
        user.monthly_sent = data.get("monthly_sent", 0)
        user.last_payment_month = data.get("last_payment_month", user.current_month())
        return user

# User Tiers


class SliverUser(User):
    pass  # Withdraw is inherited with default fee logic

class GoldUser(User):
    pass

class PlatinumUser(User):
    pass


# User Management


Users_file = "users.json"

def load_users(): # user haru ko data lai load garne from json file
    if os.path.exists(Users_file) and os.path.getsize(Users_file) > 0:
        with open(Users_file, "r") as file:
            data = json.load(file)
            return {u["username"]: User.from_dict(u) for u in data}
    return {}

def save_users(users): # user haru ko data lai save garne to json file
    with open(Users_file, "w") as file:
        json.dump([u.to_dict() for u in users.values()], file, indent=4)

Users = load_users()

def hash_password(password): # password lai hash garne for security consideration
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up():  # sign up garne for new user
    print("\n--Sign Up--")
    username = input("Enter username: ").strip()
    if username in Users:
        print("Username already exists. Try logging in.")
        return None

    password = input("Enter password: ")
    password_hash = hash_password(password)

    print("Select user type:")
    print("1. Silver")
    print("2. Gold")
    print("3. Platinum")
    choice = input("Enter your choice: ")

    if choice == '1':
        user = SliverUser(username, password_hash, "Silver") 
    elif choice == '2':
        user = GoldUser(username, password_hash, "Gold")
    elif choice == '3':
        user = PlatinumUser(username, password_hash, "Platinum")
    else:
        print("Invalid choice! Defaulting to Silver.")
        user = SliverUser(username, password_hash, "Silver")

    Users[username] = user
    save_users(Users)
    print(f"Account created successfully for {username}!")
    return user

def login(): # login garne for existing user
    print("\n--Login--")
    username = input("Enter username: ").strip()
    if username not in Users:
        print("Username not found!")
        return None

    password = input("Enter password: ")
    password_hash = hash_password(password)
    user = Users[username]
    if user.password_hash == password_hash:
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Incorrect password!")
        return None


# CLI Menu


def user_menu(user): # user ko menu haru display garne for different operations
    while True:
        print(f"\nWelcome {user.username} ({user.user_type})")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Balance")
        print("4. Show Transactions")
        print("5. Pay User")
        print("6. Logout")

        choice = input("Enter choice: ")
        if choice == '1':
            amount = float(input("Enter deposit amount: "))
            user.deposit(amount)
        elif choice == '2':
            amount = float(input("Enter withdraw amount: "))
            user.withdraw(amount)
        elif choice == '3':
            user.show_balance()
        elif choice == '4':
            user.show_transactions()
        elif choice == '5':
            receiver_username = input("Enter receiver's username: ")
            if receiver_username in Users: # check garne for user ko existence
                amount = float(input("Enter amount to pay: "))
                receiver = Users[receiver_username]# receiver ko object lai get garne
                user.pay(receiver, amount)# payment garne
            else:
                print("User not found.")
        elif choice == '6':
            save_users(Users)
            print("Logged out.")
            break
        else:
            print("Invalid choice.")

def main():
    while True:
        print("\n=== Digital Wallet ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            user = sign_up()
            if user:
                user_menu(user)
        elif choice == '2':
            user = login()
            if user:
                user_menu(user)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
