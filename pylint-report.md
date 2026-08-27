# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:26:14: W0613: Unused argument 'error' (unused-argument)
app.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:64:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:80:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:105:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:111:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:150:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:174:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:194:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:235:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:235:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:255:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:255:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:281:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:295:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:305:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:322:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:338:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:343:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:363:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:363:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:382:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module posts
posts.py:1:0: C0114: Missing module docstring (missing-module-docstring)
posts.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:59:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:64:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:81:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:91:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
posts.py:126:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:26:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.54/10 (previous run: 8.52/10, +0.02)
```

Käydään läpi tarkemmin raportin sisältö ja miksi kaikki ei ole korjattu.

## Docstring-ilmoitukset:
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Raportissa mainitaan paljon docstring-kommentteiden puuttuminen. Sovelluksen teossa ei ollut tarvetta dokumentoida koodi docstring-kommenteilla, jolloin niiden yli voi hypätä tietoisesti.

## käyttämätön error:
```
app.py:26:14: W0613: Unused argument 'error' (unused-argument)
```
Pylint antaa varoituksen, koska `error`-parametria ei käytetä funktion sisällä. Flaskin virheenkäsittelymekanismi kuitenkin vaatii error-parametrin, jotta virheenkäsittelijä voi vastaanottaa Flaskin välittämän virheobjektin. Virheen tietoja ei kuitenkin tarvita, koska käyttäjä ohjataan kuitenkin etusivulle.

## Puuttuva palautusarvo:
```
app.py:235:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:255:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Ensimmäiseen ilmoitukseen liittyvä koodi:
```python
@app.route("/remove_opinion/<int:post_id>", methods=["GET", "POST"])
def remove_post(post_id):
    check_login()
    classes = posts.get_all_classes()
    post = posts.get_post(post_id)
    if not post:
        abort(404)
    if post[ "user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_post.html", post=post, classes=classes)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            posts.remove_post(post_id)
            return redirect("/")
        return redirect("/opinion/" + str(post_id))
```

Ilmoitus haluaa varoittaa, että koodi ei palauta arvoa, kun `request.method` ei ole `GET` tai `POST`. Tämä ei ole kuitenkaan mahdollista, sillä funktion dekoraattorissa vaaditaan, että metodin tulee olla `GET` tai `POST`. Tällöin ei ole riskiä, että funktio ei palauta mitään.

## Vaarallinen oletusarvo:
```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Ensimmäiseen ilmoitukseen liittyvä koodi:
```python
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

Tässä parametrin oletusarvo `[]` on tyhjä lista. Varoitus tulee siksi, että jaettu oletuslista voisi aiheuttaa ongelmia, jos sitä muokattaisiin. Tässä funktiossa listaa ei kuitenkaan koskaan muuteta, jolloin haittaa ei synny.
