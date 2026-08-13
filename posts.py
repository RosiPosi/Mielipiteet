import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    rows = list(db.query(sql))

    classes = {}
    for title, value in rows:
        classes.setdefault(title, []).append(value)

    return classes

def add_item(title, description, user_id, classes):
    sql = "INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def add_comment(item_id, user_id, comment):
    sql = "INSERT INTO comments (item_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [item_id, user_id, comment])

def get_comments(item_id):
    sql = """SELECT comments.comment,
               users.id AS user_id,
               users.username,
               votes.reaction
            FROM comments
            JOIN users ON comments.user_id = users.id
            LEFT JOIN votes
            ON votes.item_id = comments.item_id
            AND votes.user_id = comments.user_id
            WHERE comments.item_id = ?
            ORDER BY comments.id"""
    return db.query(sql, [item_id])

def get_reaction_counts(item_id):
    sql = """SELECT reaction, COUNT(*)
            FROM votes
            WHERE item_id = ?
            GROUP BY reaction"""
    rows = db.query(sql, [item_id])

    counts = {"yes": 0, "meh": 0, "no": 0}

    for reaction, count in rows:
        counts[reaction] = count

    return counts

def add_vote(item_id, user_id, reaction):
    sql = "INSERT INTO votes (item_id, user_id, reaction) VALUES (?, ?, ?)"
    db.execute(sql, [item_id, user_id, reaction])

def has_user_voted(item_id, user_id):
    sql = "SELECT reaction FROM votes WHERE item_id = ? AND user_id = ?"
    result = db.query(sql, [item_id, user_id])
    return result[0]["reaction"] if result else None

def get_images(item_id):
    sql = "SELECT id FROM images WHERE item_id = ?"
    return db.query(sql, [item_id])

def add_image(item_id, image):
    sql = "INSERT INTO images (item_id, image) VALUES (?, ?)"
    db.execute(sql, [item_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(item_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND item_id = ?"
    db.execute(sql, [image_id, item_id])

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_items(page=1):
    limit = 15
    offset = (page - 1) * limit
    sql = "SELECT id, title FROM items ORDER BY id DESC LIMIT ? OFFSET ?"
    return db.query(sql, [limit, offset])

def get_item(item_id):
    sql = """SELECT items.id,
                    items.title, 
                    items.description,
                    users.id user_id, 
                    users.username
            FROM items, users
            WHERE items.user_id = users.id 
            AND items.id = ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description, classes):
    sql = """UPDATE items SET
                    title = ?,
                    description = ?
                    WHERE id = ?
            """
    db.execute(sql, [title, description, item_id])

    sql = "DELETE FROM item_classes Where item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [item_id, class_title, class_value])

def remove_item(item_id):
    db.execute("DELETE FROM votes WHERE item_id = ?", [item_id])
    db.execute("DELETE FROM comments WHERE item_id = ?", [item_id])
    db.execute("DELETE FROM item_classes WHERE item_id = ?", [item_id])
    db.execute("DELETE FROM images WHERE item_id = ?", [item_id])
    db.execute("DELETE FROM items WHERE id = ?", [item_id])


def search_results(query, category="", opinion_type="", page=1):
    limit = 15
    offset = (page - 1) * limit

    sql = """SELECT id, title FROM items
            WHERE (title LIKE ? OR description LIKE ?)
            AND (? = '' OR EXISTS (
            SELECT 1 FROM item_classes
            WHERE item_id = items.id
            AND title = 'Category' AND value = ?))
            AND (? = '' OR EXISTS (
            SELECT 1 FROM item_classes
            WHERE item_id = items.id
            AND title = 'Type' AND value = ?))
            ORDER BY id DESC
            LIMIT ? OFFSET ?"""

    like = "%" + query + "%"
    return db.query(sql, [like, like, category, category,
                          opinion_type, opinion_type, limit, offset])
