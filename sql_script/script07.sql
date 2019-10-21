USE REDESOCIAL;
DROP TABLE IF EXISTS posts_favoritos;

CREATE TABLE posts_favoritos (
    email VARCHAR(30) NOT NULL,
    post_id INT NOT NULL,
    PRIMARY KEY (email, post_id),
    FOREIGN KEY(post_id)
        REFERENCES post(post_id),
    FOREIGN KEY (email)
        REFERENCES usuario(email)
);

DROP TRIGGER IF EXISTS remove_curtidas_usuario;
DROP TRIGGER IF EXISTS remove_favoritos_usuario;
DROP TRIGGER IF EXISTS remove_curtidas_post;
DROP TRIGGER IF EXISTS remove_favoritos_post;
DROP TRIGGER IF EXISTS remove_post_usuario;


DELIMITER //
CREATE TRIGGER remove_curtidas_usuario
BEFORE UPDATE ON usuario
FOR EACH ROW
BEGIN
  IF NEW.ativo = 0 THEN DELETE FROM curtidas WHERE email = OLD.email ;
  END IF;
END;

CREATE TRIGGER remove_favoritos_usuario
BEFORE UPDATE ON usuario
FOR EACH ROW
BEGIN
  IF NEW.ativo = 0 THEN DELETE FROM posts_favoritos WHERE email = OLD.email ;
  END IF;
END;

CREATE TRIGGER remove_curtidas_post
BEFORE UPDATE ON post
FOR EACH ROW
BEGIN
  IF NEW.ativo = 0 THEN DELETE FROM curtidas WHERE post_id = OLD.post_id;
  END IF;
END;

CREATE TRIGGER remove_favoritos_post
BEFORE UPDATE ON post
FOR EACH ROW
BEGIN
  IF NEW.ativo = 0 THEN DELETE FROM posts_favoritos WHERE post_id = OLD.post_id;
  END IF;
END;

CREATE TRIGGER remove_post_usuario
BEFORE UPDATE ON usuario
FOR EACH ROW
BEGIN
  IF NEW.ativo = 0 THEN UPDATE post SET ativo = 0 WHERE email = OLD.email;
  END IF;
END //

