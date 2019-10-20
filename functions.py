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


def acha_usuario_ativo(conn, email):
	with conn.cursor() as cursor:
		cursor.execute('SELECT email FROM usuario WHERE email = %s AND ativo = 1', (email))
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
	pessoas, passaros = coleta_marcacoes(texto)
	with conn.cursor() as cursor:
		try:
			cursor.execute('INSERT INTO post (titulo, texto, url, email) VALUES (%s, %s, %s, %s)', (titulo, texto, url, email))
			cursor.execute('SELECT post_id FROM post WHERE post_id = LAST_INSERT_ID() LIMIT 1')
			res = cursor.fetchone()
			for i in pessoas:
				marca_usuario(conn, res[0], i)
			for i in passaros:
				marca_passaro(conn, res[0], i)
			
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

def acha_post_ativo(conn, titulo, email):
	with conn.cursor() as cursor:
		cursor.execute('SELECT post_id FROM post WHERE titulo = %s AND email = %s AND ativo = 1', (titulo, email))
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
			#cursor.execute('INSERT INTO usuario_tag (post_id, email) VALUES (%s, %s)', (post_id, email))
			cursor.execute('CALL marca_usuario(%s, %s)', (email, post_id))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso adicionar a tag do usuario de email: {email} no post de id: {post_id} na tabela usuario_tag')


''' TABELA usuario_passaro '''
def cria_preferencia(conn, email, nome_passaro):
	with conn.cursor() as cursor:
		try:
			cursor.execute('INSERT INTO usuario_passaro (email, nome_passaro) VALUES (%s, %s)', (email, nome_passaro))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso adicionar a preferencia do usuario de email: {email} ao passaro: {nome_passaro} na tabela usuario_passaro')


''' TABELA curtidas '''
def adiciona_curtida(conn, email, post_id, tipo):
	with conn.cursor() as cursor:
		try:
			cursor.execute('CALL adiciona_curtidas(%s, %s, %s)', (email, post_id, tipo))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso adicionar a curtida do usuario de email: {email} no post de id: {post_id} na tabela curtidas')

def remove_curtida(conn, email, post_id):
	with conn.cursor() as cursor:
		try:
			cursor.execute('DELETE FROM curtidas WHERE email=%s AND post_id=%s', (email, post_id))
		except pymysql.err.IntegrityError as e:
			raise ValueError(f'Não posso remover a curtida do usuario de email: {email} no post de id: {post_id} da tabela curtidas')

def acha_curtidas_post(conn, post_id):
	with conn.cursor() as cursor:
		cursor.execute('SELECT tipo FROM curtidas WHERE post_id = %s', (post_id))
		res = cursor.fetchone()
		if res:
			return res[0]
		else:
			return None


''' SELECOES '''

def procura_post_por_passaro_tag(conn, nome_passaro):
	with conn.cursor() as cursor:
		cursor.execute('SELECT a.post_id\
						FROM post a, passaro_tag b\
						WHERE a.post_id = b.post_id\
						AND b.nome_passaro=%s', (nome_passaro))

		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				posts = tuple(x[0] for x in res)
				return posts[0]

def procura_post_por_usuario_tag(conn, email):
	with conn.cursor() as cursor:
		cursor.execute('SELECT a.post_id\
						FROM post a, usuario_tag b, usuario c\
						WHERE a.post_id = b.post_id AND c.email= %s', (email))

		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				posts = tuple(x[0] for x in res)
				return posts[0]

def procura_usuario_tag_por_post(conn, post_id):
	with conn.cursor() as cursor:
		cursor.execute('SELECT post.email\
						FROM post, usuario_tag\
						WHERE post.post_id = usuario_tag.post_id\
						AND usuario_tag.post_id = %s', (post_id))

		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				posts = tuple(x[0] for x in res)
				return posts[0]


def procura_post_ativo_por_autor(conn, email):
	with conn.cursor() as cursor:
		cursor.execute('SELECT post_id\
						FROM post\
						WHERE post.email = %s\
						AND post.ativo = 1', (email))

		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				posts = tuple(x[0] for x in res)
				return posts[0]



def procura_visualizacao_por_usuario(conn, email):
	with conn.cursor() as cursor:
		cursor.execute('SELECT post_id\
						FROM visualizacao v\
						WHERE v.email=%s', (email))

		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				visualizacao = tuple(x[0] for x in res)
				return visualizacao[0]


def procura_passaro_por_usuario(conn, email): #preferencia --
	with conn.cursor() as cursor:
		cursor.execute('SELECT nome_passaro\
						FROM usuario NATURAL JOIN usuario_passaro\
						WHERE usuario_passaro.email = %s AND usuario.ativo = 1', (email))

		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				passaros = tuple(x[0] for x in res)
				return passaros[0]

def consulta_post_ordem_cronologica_reversa(conn, email):
	with conn.cursor() as cursor:
		cursor.execute('CALL consulta_post_ordem_cronologica_reversa(%s)', (email))
		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				resultado = tuple(x[0] for x in res)
				return resultado

def consulta_usuario_popular(conn):
	with conn.cursor() as cursor:
		cursor.execute('SELECT * FROM consulta_usuario_popular')
		res = cursor.fetchall()
		print("AAAA", res)
		if len(res) == 0 :
				return None
		else:
			return res

def consulta_referencia_usuario(conn, email):
	with conn.cursor() as cursor:
		cursor.execute('CALL referencia_usuario(%s)', (email))
		res = cursor.fetchall()
		if len(res) == 0 :
				return None
		else:
				resultado = tuple(x[0] for x in res)
				return resultado


def coleta_marcacoes(texto): # Retorna as marcacoes de pessoas e passaros de um texto de um post a ser publicado

	palavras = texto.split()
	pessoas = []
	passaros = []

	for i in palavras:
		if(i[0] == "@"):    # Coletar marcacoes de pessoas
			pessoas.append(i[1:])

		if(i[0] == "#"):    # Coletar marcacoes de passaros
			passaros.append(i[1:])
	return pessoas, passaros

