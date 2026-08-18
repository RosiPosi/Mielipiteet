import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session
import markupsafe

import config
import posts
import users

print("USING ITEMS FILE:", posts.__file__)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def check_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1
    all_items = posts.get_items(page)
    classes = posts.get_all_classes()
    return render_template("index.html", items=all_items, classes=classes, page=page)

@app.route("/opinion/<int:item_id>")
def show_post(item_id):
    item = posts.get_item(item_id)
    if not item:
        abort(404)
    classes = posts.get_classes(item_id)
    comments = posts.get_comments(item_id)
    images = posts.get_images(item_id)
    reaction_counts = posts.get_reaction_counts(item_id)

    user_vote = None
    if "user_id" in session:
        user_vote = posts.has_user_voted(item_id, session["user_id"])

    return render_template("show_post.html", item=item, classes=classes,
                           comments=comments, images=images,
                           reaction_counts=reaction_counts, user_vote=user_vote)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    page = request.args.get("page", 1, type=int)
    if page < 1:
        page = 1

    user_items = users.get_item(user_id, page)
    item_count = users.get_item_count(user_id)
    classes = posts.get_all_classes()

    return render_template("show_user.html", user=user, items=user_items, 
                           item_count=item_count, classes=classes, page=page)

@app.route("/vote", methods=["POST"])
def vote():
    check_login()
    check_csrf()

    item_id = request.form["item_id"]
    reaction = request.form["reaction"]

    allowed = {"yes", "meh", "no"}

    if reaction not in allowed:
        return "Invalid reaction."

    if posts.has_user_voted(item_id, session["user_id"]):
        return "You have already voted."

    try:
        posts.add_vote(item_id, session["user_id"], reaction)
    except sqlite3.IntegrityError:
        return "You have already voted."

    session["needs_vote_comment"] = item_id

    return redirect("/opinion/" + str(item_id))

@app.route("/new_opinion")
def new_post():
    check_login()
    classes = posts.get_all_classes()
    print("CLASSES:", classes)
    return render_template("new_post.html", classes=classes)

@app.route("/create_opinion", methods=["POST"])
def create_item():
    check_login()
    check_csrf()

    title = request.form["title"].strip()
    description = request.form["description"]
    user_id = session["user_id"]

    if not title or len(title) > 50:
        flash("ERROR: Please input a title in the requested format.")
        return redirect("/new_opinion")
    if len(description) > 1000:
        flash("ERROR: Description can be at most 1000 characters.")
        return redirect("/new_opinion")

    all_classes = posts.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            category, name = entry.split(":")
            if category not in all_classes:
                flash("ERROR: Non-existent category")
                return redirect("/new_opinion")
            if name not in all_classes[category]:
                flash("ERROR: Non-existent category")
                return redirect("/new_opinion")
            classes.append((category, name))

    posts.add_item(title, description, user_id, classes)

    return redirect("/")

@app.route("/comment", methods=["POST"])
def comment():
    check_login()
    check_csrf()

    comment_text = request.form["comment"]
    if not comment_text or len(comment_text) > 450:
        flash("ERROR: Comments can be at most 450 characters.")
        return redirect("/opinion/" + str(item_id))

    item_id = request.form["item_id"]
    item = posts.get_item(item_id)
    if not item:
        abort(403)
    user_id = session["user_id"]

    posts.add_comment(item_id, user_id, comment_text)
    session.pop("needs_vote_comment", None)

    return redirect("/opinion/" + str(item_id))

@app.route("/edit_opinion/<int:item_id>")
def edit_post(item_id):
    check_login()
    item = posts.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    all_classes = posts.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in posts.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_post.html", item=item, classes=classes,
                           all_classes=all_classes)

@app.route("/update_opinion", methods=["POST"])
def update_item():
    check_login()
    check_csrf()

    item_id = request.form["item_id"]

    item = posts.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"].strip()
    description = request.form["description"]

    if not title or len(title) > 50:
        flash("ERROR: Please input a title in the requested format.")
        return redirect("/new_opinion")
    if len(description) > 1000:
        flash("ERROR: Description can be at most 1000 characters.")
        return redirect("/new_opinion")

    all_classes = posts.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            category, name = entry.split(":")
            if category not in all_classes:
                flash("ERROR: Non-existent category")
                return redirect("/new_opinion")
            if name not in all_classes[category]:
                flash("ERROR: Non-existent category")
                return redirect("/new_opinion")
            classes.append((category, name))

    posts.update_item(item_id, title, description, classes)

    return redirect("/opinion/" + str(item_id))

@app.route("/remove_opinion/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    check_login()

    item = posts.get_item(item_id)
    if not item:
        abort(404)
    if item[ "user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            posts.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/opinion/" + str(item_id))

@app.route("/add_image", methods=["POST"])
def add_image():
    check_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = posts.get_item(item_id)
    if not item:
        abort(404)
    if item[ "user_id"] != session["user_id"]:
        abort(403)

    if request.method == "POST":
        file = request.files["image"]
        if not file.filename.lower().endswith((".png")):
            flash("ERROR: PNG files only!")
            return redirect("/images/" + str(item_id))

        image = file.read()
        if len(image) > 1920 * 1080:
            flash("ERROR: Your file is too big!")
            return redirect("/images/" + str(item_id))

        posts.add_image(item_id, image)
        return redirect("/images/" + str(item_id))

@app.route("/images/<int:item_id>")
def edit_images(item_id):
    check_login()
    item = posts.get_item(item_id)
    if not item:
        abort(404)
    if item[ "user_id"] != session["user_id"]:
        abort(403)

    images = posts.get_images(item_id)

    return render_template("images.html", item=item, images=images)

@app.route("/image/<int:image_id>")
def show_image(image_id):
    image = posts.get_image(image_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/remove_images", methods=["POST"])
def remove_images():
    check_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = posts.get_item(item_id)
    if not item:
        abort(404)
    if item[ "user_id"] != session["user_id"]:
        abort(403)

    for image_id in request.form.getlist("image_id"):
        posts.remove_image(item_id, image_id)

    return redirect("/images/" + str(item_id))

@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    category = request.args.get("category", "").strip()
    opinion_type = request.args.get("type", "").strip()
    page = request.args.get("page", 1, type=int)

    if page < 1:
        page = 1

    classes = posts.get_all_classes()
    results = posts.search_results(query, category, opinion_type, page)

    return render_template("search_results.html", query=query, results=results, 
                           category=category, opinion_type=opinion_type, 
                        classes=classes, page=page)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("ERROR: Passwords don't match.")
        return redirect("/register")

    if " " in username:
        abort(403)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("ERROR: Username already taken.")
        return redirect("/register")

    return redirect("/login?registered=1")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("ERROR: wrong username or password.")
            return render_template("login.html")

@app.route("/logout")
def logout():
    check_login()
    session.clear()

    return redirect("/")
