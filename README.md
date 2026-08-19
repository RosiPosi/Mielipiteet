# Mielipiteiden sovellus
Mielipideäänestys sovellus.

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan lisäämiään aiheita.
- Käyttäjä pystyy lisäämään kuvia omiin julkaisuihin.
- Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät mielipiteet.
- Käyttäjä pystyy etsimään aiheita hakusanalla tai kategorian suodatuksilla. 
- Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät mielipiteet.
- Käyttäjä pystyy valitsemaan mielipiteelle yhden kategorian. Mahdolliset kategoriat ovat esim. Urheilu, Pelit, Anime ja Manga, Ruoka, Eläimet, Suhteet jne.
- Käyttäjä pystyy valitsemaan mielipiteelle "tyypin", joka kuvaa onko julkaisu esim. satiirinen, vakava tai henkilökohtainen.
- Sovelluksessa pystyy äänestämään "yes", "meh" tai "no" jokaiseen mielipiteeseen ja näkemään äänestyksen tilastot.
- Sovelluksessa pystyy lukemaan ja kirjoittamaan mielipiteiden perusteluja, jotta ymmärretään miksi näin äänestettiin.
- Perusteluiden/kommenttien mukana lukee mitä käyttäjä äänesti.

# Asennus
Asenna flask-kirjasto:
- Linux: $ pip install flask
- Windows: pip install Flask

Luo tietokannan taulut ja lisää alkutiedot:
- Linux: $ sqlite3 database.db < schema.sql
- Linux: $ sqlite3 database.db < init.sql

- Windows: sqlite3.exe database.db ".read schema.sql"
- Windows: sqlite3.exe database.db ".read init.sql"

Käynnistys:
- Linux: $ flask run 
- Windows: flask run

Vaihda config.py secret key, jotta session toimisi paremmin!

# Sovelluksen toiminta suurella tietomäärällä
Käytin testauksessa koodia, joka näkyy seed.py tiedostossa.
Tässä on tulokset eri määrillä ja niiden ajoilla:

Added 5000 test opinions.
Time taken: 0.0212 seconds

Added 50000 test opinions.
Time taken: 0.1995 seconds

Added 500000 test opinions.
Time taken: 1.5802 seconds

Voidaan havaita, että mitä enemmän lisätään kerralla, sitä hitaammaksi prosessi muuttuu.
Koodi lisäsi tietokantaan 5000-500000 julkaisua ja kaikki ilmestyi sivulle moitteettomasti.
Jos julkaisuja on kuitenkin liikaa, sivusta tulee hyvin pitkä. Tämän takia tietokohteiden sivutus on kätevää.
