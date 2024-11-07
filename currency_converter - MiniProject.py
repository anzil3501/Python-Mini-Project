import mysql.connector
from decimal import Decimal

# Database setup
def create_database():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="mohammedanzil123")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS currency_converter")
        mycursor.execute("USE currency_converter")
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies (
                id INT AUTO_INCREMENT PRIMARY KEY,
                code VARCHAR(3) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                exchange_rate DECIMAL(10, 6) NOT NULL
            )
        """)
        
        # Insert default currencies
        default_currencies = [
            ('USD', 'United States Dollar', 1.0),
            ('EUR', 'Euro', 0.92),
            ('JPY', 'Japanese Yen', 152.82),
            ('GBP', 'British Pound', 0.77),
            ('AUD', 'Australian Dollar', 1.52)
        ]

        sql = "INSERT IGNORE INTO currencies (code, name, exchange_rate) VALUES (%s, %s, %s)"
        mycursor.executemany(sql, default_currencies)
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
    finally:
        if mycursor:
            mycursor.close()
        if mydb:
            mydb.close()

class Currency:
    def __init__(self, code, name, exchange_rate):
        self.code = code
        self.name = name
        self.exchange_rate = exchange_rate

    def __str__(self):
        return f"Code: {self.code}, Name: {self.name}, Exchange Rate: {self.exchange_rate}"

class CurrencyConverter:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'mohammedanzil123',
            'database': 'currency_converter'
        }

    def _connect(self):
        return mysql.connector.connect(**self.db_config)

    def add_currency(self, currency):
        mydb = self._connect()
        mycursor = mydb.cursor()
        sql = "INSERT INTO currencies (code, name, exchange_rate) VALUES (%s, %s, %s)"
        mycursor.execute(sql, (currency.code, currency.name, currency.exchange_rate))
        mydb.commit()
        print(f"Currency '{currency.code}' added to the converter.")
        mycursor.close()
        mydb.close()

    def remove_currency(self, code):
        mydb = self._connect()
        mycursor = mydb.cursor()
        sql = "DELETE FROM currencies WHERE code = %s"
        mycursor.execute(sql, (code,))
        mydb.commit()
        if mycursor.rowcount > 0:
            print(f"Currency '{code}' removed from the converter.")
        else:
            print(f"Currency '{code}' not found in the converter.")
        mycursor.close()
        mydb.close()

    def update_currency(self, code, name, exchange_rate):
        mydb = self._connect()
        mycursor = mydb.cursor()
        sql = "UPDATE currencies SET name = %s, exchange_rate = %s WHERE code = %s"
        mycursor.execute(sql, (name, exchange_rate, code))
        mydb.commit()
        if mycursor.rowcount > 0:
            print(f"Currency '{code}' updated successfully.")
        else:
            print(f"Currency '{code}' not found.")
        mycursor.close()
        mydb.close()

    def display_currencies(self):
        mydb = self._connect()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM currencies")
        currencies = mycursor.fetchall()
        mycursor.close()
        mydb.close()

        if currencies:
            print("Available Currencies:")
            for row in currencies:
                print(Currency(row[1], row[2], row[3]))
        else:
            print("No currencies available.")

    def convert_currency(self, from_code, to_code, amount):
        mydb = self._connect()
        mycursor = mydb.cursor()
        sql = "SELECT code, exchange_rate FROM currencies WHERE code IN (%s, %s)"
        mycursor.execute(sql, (from_code, to_code))
        rates = mycursor.fetchall()
        mycursor.close()
        mydb.close()

        if len(rates) == 2:
            from_rate = Decimal(next(rate for code, rate in rates if code == from_code))
            to_rate = Decimal(next(rate for code, rate in rates if code == to_code))
            converted_amount = Decimal(amount) * (to_rate / from_rate)
            print(f"{amount} {from_code} is equal to {converted_amount:.2f} {to_code}.")
        else:
            print("Conversion failed. One of the currency codes is invalid.")

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class CurrencyConverterSystem:
    def __init__(self):
        self.converter = CurrencyConverter()
        self.admin = User("admin", "777")
        self.current_user = None

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == self.admin.username and password == self.admin.password:
            self.current_user = self.admin
            print("Admin logged in successfully.")
        else:
            print("Invalid credentials. Try again.")

    def logout(self):
        self.current_user = None
        print("Logged out successfully.")

    def admin_operations(self):
        while True:
            choice = input("\nAdmin Menu: \n1. Add Currency\n2. Remove Currency\n3. Update Currency\n4. Display Currencies\n5. Logout\nChoose an option: ")
            if choice == '1':
                code = input('Enter the currency code: ')
                name = input('Enter the currency name: ')
                exchange_rate = float(input("Enter the exchange rate: "))
                currency = Currency(code, name, exchange_rate)
                self.converter.add_currency(currency)
            elif choice == '2':
                code = input('Enter the currency code to remove: ')
                self.converter.remove_currency(code)
            elif choice == '3':
                code = input('Enter the currency code to update: ')
                name = input('Enter the new currency name: ')
                exchange_rate = float(input("Enter the new exchange rate: "))
                self.converter.update_currency(code, name, exchange_rate)
            elif choice == '4':
                self.converter.display_currencies()
            elif choice == '5':
                self.logout()
                break
            else:
                print("Invalid option. Please try again.")

    def user_operations(self):
        while True:
            choice = input("\nUser Menu: \n1. Display Currencies\n2. Convert Currency\n3. Logout\nChoose an option: ")
            if choice == '1':
                self.converter.display_currencies()
            elif choice == '2':
                from_code = input('Enter the currency code to convert from: ')
                to_code = input('Enter the currency code to convert to: ')
                amount = float(input('Enter the amount: '))
                self.converter.convert_currency(from_code, to_code, amount)
            elif choice == '3':
                self.logout()
                break
            else:
                print("Invalid option. Please try again.")

    def run(self):
        while True:
            choice = input("1. Login as Admin\n2. Login as User\n3. Exit\nChoose an option: ")
            if choice == '1':
                self.login()
                if self.current_user:
                    self.admin_operations()
            elif choice == '2':
                self.current_user = User("user", "user123")  # Simplified for this example
                print("User logged in successfully.")
                self.user_operations()
            elif choice == '3':
                print("Exiting the currency converter system.")
                break
            else:
                print("Invalid option. Please try again.")

# Create database and run the Currency Converter System
if __name__ == "__main__":
    create_database()
    system = CurrencyConverterSystem()
    system.run()
