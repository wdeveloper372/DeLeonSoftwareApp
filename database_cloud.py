import sqlite3
from datetime import datetime

def initialize_db():
    conn = sqlite3.connect("estimates.db")
    cursor = conn.cursor()
    # Create the table if it doesn't exist yet
    cursor.execute('''CREATE TABLE IF NOT EXISTS history 
                      (id INTEGER PRIMARY KEY, 
                       date TEXT, 
                       client_name TEXT, 
                       units REAL, 
                       total REAL)''')
    conn.commit()
    conn.close()

def save_estimate(name, units, total):
    conn = sqlite3.connect("estimates.db")
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    cursor.execute("INSERT INTO history (date, client_name, units, total) VALUES (?, ?, ?, ?)", 
                   (date_str, name, units, total))
    conn.commit()
    conn.close()

def search_estimates(name):
    conn = sqlite3.connect("estimates.db")
    cursor = conn.cursor()
    # Find any name that "contains" the search text
    cursor.execute("SELECT * FROM history WHERE client_name LIKE ? ORDER BY id DESC", (f'%{name}%',))
    results = cursor.fetchall()
    conn.close()
    return results