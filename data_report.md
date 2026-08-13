Käytin seuraavaa koodia suuren tietomäärän testaamiseen:
```python
import db
import sqlite3
import time

db_connection = db.get_connection()

start_time = time.perf_counter()

for i in range(5000):
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
```
Tässä on eri määrien ajat:

Added 5000 test opinions.
Time taken: 0.0212 seconds

Added 50000 test opinions.
Time taken: 0.1995 seconds

Added 500000 test opinions.
Time taken: 1.5802 seconds

Voidaan havaita, että mitä enemmän lisätään kerralla, sitä hitaammaksi prosessi muuttuu.
Koodi lisäsi tietokantaan 5000-500000 julkaisua ja kaikki ilmestyi sivulle moitteettomasti. 
Jos julkaisuja on kuitenkin liikaa, sivusta tulee hyvin pitkä. Tämän takia tietokohteiden sivutus on kätevää. 

