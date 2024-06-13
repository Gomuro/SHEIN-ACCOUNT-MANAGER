# Junior Python Developer Project Documentation

## Project Structure

```
junior_python_developer_project/
│
├── parser/
│   ├── __init__.py
│   ├── parser.py             # Main script for parsing vacancies
│   └── requirements.txt      # Dependencies for the parser
│
├── bot/
│   ├── __init__.py
│   ├── bot.py                # Telegram bot implementation
│   └── requirements.txt      # Dependencies for the bot
│
├── database/
│   ├── __init__.py
│   ├── db.py                 # Database setup and interaction
│   └── vacancies.db          # SQLite database file
│
├── main.py                   # Main entry point to run both parser and bot concurrently
└── requirements.txt          # Main dependencies for the entire project
```

## Installation Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/junior_python_developer_project.git
cd junior_python_developer_project
```

### 2. Set Up a Virtual Environment

It's recommended to use a virtual environment to manage your dependencies. You can create and activate a virtual environment using the following commands:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Project

### 1. Database Setup

Before running the project, ensure the SQLite database is set up. The database schema will be automatically created when the parser script is run for the first time.

### 2. Running the Parser and Bot Concurrently

The main entry point of the project is `main.py`, which runs both the parser and the Telegram bot concurrently using `asyncio`.

To start the project, run:

```bash
python main.py
```

This script will:
- Start the parser that fetches the number of "junior" vacancies from robota.ua every hour and stores the data in the SQLite database.
- Start the Telegram bot that listens for commands and responds with statistics.

## Project Components

### Parser

- **File**: `parser/parser.py`
- **Description**: This script fetches the number of "junior" vacancies from robota.ua and saves the count along with the current timestamp into the SQLite database.

### Telegram Bot

- **File**: `bot/bot.py`
- **Description**: This script implements a Telegram bot using `aiogram`. The bot listens for the command `/get_today_statistic` and responds with an Excel report containing the number of vacancies for the current day.

### Database

- **File**: `database/db.py`
- **Description**: This script sets up the SQLite database and provides functions for interacting with it.

## Example Commands

### Fetch Today's Statistics

To fetch the statistics, send the following command to the Telegram bot:

```
/get_today_statistic
```

The bot will respond with an Excel file containing the vacancy data for the current day.

## Additional Notes

- Ensure you have the necessary permissions to access and modify the SQLite database file (`vacancies.db`).
- The parser fetches data every hour. Ensure your system's clock is correctly synchronized to avoid any discrepancies in timestamps.
- If you encounter any issues, check the logs for error messages and debug information.

## Dependencies

Here is the complete list of dependencies specified in the `requirements.txt`:

```
aiofiles==23.2.1
aiogram==3.7.0
aiohttp==3.9.5
aiosignal==1.3.1
annotated-types==0.7.0
attrs==23.2.0
certifi==2024.6.2
cffi==1.16.0
charset-normalizer==3.3.2
et-xmlfile==1.1.0
frozenlist==1.4.1
greenlet==3.0.3
h11==0.14.0
idna==3.7
magic-filter==1.0.12
multidict==6.0.5
numpy==1.26.4
openpyxl==3.1.4
outcome==1.3.0.post0
packaging==24.1
pandas==2.2.2
pycparser==2.22
pydantic==2.7.4
pydantic_core==2.18.4
PySocks==1.7.1
python-dateutil==2.9.0.post0
python-dotenv==1.0.1
pytz==2024.1
requests==2.32.3
schedule==1.2.2
selenium==4.21.0
six==1.16.0
sniffio==1.3.1
sortedcontainers==2.4.0
SQLAlchemy==2.0.30
trio==0.25.1
trio-websocket==0.11.1
typing_extensions==4.12.2
tzdata==2024.1
urllib3==2.2.1
webdriver-manager==4.0.1
wsproto==1.2.0
XlsxWriter==3.2.0
yarl==1.9.4
```

With this documentation, you should be able to install the necessary dependencies, understand the project structure, and run the project successfully.