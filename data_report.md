Käytin seuraavaa koodia suuren tietomäärän testaamiseen:
```python
import db
import sqlite3

db_connection = db.get_connection()

for i in range(5000):
    db_connection.execute("""
        INSERT INTO items(title, description, user_id)
        VALUES (?, ?, ?)
    """, [f"Test opinion {i}", "Lorem ipsum...", 1])

db_connection.commit()
db_connection.close()

print("Added 5000 test opinions.")
```
Koodi lisäsi tietokantaan 5000 julkaisua ja ilmestyi sivulle moitteettomasti.
Jos julkaisuja on kuitenkin liikaa, sivusta tulee hyvin pitkä. Tämän takia tietokohteiden sivutus on kätevää.
