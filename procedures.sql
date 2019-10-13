USE REDESOCIAL;
DROP PROCEDURE IF EXISTS marca_usuario;

DELIMITER //
CREATE PROCEDURE marca_usuario(IN var_email VARCHAR(30), IN var_id INT)
BEGIN
	IF (SELECT IF((SELECT COUNT(email) FROM usuario WHERE email=var_email)>0, 1,0) = 1) THEN
		INSERT INTO user_tag (email, post_id) VALUES (var_email, var_id);
    END IF;
END//
DELIMITER ;