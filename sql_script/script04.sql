USE REDESOCIAL;

CREATE TABLE curtidas (
	email VARCHAR(30) NOT NULL,
	post_id INT NOT NULL,
	tipo BOOLEAN,
    PRIMARY KEY (email,post_id),
    FOREIGN KEY(post_id)
        REFERENCES post(post_id),
    FOREIGN KEY (email)
        REFERENCES usuario(email)
);