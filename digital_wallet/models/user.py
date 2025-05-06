from datetime import datetime
from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class User:#    Base User class representing a digital wallet user.
    username: str
    password_hash: str
    user_type: str = "Silver"
    balance: float = field(default=0.0, repr=False)
    transactions: List[str] = field(default_factory=list, repr=False)
    monthly_sent: float = field(default=0.0, repr=False)
    last_payment_month: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m"), repr=False)


    def __post_init__(self):#        Initialize transaction cap based on user type.
        self.transaction_cap = self._set_transaction_cap()


    def _set_transaction_cap(self) -> float:
        caps = {
            "silver": 30000,
            "gold": 150000,
            "platinum": 500000
        }
        return caps.get(self.user_type.lower(), 30000)


    def get_fee(self) -> float:#Get transaction fee based on user tier
        fees = {
            "silver": 10,
            "gold": 5,
            "platinum": 0
        }
        return fees.get(self.user_type.lower(), 10)


    def deposit(self, amount: float) -> bool:
        if amount <= 0:
            print("Deposit amount must be positive!")
            return False
        
        self.balance += amount
        self.transactions.append(f"Deposited: Rs {amount}")
        print(f"Deposited Rs {amount} successfully!")
        return True


    def withdraw(self, amount: float) -> bool:
        if amount > self.balance:
            print("Insufficient funds!")
            return False
        
        self.balance -= amount
        self.transactions.append(f"Withdrew: Rs {amount}")
        print(f"Withdrew Rs {amount} successfully!")
        return True


    def pay(self, receiver: 'User', amount: float) -> bool: #Pay another user.
        fee = self.get_fee()
        total = amount + fee

        current_month = datetime.now().strftime("%Y-%m")
        if self.last_payment_month != current_month:
            self.monthly_sent = 0
            self.last_payment_month = current_month

        if self.monthly_sent + amount > self.transaction_cap:
            print(f"Monthly payment cap exceeded! Your limit is Rs {self.transaction_cap}/month.")
            return False

        if total > self.balance:
            print("Insufficient funds! (including fee)")
            return False

        self.balance -= total
        receiver.balance += amount
        self.monthly_sent += amount

        self.transactions.append(f"Paid {receiver.username}: Rs {amount} (Fee: Rs {fee})")
        receiver.transactions.append(f"Received Rs {amount} from {self.username}")

        print(f"Payment of Rs {amount} to {receiver.username} successful! (Fee: Rs {fee})")
        return True


    def to_dict(self) -> Dict[str, Any]: # Convert user object to dictionary for storage
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "user_type": self.user_type,
            "balance": self.balance,
            "transactions": self.transactions,
            "monthly_sent": self.monthly_sent,
            "last_payment_month": self.last_payment_month,
        }


    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        user = cls(
            username=data["username"],
            password_hash=data["password_hash"],
            user_type=data["user_type"]
        )
        user.balance = data["balance"]
        user.transactions = data["transactions"]
        user.monthly_sent = data.get("monthly_sent", 0)
        user.last_payment_month = data.get("last_payment_month", user.last_payment_month)
        return user


class SilverUser(User):
    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, "Silver")


class GoldUser(User):
    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, "Gold")


class PlatinumUser(User):
    def __init__(self, username: str, password_hash: str):
        super().__init__(username, password_hash, "Platinum") 