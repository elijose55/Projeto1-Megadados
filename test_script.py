
import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql
from functools import partial

from functions import *

def run_db_query(connection, query, args=None):
	with connection.cursor() as cursor:
		#print('Executando query:')
		cursor.execute(query, args)
		results = []
		for result in cursor:
			results.append(result)
		return results


class TestProjeto(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		global config
		cls.connection = pymysql.connect(
			host=config['HOST'],
			user=config['USER'],
			password=config['PASS'],
			database='redesocial'
		)

	@classmethod
	def tearDownClass(cls):
		cls.connection.close()

	def setUp(self):
		conn = self.__class__.connection
		with conn.cursor() as cursor:
			cursor.execute('START TRANSACTION')

	def tearDown(self):
		conn = self.__class__.connection
		with conn.cursor() as cursor:
			cursor.execute('ROLLBACK')

	def test_adiciona_usuario(self):
		conn = self.__class__.connection

		nome_usuario = 'eli joseph'
		email = 'elijose55@hotmail.com'
		nome_cidade = "sp"

		# Adiciona um usuario não existente.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)

		# Tenta adicionar o mesmo usuario duas vezes.
		try:
			adiciona_usuario(conn, nome_usuario, email, nome_cidade)
			self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
		except ValueError as e:
			pass

		# Checa se o usuario existe.
		id = acha_usuario(conn, email)
		self.assertIsNotNone(id)

		# Tenta achar um usuario inexistente.
		id = acha_usuario(conn, "naoexiste@hotmail.com")
		self.assertIsNone(id)

	def test_remove_usuario(self):
		conn = self.__class__.connection

		nome_usuario = 'eli joseph'
		email = 'elijose55@hotmail.com'
		nome_cidade = "sp"

		# Adiciona um usuario não existente.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)
		remove_usuario(conn, email)

		# Checa se o usuario ainda existe.
		_id = acha_usuario_ativo(conn, email)
		self.assertIsNone(_id)

		# Checa se ainda existe algum post ativo daquele usuario
		_id = procura_post_ativo_por_autor(conn, email)
		self.assertIsNone(_id)

		# Checa se ainda existe alguma preferencia daquele usuario
		_id = procura_passaro_por_usuario(conn, email)
		self.assertIsNone(_id)

		# Checa se ainda existe alguma marcacao aquele usuario
		_id = procura_post_por_usuario_tag(conn, email)
		self.assertIsNone(_id)

	def test_adiciona_preferencia(self):
		conn = self.__class__.connection

		nome_usuario = 'eli joseph'
		email = 'elijose55@hotmail.com'
		nome_cidade = "sp"
		nome_passaro = 'pica pau'

		# Adiciona um usuario não existente.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)

		# Checa se o usuario existe.
		_id = acha_usuario(conn, email)
		self.assertIsNotNone(_id)

		# Adiciona uma preferencia ao usuario
		cria_preferencia(conn, email, nome_passaro)

		# Checa se a preferencia foi adicionada
		passaro = procura_passaro_por_usuario(conn, email)
		self.assertIsNotNone(_id)
		self.assertEqual(passaro, nome_passaro)

	def test_adiciona_post(self):

		conn = self.__class__.connection

		titulo = 'Meu primeiro post sobre passaros!'
		texto = 'Voce sabia que um avestruz tem o mesmo tamanho de um camelo.'
		email = 'elijose55@hotmail.com'
		url = 'auera.app'


		nome_usuario = 'eli joseph'
		nome_cidade = "sp"

		# Adiciona o usuario que irá postar.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)
		# Adiciona um post.
		adiciona_post(conn, titulo, texto, url, email)

		# Checa se o post existe e esta ativo.
		post_id = acha_post_ativo(conn, titulo,email)
		self.assertIsNotNone(post_id)

		# Tenta achar um post inexistente.
		id = acha_post_ativo(conn, "nao existe", email)
		self.assertIsNone(id)

	def test_remove_post(self):
		conn = self.__class__.connection
		nome_usuario = 'eli joseph'
		nome_cidade = "sp"
		titulo = 'Meu segundo post sobre passaros!'
		texto = 'Voce sabia que um avestruz tem o mesmo tamanho de dois camelos pequenos – 1,80 a 2,50 metros de altura.'
		email = 'elijose55@hotmail.com'
		url = 'auera.app'
				

		# Adiciona o usuario que irá postar.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)
		# Adiciona um post.
		adiciona_post(conn, titulo, texto, url, email)

		# Checa se o post existe e esta ativo.
		post_id = acha_post_ativo(conn, titulo, email)
		self.assertIsNotNone(post_id)


		# Remove o post
		remove_post(conn, post_id)

		# Checa se o post existe e nao esta ativo.
		id = acha_post_ativo(conn, titulo, email)
		self.assertIsNone(id)

	def test_marca_usuario(self):
		conn = self.__class__.connection
		nome_usuario = 'eli joseph'
		nome_usuario_marcado = 'pedro azambuja'
		nome_cidade = "sp"
		email_marcado = 'pedroazambuja@hotmail.com'
		url = 'auera.app'
		titulo = 'Meu terceiro post sobre passaros!'
		texto = 'Voce sabia que um #avestruz tem o mesmo tamanho de 3 mini camelos – 1,80 a 2,50 metros de altura. @pedroazambuja@hotmail.com'
		email = 'elijose55@hotmail.com'
		url = 'auera.app'



		# Adiciona o usuario que irá postar.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)
		# Adiciona o usuario que irá ser marcado.
		adiciona_usuario(conn, nome_usuario_marcado, email_marcado, nome_cidade)
		# Adiciona um post que contem marcacoes a passaros e usuarios.
		adiciona_post(conn, titulo, texto, url, email)

		# Checa se o post existe e esta ativo.
		post_id = acha_post_ativo(conn, titulo, email)
		self.assertIsNotNone(post_id)

		# Checa se o usuario foi marcado
		post = procura_post_por_usuario_tag(conn, email_marcado)
		self.assertIsNotNone(post)
		self.assertEqual(post, post_id)

		# Checa se consegue marcar um usuario que nao existe em um post
		titulo2 = "teste"
		texto2 = "Ola, @adalberto"
		adiciona_post(conn, titulo2, texto2, url, email)
		post_id = acha_post_ativo(conn, titulo2, email)

		# Checa se o usuario inexistente nao foi marcado
		tag = procura_usuario_tag_por_post(conn, post_id)
		self.assertIsNone(tag)

	def test_marca_passaro(self):
		conn = self.__class__.connection
		email = 'elijose55@hotmail.com'
		nome_passaro = 'avestruz'
		nome_usuario = 'eli joseph'
		nome_cidade = "sp"
		url = 'auera.app'
		titulo = 'Meu quarto post sobre passaros!'
		texto = 'Voce sabia que um avestruz tem o mesmo tamanho de 3 mini camelos – 1,80 a 2,50 metros de altura.'



		# Adiciona o usuario que irá postar.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)

		# Adiciona um post.
		adiciona_post(conn, titulo, texto, url, email)

		# Checa se o post existe e esta ativo.
		post_id = acha_post_ativo(conn, titulo, email)
		self.assertIsNotNone(post_id)

		# Marca um passaro
		marca_passaro(conn, post_id, nome_passaro)

		# Checa se o passaro foi marcado
		post = procura_post_por_passaro_tag(conn, nome_passaro)
		self.assertIsNotNone(post)
		self.assertEqual(post, post_id)

	def test_visualiza_post(self):
		conn = self.__class__.connection

		titulo = 'Meu primeiro post sobre passaros!'
		texto = 'Voce sabia que um avestruz tem o mesmo tamanho de um camelo – 1,80 a 2,50 metros de altura.'
		email = 'elijose55@hotmail.com'
		nome_usuario = 'eli joseph'
		nome_cidade = "sp"
		nome_usuario_visualizacao = "picapau"
		email_visualizacao = 'picapau@hotmail.com'
		url = 'auera.app'
		tipo_aparelho = 'android'
		browser = 'chrome'
		ip = '192.168.203.16'

		# Adiciona o usuario que irá postar.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)
		# Adiciona o usuario que irá visualizar.
		adiciona_usuario(conn, nome_usuario_visualizacao, email_visualizacao, nome_cidade)

		# Adiciona um post.
		adiciona_post(conn, titulo, texto, url, email)

		# Checa se o post existe e esta ativo.
		post_id = acha_post_ativo(conn, titulo, email)
		self.assertIsNotNone(post_id)

		# Visualiza o post
		visualiza_post(conn, email_visualizacao, post_id,
					   tipo_aparelho, browser, ip)

		# Checa se a visualizacao foi adicionada na tabela VISUALIZACAO
		post = procura_visualizacao_por_usuario(conn, email_visualizacao)
		self.assertIsNotNone(post)
		self.assertEqual(post, post_id)


	def test_curtidas(self):
		conn = self.__class__.connection

		nome_usuario = 'eli joseph'
		email = 'elijose55@hotmail.com'
		nome_cidade = "sp"

		# Adiciona um usuario não existente.
		adiciona_usuario(conn, nome_usuario, email, nome_cidade)

		# Checa se o usuario existe.
		id = acha_usuario(conn, email)
		self.assertIsNotNone(id)

		titulo = 'Meu primeiro post sobre passaros!'
		texto = 'Voce sabia que um avestruz tem o mesmo tamanho de um camelo.'
		url = 'auera.app'

		# Adiciona um post.
		adiciona_post(conn, titulo, texto, url, email)

		# Checa se o post existe e esta ativo.
		post_id = acha_post_ativo(conn, titulo, email)
		self.assertIsNotNone(post_id)


		# Adiciona uma curtida positiva ao post
		adiciona_curtida(conn, email, post_id, 1)

		# Checa se a curtida foi adicionada corretamente
		tipo_curtida = acha_curtidas_post(conn, post_id)
		self.assertIsNotNone(tipo_curtida)
		self.assertEqual(tipo_curtida, 1)

		# Tenta adicionar uma segunda curtida do mesmo usuario
		adiciona_curtida(conn, email, post_id, 1)
		tipo_curtida = acha_curtidas_post(conn, post_id)
		self.assertIsNotNone(tipo_curtida)
		self.assertEqual(tipo_curtida, 1)


		# Troca para curtida negativa (anti-joinha)
		adiciona_curtida(conn, email, post_id, 0)

		# Checa se a curtida foi atualizada corretamente
		tipo_curtida = acha_curtidas_post(conn, post_id)
		self.assertIsNotNone(tipo_curtida)
		self.assertEqual(tipo_curtida, 0)

		# Cancela a curtida ao post
		remove_curtida(conn, email, post_id)

		# Checa se a curtida foi removida
		tipo_curtida = acha_curtidas_post(conn, post_id)
		self.assertIsNone(tipo_curtida)






def run_sql_script(filename):
	global config
	with open(filename, 'rb') as f:
		subprocess.run(
			[
				config['MYSQL'], 
				'-u', config['USER'], 
				'-p' + config['PASS'], 
				'-h', config['HOST']
			], 
			stdin=f
		)

def setUpModule():
	filenames = []
	for file in os.listdir("sql_script"):
		if (file.endswith(".sql") and file != "tear_down.sql"):
			filenames.append("sql_script/" + file)

	for filename in filenames:
		run_sql_script(filename)

def tearDownModule():
 	run_sql_script('sql_script/tear_down.sql')


if __name__ == '__main__':
	global config
	with open('config_tests.json', 'r') as f:
		config = json.load(f)
	logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
	unittest.main(verbosity=2)


