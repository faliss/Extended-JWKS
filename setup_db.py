import sqlite3

# This will create a SQLite database file if it doesn't exist
conn = sqlite3.connect("totally_not_my_privateKeys.db")
c = conn.cursor()

# Create table 'keys' to store our private keys and their expiration time
c.execute("""
CREATE TABLE IF NOT EXISTS keys(
    kid INTEGER PRIMARY KEY AUTOINCREMENT,
    key BLOB NOT NULL,
    exp INTEGER NOT NULL
)
""")

conn.commit()
conn.close()

print("Database 'totally_not_my_privateKeys.db' created successfully!")
