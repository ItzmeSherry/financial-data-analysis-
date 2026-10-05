# Financial Data Analysis — SQLite

A Python-based financial data analysis project that collects cryptocurrency and foreign-exchange market data using Yahoo Finance, stores it locally in SQLite, and performs basic financial analysis.

## Overview

This project was built to explore how financial market data can be collected, stored, processed, and analyzed using Python.

The application currently supports:

- Cryptocurrency market data
- Foreign-exchange market data
- Yahoo Finance data retrieval
- SQLite database storage
- Pandas-based data processing
- Basic financial statistics
- User registration and login
- CLI-based interaction
- Tabular data visualization

## Tech Stack

- **Python**
- **Pandas** — data processing and analysis
- **yfinance** — financial market data
- **SQLite3** — local database
- **Tabulate** — terminal table formatting

## Architecture

```text
Yahoo Finance
      │
      ▼
   yfinance
      │
      ▼
    Pandas
      │
      ├── Data cleaning
      ├── Transformation
      └── Analysis
      │
      ▼
    SQLite
      │
      ├── Users
      ├── Crypto
      └── Forex
      │
      ▼
    CLI
```

## Features

### Market Data

The application retrieves market data including:

- Open price
- High price
- Low price
- Closing price
- Trading date
- Data retrieval timestamp

Supported asset categories include:

**Cryptocurrency**

- Bitcoin
- Ethereum
- Dogecoin
- BNB
- Tether
- XRP
- Solana
- USD Coin
- and other supported Yahoo Finance symbols

**Forex**

- EUR/USD
- NZD/USD
- INR
- GBP/INR
- CNY
- EUR/INR
- EUR/JPY
- EUR/GBP
- and other supported Yahoo Finance symbols

### Database

The project uses SQLite because it requires no external database server and keeps the application portable.

The database contains:

```text
users
crypto
forex
```

The SQLite database file is generated locally and is intentionally excluded from GitHub.

### Analysis

The project can perform basic analysis such as:

- Highest recorded price
- Lowest recorded price
- Average price
- Daily returns
- Volatility
- Moving averages

Additional analysis can be added as the project develops.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd financial-data-analysis-sqlite
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Database

SQLite is included with Python, so no separate database server is required.

The application automatically creates the required database and tables when it starts.

## Project Structure

```text
financial-data-analysis-sqlite/
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── financial_data.db   # generated locally, not committed
```

## Future Improvements

Planned improvements include:

- Interactive financial charts
- More technical indicators
- Historical data storage
- Asset comparison
- Portfolio tracking
- Improved authentication
- Web-based dashboard
- MySQL implementation
- Automated data updates
- More advanced statistical analysis
- Machine-learning-based market analysis

## What I Learned

This project explores the connection between several components of a data application:

```text
API
 ↓
Data Processing
 ↓
Database
 ↓
Analysis
 ↓
User Interface
```

It provided practical experience with Python, SQL databases, external APIs, data processing, and application structure.

## P.S

modify the forex data early so that it can display further data (bug will debug it later)

## Disclaimer

This project is intended for educational and experimental purposes. The financial data and analysis produced by the application should not be considered financial advice.

## License

This project is licensed under the MIT License.
