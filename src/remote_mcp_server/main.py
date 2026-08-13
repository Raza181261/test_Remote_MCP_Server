from fastmcp import FastMCP
import os
import sqlite3


DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    """Initialize the database and create the expenses table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT ''
        )
    ''')

init_db()

@mcp.tool
def add_expense(date, amount, category, subcategory='', note=''):
    """Add a new expense to the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, amount, category, subcategory, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, amount, category, subcategory, note))
    return {"status": "ok", "id": cursor.lastrowid}


@mcp.tool
def list_expenses(start_date, end_date):
    """List all expenses in the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, date, amount, category, subcategory, note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC', (start_date, end_date))
    cols = [column[0] for column in cursor.description]
    expenses = [dict(zip(cols, row)) for row in cursor.fetchall()]
    return {"status": "ok", "expenses": expenses}

@mcp.tool
def summarize(start_date, end_date, category=None):
    """Summarize expenses by category within a date range. If category is provided, summarize only that category."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE date BETWEEN ? AND ?
    ''')
    params = [start_date, end_date]
    if category:
        query += ' AND category = ?'
        params.append(category)
    query += ' GROUP BY category ORDER BY category ASC'

    cursor.execute(query, params)

    cols = [column[0] for column in cursor.description]
    summary = [dict(zip(cols, row)) for row in cursor.fetchall()]
    return {"status": "ok", "summary": summary}


@mcp.resource("expenses://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can add new categories without restarting the server
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

def main():
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
    )

if __name__ == "__main__":
    main()


# Start the server
# if __name__ == "__main__":
#     mcp.run(transport="http", host="0.0.0.0", port=8000)