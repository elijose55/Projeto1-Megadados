DROP DATABASE IF EXISTS REDESOCIAL;
CREATE DATABASE REDESOCIAL;
USE REDESOCIAL;

CREATE TABLE cidades
(
    nome_cidade VARCHAR(30) NOT NULL,
    PRIMARY KEY(nome_cidade)
);
CREATE TABLE usuario
(
    nome_usuario VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL,
    nome_cidade VARCHAR(30) NOT NULL,
    PRIMARY KEY (email),
    FOREIGN KEY(nome_cidade)
        REFERENCES cidades(nome_cidade)
);

CREATE TABLE passaro
(
    nome_passaro VARCHAR(30) NOT NULL,
    PRIMARY KEY (nome_passaro)
);

CREATE TABLE usuario_passaro
(
    email VARCHAR(30) NOT NULL,
    nome_passaro VARCHAR(30) NOT NULL,
    PRIMARY KEY (email, nome_passaro),
    FOREIGN KEY(email)
        REFERENCES usuario(email),
    FOREIGN KEY(nome_passaro)
        REFERENCES passaro(nome_passaro)
);

CREATE TABLE post
(
    post_id INT NOT NULL
    AUTO_INCREMENT,
    titulo VARCHAR
    (30) NOT NULL,
    texto VARCHAR
    (300) NULL,
    URL VARCHAR
    (80) NULL,
    ativo INT NOT NULL DEFAULT 1,
    email VARCHAR
    (30) NOT NULL,
    PRIMARY KEY
    (post_id),
    FOREIGN KEY
    (email) 
        REFERENCES usuario
    (email)
);
    CREATE TABLE usuario_post
    (
        post_id INT NOT NULL,
        email VARCHAR(30) NOT NULL,
        PRIMARY KEY(post_id, email),
        FOREIGN KEY(post_id)
        REFERENCES post(post_id),
        FOREIGN KEY(email)
        REFERENCES usuario(email)
    );
    CREATE TABLE visualizacao
    (
        email VARCHAR(30) NOT NULL,
        post_id INT NOT NULL,
        device VARCHAR(30) NOT NULL,
        browser VARCHAR(30) NOT NULL,
        IP VARCHAR(30) NOT NULL,
        view_time TIMESTAMP NOT NULL,
        PRIMARY KEY (email,post_id),
        FOREIGN KEY(post_id)
        REFERENCES post(post_id),
        FOREIGN KEY (email)
        REFERENCES usuario(email)
    );

    CREATE TABLE post_tag
    (
        post_id INT NOT NULL,
        nome_passaro VARCHAR(30) NOT NULL,
        PRIMARY KEY(post_id,nome_passaro),
        FOREIGN KEY(post_id)
        REFERENCES post(post_id),
        FOREIGN KEY(nome_passaro)
        REFERENCES passaro(nome_passaro)

    );

    CREATE TABLE user_tag
    (
        post_id INT NOT NULL,
        email VARCHAR(30) NOT NULL,
        PRIMARY KEY(post_id,email),
        FOREIGN KEY(email)
        REFERENCES usuario(email),
        FOREIGN KEY(post_id)
        REFERENCES post(post_id)
    );


