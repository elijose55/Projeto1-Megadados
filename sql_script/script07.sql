USE REDESOCIAL;

CREATE TABLE posts_favoritos (
    email VARCHAR(30) NOT NULL,
    post_id INT NOT NULL,
    PRIMARY KEY (email, post_id),
    FOREIGN KEY(post_id)
        REFERENCES post(post_id),
    FOREIGN KEY (email)
        REFERENCES usuario(email)
);