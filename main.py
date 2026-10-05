import sqlite3
import hashlib
import getpass
import yfinance as yf
import tabulate


DATABASE = "financial_data.db"


# ============================================================
# DATABASE
# ============================================================

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)


def create_tables():
    """Create all required tables."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            dob TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crypto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, date)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forex (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            date TEXT NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(symbol, date)
        )
    """)

    conn.commit()
    conn.close()

    print("Database and tables ready.")


# ============================================================
# PASSWORD SECURITY
# ============================================================

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================================
# USER AUTHENTICATION
# ============================================================

def signup():
    """Create a new user account."""

    print("\n========== SIGN UP ==========")

    username = input("Username: ")
    dob = input("Date of birth (DD-MM-YYYY): ")
    phone = input("Phone number: ")
    email = input("Email ID: ")

    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return False

    hashed_password = hash_password(password)

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users
            (username, dob, phone, email, password)
            VALUES (?, ?, ?, ?, ?)
        """, (username, dob, phone, email, hashed_password))

        conn.commit()
        print("\nAccount created successfully!")
        return True

    except sqlite3.IntegrityError:
        print("\nAn account with this email already exists.")
        return False

    finally:
        conn.close()


def login():
    """Authenticate an existing user."""

    print("\n========== LOGIN ==========")

    email = input("Email ID: ")
    password = getpass.getpass("Password: ")

    hashed_password = hash_password(password)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username
        FROM users
        WHERE email = ? AND password = ?
    """, (email, hashed_password))

    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"\nLogin successful. Welcome, {user[0]}!")
        return True

    print("\nInvalid email or password.")
    return False


# ============================================================
# MARKET DATA
# ============================================================

CRYPTO_SYMBOLS = [
    "BTC-USD",
    "ETH-USD",
    "DOGE-USD",
    "BNB-USD",
    "USDT-USD",
    "XRP-USD",
    "WTRX-USD",
    "USDC-USD",
    "SOL-USD",
    "STETH-USD"
]

FOREX_SYMBOLS = [
    "EURUSD=X",
    "NZDUSD=X",
    "INR=X",
    "GBPINR=X",
    "CNY=X",
    "EURINR=X",
    "RUB=X",
    "JPY=X",
    "EURJPY=X",
    "EURGBP=X"
]


def fetch_market_data(symbol):
    """Fetch the latest market data for a symbol."""

    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1mo")

    if data.empty:
        raise ValueError(f"No data returned for {symbol}")

    latest = data.iloc[-1]

    date = latest.name.date()

    return (
        symbol,
        str(date),
        float(latest["Open"]),
        float(latest["High"]),
        float(latest["Low"]),
        float(latest["Close"])
    )


# ============================================================
# INSERT MARKET DATA
# ============================================================

def insert_market_data(table, market_data):
    """Insert market data into the selected table."""

    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            INSERT OR REPLACE INTO {table}
            (symbol, date, open, high, low, close)
            VALUES (?, ?, ?, ?, ?, ?)
        """, market_data)

        conn.commit()

    except sqlite3.Error as e:
        print(f"Database error: {e}")

    finally:
        conn.close()


def update_market_data():
    """Fetch and store all crypto and forex data."""

    print("\n========== UPDATING MARKET DATA ==========")

    print("\nFetching cryptocurrency data...")

    for symbol in CRYPTO_SYMBOLS:
        try:
            data = fetch_market_data(symbol)
            insert_market_data("crypto", data)
            print(f"Inserted: {symbol}")

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    print("\nFetching forex data...")

    for symbol in FOREX_SYMBOLS:
        try:
            data = fetch_market_data(symbol)
            insert_market_data("forex", data)
            print(f"Inserted: {symbol}")

        except Exception as e:
            print(f"Error fetching {symbol}: {e}")


# ============================================================
# DISPLAY DATA
# ============================================================

def display_data(table):
    """Display all data from a selected table."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT symbol, date, open, high, low, close, timestamp
        FROM {table}
        ORDER BY date DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    if not rows:
        print("\nNo data available.")
        return

    headers = [
        "Symbol",
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Timestamp"
    ]

    print(
        tabulate.tabulate(
            rows,
            headers=headers,
            tablefmt="fancy_grid"
        )
    )


# ============================================================
# ANALYSIS
# ============================================================

def analyse_data(table):
    """Perform basic analysis on market data."""

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT symbol, high
        FROM {table}
        ORDER BY high DESC
        LIMIT 1
    """)

    highest = cursor.fetchone()

    cursor.execute(f"""
        SELECT symbol, low
        FROM {table}
        ORDER BY low ASC
        LIMIT 1
    """)

    lowest = cursor.fetchone()

    conn.close()

    if highest:
        print(
            f"\nHighest recorded price: "
            f"{highest[0]} → {highest[1]}"
        )

    if lowest:
        print(
            f"Lowest recorded price: "
            f"{lowest[0]} → {lowest[1]}"
        )


# ============================================================
# MENU
# ============================================================

def market_menu():
    """Display the main market-data menu."""

    while True:

        print("\n====================================")
        print("       FINANCIAL DATA ANALYSIS")
        print("====================================")

        print("\n1. View Crypto")
        print("2. Analyse Crypto")
        print("3. View Forex")
        print("4. Analyse Forex")
        print("5. Update Market Data")
        print("6. Exit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            display_data("crypto")

        elif choice == 2:
            analyse_data("crypto")

        elif choice == 3:
            display_data("forex")

        elif choice == 4:
            analyse_data("forex")

        elif choice == 5:
            update_market_data()

        elif choice == 6:
            print("\nThank you for using Financial Data Analysis!")
            break

        else:
            print("Invalid choice.")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    create_tables()

    while True:

        print("\n====================================")
        print("      WELCOME TO DATA ANALYSIS")
        print("====================================")

        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            signup()

        elif choice == 2:
            if login():
                market_menu()

        elif choice == 3:
            print("\nGoodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()