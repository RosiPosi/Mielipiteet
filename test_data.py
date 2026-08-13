import db
import sqlite3
import time


db_connection = db.get_connection()

start_time = time.perf_counter()

for i in range(500000):
    db_connection.execute("""
        INSERT INTO items(title, description, user_id)
        VALUES (?, ?, ?)
    """, [f"Test opinion {i}", "Lorem ipsum...", 1])

db_connection.commit()

end_time = time.perf_counter()

db_connection.close()

elapsed_time = end_time - start_time

print("Added 5000 test opinions.")
print(f"Time taken: {elapsed_time:.4f} seconds")
