# Expense Tracker CLI

A command-line interface application for tracking personal expenses with filtering, sorting, and summary capabilities.

## Features

- Add expenses with date, category, amount, and notes
- List expenses with various filters and sorting options
- Generate expense summaries by category and time period
- Edit existing expenses
- Delete expenses
- Multi-currency support (default: BDT)
- Comprehensive logging
- Data persistence with JSON storage

## Installation

1. Clone or download this repository:
```bash
git clone https://github.com/Mubashirul-Islam/expense-tracker-cli
```
2. Navigate to the project directory:

```bash
cd expense-tracker-cli
```
3. (Optional) Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```
4. No external dependencies required (uses Python standard library only)

## Usage

Run the application as a Python module:

```bash
python -m tracker [command] [options]
```

### Commands

#### Add Expense

Add a new expense entry:

```bash
python -m tracker add --category <category> --amount <amount> [options]
```

**Options:**

- `--category` (required): Expense category (e.g., food, transport, utilities)
- `--amount` (required): Expense amount (must be greater than 0)
- `--date`: Date in YYYY-MM-DD format (default: today)
- `--note`: Optional note or description
- `--currency`: Currency code (default: BDT)

**Examples:**

```bash
# Add a food expense
python -m tracker add --category food --amount 150.50 --note "Lunch at restaurant"

# Add with specific date
python -m tracker add --category transport --amount 50 --date 2026-01-15

# Add with different currency
python -m tracker add --category shopping --amount 99.99 --currency USD --note "Online purchase"
```

#### List Expenses

List expenses with optional filters and sorting:

```bash
python -m tracker list [options]
```

**Options:**

- `--month`: Filter by month (YYYY-MM format)
- `--category`: Filter by category
- `--min`: Minimum amount filter
- `--max`: Maximum amount filter
- `--sort`: Sort by field (choices: date, amount, category; default: date)
- `--desc`: Sort in descending order
- `--limit`: Limit number of results

**Examples:**

```bash
# List all expenses
python -m tracker list

# List expenses for January 2026
python -m tracker list --month 2026-01

# List food expenses sorted by amount (highest first)
python -m tracker list --category food --sort amount --desc

# List expenses between 100 and 500
python -m tracker list --min 100 --max 500

# List top 5 expenses
python -m tracker list --sort amount --desc --limit 5
```

#### Summary

Generate expense summary with category breakdown:

```bash
python -m tracker summary [options]
```

**Options:**

- `--month`: Filter by month (YYYY-MM)
- `--category`: Filter by category
- `--from`: Start date (YYYY-MM-DD)
- `--to`: End date (YYYY-MM-DD)

**Examples:**

```bash
# Summary for current month
python -m tracker summary

# Summary for January 2026
python -m tracker summary --month 2026-01

# Summary for food category
python -m tracker summary --category food

# Summary for date range
python -m tracker summary --from 2026-01-01 --to 2026-01-31
```

The summary displays:

- Total expenses by category with percentages
- Grand total
- Number of expenses
- Average per day
- Highest expense

#### Edit Expense

Edit an existing expense:

```bash
python -m tracker edit --id <expense-id> [options]
```

**Options:**

- `--id` (required): Expense ID to edit
- `--amount`: New amount
- `--note`: New note
- `--category`: New category
- `--date`: New date (YYYY-MM-DD)

**Examples:**

```bash
# Edit amount
python -m tracker edit --id EXP-20260125-0001 --amount 200

# Edit multiple fields
python -m tracker edit --id EXP-20260125-0001 --category utilities --amount 150 --note "Electric bill"
```

#### Delete Expense

Delete an expense by ID:

```bash
python -m tracker delete --id <expense-id>
```

**Example:**

```bash
python -m tracker delete --id EXP-20260125-0001
```


## Project Structure

```
expense-tracker-cli/
├── tracker/
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # Entry point for module execution
│   ├── cli.py            # Command-line interface and argument parsing
│   ├── logger.py         # Logging configuration
│   ├── models.py         # Data models (Expense class)
│   ├── service.py        # Business logic layer
│   ├── storage.py        # Data persistence layer
│   └── utils.py          # Utility functions (validation, ID generation)
├── data/
│   └── expenses.json     # Expense data storage
├── logs/
│   └── expense_tracker.log  # Application logs
└── README.md
```

## Requirements

- Python 3.7 or higher
- No external dependencies (standard library only)

## Development

The application follows a layered architecture:

1. **CLI Layer** ([cli.py](tracker/cli.py)): Handles command-line arguments and user interaction
2. **Service Layer** ([service.py](tracker/service.py)): Contains business logic and validation
3. **Storage Layer** ([storage.py](tracker/storage.py)): Manages data persistence
4. **Model Layer** ([models.py](tracker/models.py)): Defines data structures
5. **Utilities** ([utils.py](tracker/utils.py)): Common helper functions


---

**Note:** This is a command-line application designed for simplicity and ease of use. All data is stored locally in JSON format.
