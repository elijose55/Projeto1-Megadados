USE REDESOCIAL;
DROP PROCEDURE IF EXISTS marca_usuario;

DELIMITER //
CREATE PROCEDURE marca_usuario(IN email_marcado VARCHAR(30), IN post_marcado INT)
BEGIN
	IF EXISTS (SELECT email FROM usuario WHERE email = email_marcado) THEN
		INSERT INTO usuario_tag (email, post_id) VALUES (email_marcado, post_marcado);
    END IF;
END//
DELIMITER ;