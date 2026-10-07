import sqlite3

import pandas as pd


connection = sqlite3.connect("library.db")

connection.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
        title TEXT PRIMARY KEY,
        author TEXT,
        genre TEXT,
        year INTEGER,
        price REAL
    )
    """
)

connection.executemany(
    "INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?)",
    [
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937, 12.99),
        ("Matilda", "Roald Dahl", "Children", 1988, 8.50),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925, 10.00),
        ("Harry Potter", "J.K. Rowling", "Fantasy", 1997, 15.00),
    ],
)
connection.commit()

books = pd.read_sql_query("SELECT * FROM books", connection)
print("All books:")
print(books.to_string(index=False))

genre = input("\nFilter by genre: ")
filtered_books = pd.read_sql_query(
    "SELECT * FROM books WHERE genre LIKE ?",
    connection,
    params=(f"%{genre}%",),
)
print("\nMatching genre:")
print(filtered_books.to_string(index=False))

pattern = input("\nSearch title (use % as a wildcard): ")
matching_titles = pd.read_sql_query(
    "SELECT * FROM books WHERE title LIKE ?",
    connection,
    params=(f"%{pattern}%",),
)
print("\nMatching titles:")
print(matching_titles.to_string(index=False))

print("\nLowest price:")
print(books.loc[books["price"].idxmin()].to_string())
print("\nHighest price:")
print(books.loc[books["price"].idxmax()].to_string())

connection.close()
