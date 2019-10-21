from fastapi import FastAPI
import pymysql

app = FastAPI()

def connect_db(host='localhost',user='megadados',password='megadados2019',database='redesocial'):
    connection = pymysql.connect(
        host='localhost',
        user='megadados',
        password='megadados2019',
        database='redesocial')
    return connection

''' TABELA USUARIOS '''
@app.post('/usuario')
def adiciona_usuario(nome_usuario: str,email: str,nome_cidade: str):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO usuario (nome_usuario, email, nome_cidade) VALUES (%s, %s, %s)', (nome_usuario, email, nome_cidade))
        cursor.execute('''COMMIT''')
    connection.close()

@app.get('/usuario/{email}')
def acha_usuario_ativo(email):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('SELECT email FROM usuario WHERE email = %s AND ativo = 1', (email))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

@app.put('/usuario/{email}')
def remove_usuario(email):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('UPDATE usuario SET ativo=0 where email=%s', (email))
        cursor.execute('''COMMIT''')

@app.get('/usuario')
def lista_usuarios():
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('SELECT email, nome_usuario from usuario')
        cursor.execute('''COMMIT''')
        res = cursor.fetchall()
        usuarios = tuple(x[0] for x in res)
        return usuarios        



''' TABELA POST '''
@app.put('/posts')
def adiciona_post(titulo,texto,url,email):
    pessoas, passaros = coleta_marcacoes(texto)
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('''START TRANSACTION''')
        cursor.execute('INSERT INTO post (titulo, texto, url, email) VALUES (%s, %s, %s, %s)', (titulo, texto, url, email))
        cursor.execute('SELECT post_id FROM post WHERE post_id = LAST_INSERT_ID() LIMIT 1')

        res = cursor.fetchone()
        for i in pessoas:
            cursor.execute('CALL marca_usuario(%s, %s)', (i, res[0]))
        for i in passaros:
            cursor.execute('INSERT INTO passaro_tag (post_id, nome_passaro) VALUES (%s, %s)', (res[0], i))        
        cursor.execute('''COMMIT''')
    connection.close()


