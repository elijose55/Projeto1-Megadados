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

DROP VIEW IF EXISTS consulta_usuario_popular;
CREATE VIEW consulta_usuario_popular AS
    SELECT u.nome_usuario, u.email, u.nome_cidade, COUNT(v.post_id)
    FROM usuario u, post p, visualizacao v
    WHERE u.email = p.email
    AND v.post_id = p.post_id
    GROUP BY v.post_id
   	ORDER BY COUNT(*) DESC;
