import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    rows = list(db.query(sql))

    classes = {}
    for title, value in rows:
        classes.setdefault(title, []).append(value)

    return classes

def add_post(title, description, user_id, classes):
    sql = "INSERT INTO posts (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])

    post_id = db.last_insert_id()

    sql = "INSERT INTO post_classes (post_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [post_id, class_title, class_value])

def add_comment(post_id, user_id, comment):
    sql = "INSERT INTO comments (post_id, user_id, comment) VALUES (?, ?, ?)"
    db.execute(sql, [post_id, user_id, comment])

def get_comments(post_id):
    sql = """SELECT comments.comment,
               users.id AS user_id,
               users.username,
               votes.reaction
            FROM comments
            JOIN users ON comments.user_id = users.id
            LEFT JOIN votes
            ON votes.post_id = comments.post_id
            AND votes.user_id = comments.user_id
            WHERE comments.post_id = ?
            ORDER BY comments.id"""
    return db.query(sql, [post_id])

def get_reaction_counts(post_id):
    sql = """SELECT reaction, COUNT(*)
            FROM votes
            WHERE post_id = ?
            GROUP BY reaction"""
    rows = db.query(sql, [post_id])

    counts = {"yes": 0, "meh": 0, "no": 0}

    for reaction, count in rows:
        counts[reaction] = count

    return counts

def add_vote(post_id, user_id, reaction):
    sql = "INSERT INTO votes (post_id, user_id, reaction) VALUES (?, ?, ?)"
    db.execute(sql, [post_id, user_id, reaction])

def has_user_voted(post_id, user_id):
    sql = "SELECT reaction FROM votes WHERE post_id = ? AND user_id = ?"
    result = db.query(sql, [post_id, user_id])
    return result[0]["reaction"] if result else None

def get_images(post_id):
    sql = "SELECT id FROM images WHERE post_id = ?"
    return db.query(sql, [post_id])

def add_image(post_id, image):
    sql = "INSERT INTO images (post_id, image) VALUES (?, ?)"
    db.execute(sql, [post_id, image])

def get_image(image_id):
    sql = "SELECT image FROM images WHERE id = ?"
    result = db.query(sql, [image_id])
    return result[0][0] if result else None

def remove_image(post_id, image_id):
    sql = "DELETE FROM images WHERE id = ? AND post_id = ?"
    db.execute(sql, [image_id, post_id])

def get_classes(post_id):
    sql = "SELECT title, value FROM post_classes WHERE post_id = ?"
    return db.query(sql, [post_id])

def get_posts(page=1):
    limit = 15
    offset = (page - 1) * limit
    sql = "SELECT id, title FROM posts ORDER BY id DESC LIMIT ? OFFSET ?"
    return db.query(sql, [limit, offset])

def get_post(post_id):
    sql = """SELECT posts.id,
                    posts.title, 
                    posts.description,
                    users.id user_id, 
                    users.username
            FROM posts, users
            WHERE posts.user_id = users.id 
            AND posts.id = ?"""
    result = db.query(sql, [post_id])
    return result[0] if result else None

def update_post(post_id, title, description, classes):
    sql = """UPDATE posts SET
                    title = ?,
                    description = ?
                    WHERE id = ?
            """
    db.execute(sql, [title, description, post_id])

    sql = "DELETE FROM post_classes Where post_id = ?"
    db.execute(sql, [post_id])

    sql = "INSERT INTO post_classes (post_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        db.execute(sql, [post_id, class_title, class_value])

def remove_post(post_id):
    db.execute("DELETE FROM votes WHERE post_id = ?", [post_id])
    db.execute("DELETE FROM comments WHERE post_id = ?", [post_id])
    db.execute("DELETE FROM post_classes WHERE post_id = ?", [post_id])
    db.execute("DELETE FROM images WHERE post_id = ?", [post_id])
    db.execute("DELETE FROM posts WHERE id = ?", [post_id])


def search_results(query, category="", opinion_type="", page=1):
    limit = 15
    offset = (page - 1) * limit

    sql = """SELECT id, title FROM posts
            WHERE (title LIKE ? OR description LIKE ?)
            AND (? = '' OR EXISTS (
            SELECT 1 FROM post_classes
            WHERE post_id = posts.id
            AND title = 'Category' AND value = ?))
            AND (? = '' OR EXISTS (
            SELECT 1 FROM post_classes
            WHERE post_id = posts.id
            AND title = 'Type' AND value = ?))
            ORDER BY id DESC
            LIMIT ? OFFSET ?"""

    like = "%" + query + "%"
    return db.query(sql, [like, like, category, category,
                          opinion_type, opinion_type, limit, offset])
