CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    comment TEXT
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    user_id INTEGER REFERENCES users,
    reaction TEXT,
    UNIQUE(item_id, user_id)
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE item_classes (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    item_id INTEGER REFERENCES items,
    image BLOB
);

CREATE INDEX idx_items_user_id
ON items(user_id);

CREATE INDEX idx_item_classes_item_id
ON item_classes(item_id);

CREATE INDEX idx_item_classes_title_value
ON item_classes(title, value);

CREATE INDEX idx_votes_item_id
ON votes(item_id);

CREATE INDEX idx_comments_item_id
ON comments(item_id);

CREATE INDEX idx_images_item_id
ON images(item_id);
