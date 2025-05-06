from .services.auth_service import AuthService
from .services.wallet_service import WalletService

def display_user_menu(wallet_service: WalletService, user) -> None: # Display and handle the user menu.
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
            try:
                amount = float(input("Enter deposit amount: "))
                wallet_service.deposit(user, amount)
            except ValueError:
                print("Invalid amount!")
                
        elif choice == '2':
            try:
                amount = float(input("Enter withdraw amount: "))
                wallet_service.withdraw(user, amount)
            except ValueError:
                print("Invalid amount!")
                
        elif choice == '3':
            balance = wallet_service.get_balance(user)
            print(f"Current balance: Rs {balance}")
            
        elif choice == '4':
            transactions = wallet_service.get_transactions(user)
            print("\nTransaction History:")
            for transaction in transactions:
                print(f"- {transaction}")
                
        elif choice == '5':
            receiver = input("Enter receiver's username: ")
            try:
                amount = float(input("Enter amount to pay: "))
                wallet_service.pay(user, receiver, amount)
            except ValueError:
                print("Invalid amount!")
                
        elif choice == '6':
            print("Logged out.")
            break
            
        else:
            print("Invalid choice.")


def main():
    auth_service = AuthService()
    wallet_service = WalletService(auth_service)

    while True:
        print("\n=== Digital Wallet ===")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter choice: ")

        if choice == '1':
            username = input("Enter username: ").strip()
            password = input("Enter password: ")
            
            print("\nSelect user type:")
            print("1. Silver")
            print("2. Gold")
            print("3. Platinum")
            
            type_choice = input("Enter your choice: ")
            user_type = {
                '1': 'Silver',
                '2': 'Gold',
                '3': 'Platinum'
            }.get(type_choice, 'Silver')
            
            user = auth_service.signup(username, password, user_type)
            if user:
                display_user_menu(wallet_service, user)
                
        elif choice == '2':
            username = input("Enter username: ").strip()
            password = input("Enter password: ")
            
            user = auth_service.login(username, password)
            if user:
                display_user_menu(wallet_service, user)
                
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main() 