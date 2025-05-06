from typing import Optional, List
from ..models.user import User

class WalletService:


    def __init__(self, auth_service):
        self.auth_service = auth_service


    def deposit(self, user: User, amount: float) -> bool: #deposit amount in account
        success = user.deposit(amount)
        if success:
            self.auth_service._save_users()
        return success


    def withdraw(self, user: User, amount: float) -> bool: #withdraw amount from user wallet
        success = user.withdraw(amount)
        if success:
            self.auth_service._save_users()
        return success


    def pay(self, sender: User, receiver_username: str, amount: float) -> bool:#Pay money from one user to another.
        receiver = self.auth_service.get_user(receiver_username)
        if not receiver:
            print("Receiver not found!")
            return False

        success = sender.pay(receiver, amount)
        if success:
            self.auth_service._save_users()
        return success


    def get_balance(self, user: User) -> float:
        return user.balance


    def get_transactions(self, user: User) -> List[str]:
        return user.transactions