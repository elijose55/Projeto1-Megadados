USE REDESOCIAL;

ALTER TABLE post
	ADD COLUMN (
		data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP);

DROP PROCEDURE IF EXISTS consulta_post_ordem_cronologica_reversa;
DELIMITER //
CREATE PROCEDURE consulta_post_ordem_cronologica_reversa(IN email varchar(30))
	BEGIN
		SELECT titulo
		FROM post WHERE email = email
		ORDER BY data DESC;
    END//   
DELIMITER ;