USE REDESOCIAL;

DROP TRIGGER IF EXISTS add_user;
DROP TRIGGER IF EXISTS add_passaro_por_marcacao;
DROP TRIGGER IF EXISTS add_passaro_por_preferencia;

DELIMITER //
CREATE TRIGGER add_user
BEFORE INSERT ON usuario
FOR EACH ROW
BEGIN
  IF NOT(NEW.nome_cidade IN (SELECT * FROM cidades)) THEN INSERT INTO cidades (nome_cidade) VALUES (NEW.nome_cidade);
  END IF;
END;

CREATE TRIGGER add_passaro_por_marcacao
BEFORE INSERT ON passaro_tag
FOR EACH ROW
BEGIN
  IF NOT(NEW.nome_passaro IN (SELECT * FROM passaro)) THEN INSERT INTO passaro(nome_passaro)
  VALUES (NEW.nome_passaro);
  END IF;
END;


CREATE TRIGGER add_passaro_por_preferencia
BEFORE INSERT ON usuario_passaro
FOR EACH ROW
BEGIN
  IF NOT(NEW.nome_passaro IN (SELECT * FROM passaro)) THEN INSERT INTO passaro (nome_passaro) VALUES (NEW.nome_passaro);
  END IF;
END //