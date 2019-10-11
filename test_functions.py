import pymysql





''' TABELA USUARIOS '''
def adiciona_usuario(conn, nome_usuario, email, nome_cidade):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario (nome_usuario, email, nome_cidade) VALUES (%s, %s, %s)', (nome_usuario, email, nome_cidade))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome_usuario} na tabela usuario')

def acha_usuario(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT email FROM usuario WHERE email = %s', (email))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_usuario(conn, email, novo_nome_usuario):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET nome_usuario=%s where email=%s', (novo_nome_usuario, email))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do usuario com email: {email} para {novo_nome_usuario} na tabela usuario')

def remove_usuario(conn, email):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE usuario SET ativo=0 where email=%s', (email))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover o usuario de email: {email} (setar como inativo)')

def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT email, nome_usuario from usuario')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios





''' TABELA POST '''
def adiciona_post(conn, titulo, texto, url, email):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO post (titulo, texto, url, email) VALUES (%s, %s, %s, %s)', (titulo, texto, url, email))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir o post com titulo: {titulo} na tabela post')

def acha_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM post WHERE post_id = %s', (post_id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_post_ativo(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM post WHERE post_id = %s AND ativo = 1', (post_id))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_post(conn, post_id):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE post SET ativo=0 where post_id=%s', (post_id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso remover o post de id: {post_id} (setar como inativo)')



''' TABELA VISUALIZACAO '''
def visualiza_post(conn, email, post_id, tipo_aparelho, browser, ip):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO visualizacao (email, post_id, tipo_aparelho, browser, ip) VALUES (%s, %s, %s, %s, %s)', (email, post_id, tipo_aparelho, browser, ip))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a visualizacao do post de id: {post_id} na tabela visualizacao')



''' TABELA PASSARO_TAG '''
def marca_passaro(conn, post_id, nome_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaro_tag (post_id, nome_passaro) VALUES (%s, %s)', (post_id, nome_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a tag do passaro de nome: {nome_passaro} no post de id: {post_id} na tabela passaro_tag')


''' TABELA USUARIO_TAG '''
def marca_usuario(conn, post_id, email):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario_tag (post_id, email) VALUES (%s, %s)', (post_id, email))
            #cursor.execute('CALL marca_usuario(%s, %s)', (post_id, email))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a tag do usuario de email: {email} no post de id: {post_id} na tabela usuario_tag')


''' TABELA usuario_passaro '''
def cria_preferencia(conn, email, nome_passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO usuario_passaro (email, nome_passaro) VALUES (%s, %s)', (email, nome_passaro))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso adicionar a preferencia do usuario de email: {email} ao passaro: {nome_passaro} na tabela usuario_passaro')


''' SELECOES '''

def procura_post_por_passaro_tag(conn, nome_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM post, passaro_tag\
                        WHERE post.post_id = passaro_tag.post_id\
                        AND passaro_tag.nome_passaro=%s', (nome_passaro))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def procura_passaro_tag_por_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT nome_passaro\
                        FROM post, passaro_tag\
                        WHERE post.post_id = passaro_tag.post_id\
                        AND passaro_tag.post_id=%s', (post_id))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def procura_post_por_usuario_tag(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM post, usuario_tag\
                        WHERE post.post_id = usuario_tag.post_id\
                        AND usuario_tag.email = %s', (email))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def procura_usuario_tag_por_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT email\
                        FROM post, usuario_tag\
                        WHERE post.post_id = usuario_tag.post_id\
                        AND usuario_tag.post_id = %s', (post_id))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def procura_post_por_autor(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM post\
                        WHERE post.email = %s', (email))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts

def procura_post_ativo_por_autor(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM post\
                        WHERE post.email = %s\
                        AND post.ativo = 1', (email))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts


def procura_post_por_titulo(conn, titulo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM post\
                        WHERE post.titulo=%s', (titulo))

        res = cursor.fetchall()
        posts = tuple(x[0] for x in res)
        return posts


def procura_visualizacao_por_tipo_aparelho(conn, tipo_aparelho):
    with conn.cursor() as cursor:
        cursor.execute('SELECT *\
                        FROM visualizacao v\
                        WHERE v.tipo_aparelho=%s', (tipo_aparelho))

        res = cursor.fetchall()
        visualizacao = tuple(x[0] for x in res)
        return visualizacao

def procura_visualizacao_por_usuario(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT *\
                        FROM visualizacao v\
                        WHERE v.email=%s', (email))

        res = cursor.fetchall()
        visualizacao = tuple(x[0] for x in res)
        return visualizacao

def procura_usuario_por_cidade(conn, nome_cidade):
    with conn.cursor() as cursor:
        cursor.execute('SELECT email\
                        FROM usuario \
                        WHERE usuario.nome_cidade=%s', (nome_cidade))

        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def procura_usuario_por_passaro(conn, nome_passaro): #preferencia
    with conn.cursor() as cursor:
        cursor.execute('SELECT email\
                        FROM usuario, usuario_passaro\
                        WHERE usuario.email = usuario_passaro.email\
                        AND usuario_passaro.nome_passaro = %s', (nome_passaro))

        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios

def procura_passaro_por_usuario(conn, email): #preferencia
    with conn.cursor() as cursor:
        cursor.execute('SELECT nome_passaro\
                        FROM usuario, usuario_passaro\
                        WHERE usuario.email = usuario_passaro.email\
                        AND usuario_passaro.email = %s', (email))

        res = cursor.fetchall()
        passaros = tuple(x[0] for x in res)
        return passaros