CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    comment TEXT
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    reaction TEXT,
    UNIQUE(post_id, user_id)
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE post_classes (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    image BLOB
);

CREATE INDEX idx_posts_user_id
ON posts(user_id);

CREATE INDEX idx_post_classes_post_id
ON post_classes(post_id);

CREATE INDEX idx_post_classes_title_value
ON post_classes(title, value);

CREATE INDEX idx_votes_post_id
ON votes(post_id);

CREATE INDEX idx_comments_post_id
ON comments(post_id);

CREATE INDEX idx_images_post_id
ON images(post_id);
