USE REDESOCIAL;
DROP PROCEDURE IF EXISTS adiciona_curtidas;

DELIMITER //
CREATE PROCEDURE adiciona_curtidas(IN email_usuario VARCHAR(30), IN id_post INT, IN tipo_curtida BOOLEAN)
BEGIN
	IF EXISTS (SELECT email FROM curtidas WHERE email=email_usuario AND post_id = id_post) THEN
		IF(SELECT tipo FROM curtidas WHERE email=email_usuario AND post_id = id_post ) != tipo_curtida THEN
			UPDATE curtidas SET tipo = tipo_curtida WHERE email = email_usuario AND post_id = id_post;
		END IF;

    ELSE
    	INSERT INTO curtidas (email, post_id, tipo) VALUES (email_usuario, id_post, tipo_curtida);
    END IF;
END//
DELIMITER ;