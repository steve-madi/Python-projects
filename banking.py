import sqlite3
import random


class BankAccount:
    def __init__(self, db_name="bank.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        """Create the accounts table if it doesn't exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number TEXT PRIMARY KEY,
            account_holder TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
        """)
        self.conn.commit()

    def generate_account_number(self):
        """Generate a unique 4-digit account number."""
        while True:
            account_number = str(random.randint(1000, 9999))
            self.cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
            if not self.cursor.fetchone():
                return account_number

    def create_account(self, account_holder, pin):
        """Create a new bank account."""
        account_number = self.generate_account_number()
        self.cursor.execute("INSERT INTO accounts (account_number, account_holder, pin, balance) VALUES (?, ?, ?, ?)",
                            (account_number, account_holder, pin, 0.0))
        self.conn.commit()
        print(f"Account created successfully!\nAccount Number: {account_number}\n")

    def login(self, account_number, pin):
        """Validate account number and PIN."""
        self.cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
        return self.cursor.fetchone()

    def get_balance(self, account_number):
        """Get the balance of an account."""
        self.cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_balance(self, account_number, amount):
        """Update the balance of an account."""
        self.cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (amount, account_number))
        self.conn.commit()

    def deposit(self, account_number, amount):
        """Deposit money into an account."""
        balance = self.get_balance(account_number)
        if balance is not None:
            new_balance = balance + amount
            self.update_balance(account_number, new_balance)
            print(f"Mwk{amount} deposited successfully!")
        else:
            print("Account not found!")

    def withdraw(self, account_number, amount):
        """Withdraw money from an account."""
        balance = self.get_balance(account_number)
        if balance is not None:
            if amount > balance:
                print("Insufficient balance!")
            else:
                new_balance = balance - amount
                self.update_balance(account_number, new_balance)
                print(f"Mwk{amount} withdrawn successfully!")
        else:
            print("Account not found!")

    def delete_account(self, account_number):
        """Delete an account."""
        self.cursor.execute("DELETE FROM accounts WHERE account_number = ?", (account_number,))
        self.conn.commit()
        print("Account deleted successfully!")


def main():
    bank = BankAccount()
    print("Welcome to Code 45 Banking App!")

    while True:
        print("\nOptions:")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter your name: ")
            pin = input("Set a 4-digit PIN: ")
            if len(pin) != 4 or not pin.isdigit():
                print("PIN must be exactly 4 digits!")
                continue
            bank.create_account(name, pin)

        elif choice == '2':
            account_number = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            user = bank.login(account_number, pin)

            if user:
                print(f"Welcome back, {user[1]}!")
                while True:
                    print("\nAccount Options:")
                    print("1. Check Balance")
                    print("2. Deposit Money")
                    print("3. Withdraw Money")
                    print("4. Delete Account")
                    print("5. Logout")

                    acc_choice = input("Choose an option: ")

                    if acc_choice == '1':
                        balance = bank.get_balance(account_number)
                        print(f"Current balance: Mwk{balance:.2f}")
                    elif acc_choice == '2':
                        amount = float(input("Enter the amount to deposit: Mwk"))
                        bank.deposit(account_number, amount)
                    elif acc_choice == '3':
                        amount = float(input("Enter the amount to withdraw: Mwk"))
                        bank.withdraw(account_number, amount)
                    elif acc_choice == '4':
                        confirm = input("Are you sure you want to delete your account? (yes/no): ").lower()
                        if confirm == 'yes':
                            bank.delete_account(account_number)
                            break
                    elif acc_choice == '5':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice! Please try again.")
            else:
                print("Invalid account number or PIN!")

        elif choice == '3':
            print("Thank you for using Code 45 Banking App!")
            break
        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