@app.get('/posts')
def acha_post_ativo(conn, titulo, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id FROM post WHERE titulo = %s AND email = %s AND ativo = 1', (titulo, email))
        cursor.execute('''COMMIT''')

        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

@app.put('/posts/{post_id}')
def remove_post(post_id):
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute('UPDATE post SET ativo=0 where post_id=%s', (post_id))
        cursor.execute('''COMMIT''')


''' TABELA VISUALIZACAO '''
@app.get('/view/{post_id}')
def visualiza_post(conn, email, post_id, tipo_aparelho, browser, ip):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO visualizacao (email, post_id, tipo_aparelho, browser, ip) VALUES (%s, %s, %s, %s, %s)', (email, post_id, tipo_aparelho, browser, ip))
        cursor.execute('''COMMIT''')
       
''' TABELA post_salvo '''
@app.post('/favoritos/{post_id}')
def favorita_post(conn, email, post_id):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO posts_favoritos (email, post_id) VALUES (%s, %s)', (email, post_id))
        cursor.execute('''COMMIT''')



''' TABELA PASSARO_TAG '''
@app.post('/marcapassaro/{post_id}')
def marca_passaro(conn, post_id, nome_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO passaro_tag (post_id, nome_passaro) VALUES (%s, %s)', (post_id, nome_passaro))
        cursor.execute('''COMMIT''')

''' TABELA USUARIO_TAG '''
@app.post('/marcausuario/{post_id}')
def marca_usuario(conn, post_id, email):
    with conn.cursor() as cursor:
        cursor.execute('CALL marca_usuario(%s, %s)', (email, post_id))
        cursor.execute('''COMMIT''')

''' TABELA usuario_passaro '''
@app.post('/criapreferencia/{email}')
def cria_preferencia(conn, email, nome_passaro):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO usuario_passaro (email, nome_passaro) VALUES (%s, %s)', (email, nome_passaro))
        cursor.execute('''COMMIT''')



''' TABELA curtidas '''
@app.post('/curtidas/{email}')
def adiciona_curtida(conn, email, post_id, tipo):
    with conn.cursor() as cursor:
        cursor.execute('CALL adiciona_curtidas(%s, %s, %s)', (email, post_id, tipo))
        cursor.execute('''COMMIT''')

@app.delete('/curtidas/{email}')
def remove_curtida(conn, email, post_id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM curtidas WHERE email=%s AND post_id=%s', (email, post_id))
        cursor.execute('''COMMIT''')

@app.get('/curtidas/{post_id}')
def acha_curtidas_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT tipo FROM curtidas WHERE post_id = %s', (post_id))
        cursor.execute('''COMMIT''')
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

''' SELECOES '''
@app.get('/posts/passarotag/{nome_passaro}')
def procura_post_por_passaro_tag(conn, nome_passaro):
    with conn.cursor() as cursor:
        cursor.execute('SELECT a.post_id\
                        FROM post a, passaro_tag b\
                        WHERE a.post_id = b.post_id\
                        AND b.nome_passaro=%s', (nome_passaro))
        cursor.execute('''COMMIT''')


        res = cursor.fetchall()
        if len(res) == 0 :
            return None
        else:
            posts = tuple(x[0] for x in res)
            return posts[0]
@app.get('/posts/usuariotag/{email}')
def procura_post_por_usuario_tag(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT a.post_id\
                        FROM post a, usuario_tag b, usuario c\
                        WHERE a.post_id = b.post_id AND c.email= %s', (email))
        cursor.execute('''COMMIT''')

        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
                posts = tuple(x[0] for x in res)
                return posts[0]
@app.get('/usuario/usuariotag/{post_id}')
def procura_usuario_tag_por_post(conn, post_id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post.email\
                        FROM post, usuario_tag\
                        WHERE post.post_id = usuario_tag.post_id\
                        AND usuario_tag.post_id = %s', (post_id))
        cursor.execute('''COMMIT''')

        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
                posts = tuple(x[0] for x in res)
                return posts[0]

@app.get('/posts/autor/{email}')
def procura_post_ativo_por_autor(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM post\
                        WHERE post.email = %s\
                        AND post.ativo = 1', (email))
        cursor.execute('''COMMIT''')

        res = cursor.fetchall()
        if len(res) == 0 :
            return None
        else:
            posts = tuple(x[0] for x in res)
            return posts[0]


@app.get('/posts/usuarioview/{email}')
def procura_visualizacao_por_usuario(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM visualizacao v\
                        WHERE v.email=%s', (email))
        cursor.execute('''COMMIT''')

        res = cursor.fetchall()
        if len(res) == 0 :
            return None
        else:
            visualizacao = tuple(x[0] for x in res)
            return visualizacao[0]
@app.get('/posts/favorito/{email}')
def procura_posts_favoritos_por_usuario(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('SELECT post_id\
                        FROM posts_favoritos\
                        WHERE posts_favoritos.email=%s', (email))
        cursor.execute('''COMMIT''')

        res = cursor.fetchall()
        if len(res) == 0 :
            return None
        else:
            visualizacao = tuple(x[0] for x in res)
            return visualizacao

@app.get('/passaro/preferencia/{email}')
def procura_passaro_por_usuario(conn, email): #preferencia --
    with conn.cursor() as cursor:
        cursor.execute('SELECT nome_passaro\
                        FROM usuario NATURAL JOIN usuario_passaro\
                        WHERE usuario_passaro.email = %s AND usuario.ativo = 1', (email))
        cursor.execute('''COMMIT''')

        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
                passaros = tuple(x[0] for x in res)
                return passaros[0]
@app.get('/posts/ordenados/{email}')
def consulta_post_ordem_cronologica_reversa(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('CALL consulta_post_ordem_cronologica_reversa(%s)', (email))
        cursor.execute('''COMMIT''')
        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
                resultado = tuple(x[0] for x in res)
                return resultado
@app.get('/usuario/usuario_popular/{nome_cidade}')
def consulta_usuario_popular(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM consulta_usuario_popular')
        cursor.execute('''COMMIT''')
        res = cursor.fetchall()
        print("AAAA", res)
        if len(res) == 0 :
                return None
        else:
            return res

@app.get('/referencia/{email}')
def consulta_referencia_usuario(conn, email):
    with conn.cursor() as cursor:
        cursor.execute('CALL consulta_referencia_usuario(%s)', (email))
        cursor.execute('''COMMIT''')
        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
                resultado = tuple(x[0] for x in res)
                return resultado

@app.get('/quantidade-aparelho')
def consulta_quantidade_aparelho(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM consulta_quantidade_aparelho')
        cursor.execute('''COMMIT''')
        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
            return res

@app.get('/url-passaros/{post_id}')
def consulta_URL_passaros(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM consulta_URL_passaros')
        cursor.execute('''COMMIT''')
        res = cursor.fetchall()
        if len(res) == 0 :
                return None
        else:
            return res


def coleta_marcacoes(texto): # Retorna as marcacoes de pessoas e passaros de um texto de um post a ser publicado

	palavras = texto.split()
	pessoas = []
	passaros = []

	for i in palavras:
		if(i[0] == "@"):    # Coletar marcacoes de pessoas
			i.replace("!", "")
			pessoas.append(i[1:])

		if(i[0] == "#"):    # Coletar marcacoes de passaros
			i.replace("!", "")
			i.replace(".", "")
			i.replace("?", "")
			i.replace(")", "")
			i.replace("-", "")
			i.replace(":", "")
			i.replace(";", "")
			passaros.append(i[1:])
	return pessoas, passaros
