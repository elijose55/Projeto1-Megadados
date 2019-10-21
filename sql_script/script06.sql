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
	SELECT query.email, query.nome_cidade, MAX(query.c) FROM
		(SELECT u.email, u.nome_cidade, COUNT(v.post_id) as c
		FROM usuario u, post p, visualizacao v
		WHERE u.email = p.email
		AND v.post_id = p.post_id
		AND p.ativo = 1
		GROUP BY v.email) as query
	GROUP BY query.nome_cidade;


DROP PROCEDURE IF EXISTS consulta_referencia_usuario;
DELIMITER //
CREATE PROCEDURE consulta_referencia_usuario(IN email varchar(30))
	BEGIN
		SELECT DISTINCT post.email
		FROM post, usuario_tag
		WHERE post.post_id = usuario_tag.post_id
		AND usuario_tag.email = email;
	END//   
DELIMITER ;


DROP VIEW IF EXISTS consulta_quantidade_aparelho;
CREATE VIEW consulta_quantidade_aparelho AS 
	SELECT browser, tipo_aparelho, COUNT(tipo_aparelho)
	FROM visualizacao
	GROUP BY browser, tipo_aparelho;


DROP VIEW IF EXISTS consulta_URL_passaros;
CREATE VIEW consulta_URL_passaros AS 
	SELECT passaro.nome_passaro, post.URL
	FROM passaro, post, passaro_tag
	WHERE passaro.nome_passaro = passaro_tag.nome_passaro
	AND passaro_tag.post_id = post.post_id;