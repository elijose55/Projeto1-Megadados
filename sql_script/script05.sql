USE REDESOCIAL;
DROP PROCEDURE IF EXISTS adiciona_curtidas;

DELIMITER //
CREATE PROCEDURE adiciona_curtidas(IN email_usuario VARCHAR(30), IN id_post INT, IN tipo_curtida BOOLEAN)
BEGIN
	IF((SELECT COUNT(email) FROM curtidas WHERE email=email_usuario AND post_id = id_post )>0, 1,0) = 1 THEN
		IF(SELECT tipo FROM curtidas WHERE email=email_usuario AND post_id = id_post ) != tipo THEN
			UPDATE curtidas SET tipo = tipo_curtida WHERE email = email_usuario AND post_id = id_post;
		END IF;
    END IF;

    IF((SELECT COUNT(email) FROM curtidas WHERE email=email_usuario AND post_id = id_post )>0, 1,0) = 0 THEN
    	INSERT INTO curtidas (email, post_id, tipo) VALUES (email_usuario, id_post, tipo_curtida);
    END IF;
END//
DELIMITER ;