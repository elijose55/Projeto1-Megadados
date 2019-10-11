'''
criar user-
apagar user-
criar post-
apagar post-
marcar user-
marcar passaro-
visualizar post(guardar dados de view)-

procurar post por marcacao de passaro-
procurar post por marcacao de user-
procurar post por autor-
procurar post por titulo-
procurar view por tipo de aparelho-
procurar user por cidade-
procurar user por preferencia de passaro-
testes de constrains


restricoes e sequencias:

- para marcar user, ele deve existir (procedure)

- ao adicionar um usuario (que tera uma cidade), caso essa cidade nao exista na tabela cidades, ela deve ser adicionada (trigger)

- ao marcar um passaro, caso ele n exista na tabela passaros, ele deve ser adiciondo (trigger)

- ao preferir um passaro, caso ele n exista na tabela passaros, ele deve ser adicionado (trigger)

- ao apagar um post, seu estado muda de ativo para inativo, as marcacoes sao apagadas das tabelas tag passaros e usuario e as views tambem (trigger)

- ao apagar um usuario, seus posts mudam de ativo para inativo (aciona o trigger de cima),
apaga a preferencia dele da tabela usuario_passaro, apaga as marcacoes a ele na tabela usuario_tag (trigger)

'''

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

from test_functions import *

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


	def test_meu_teste(self):
		print(" \n-Teste 0")
		print("Isso deve funcionar")
		pass


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
			self.fail('Nao deveria ter adicionado o mesmo perigo duas vezes.')
		except ValueError as e:
			pass

		# Checa se o usuario existe.
		id = acha_usuario(conn, email)
		self.assertIsNotNone(id)

		# Tenta achar um usuario inexistente.
		id = acha_usuario(conn, "naoexiste@hotmail.com")
		self.assertIsNone(id)





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
		filenames = [entry for entry in os.listdir() 
			if os.path.isfile(entry) and re.match(r'.*_\d{3}\.sql', entry)]
		for filename in filenames:
			run_sql_script(filename)

	def tearDownModule():
		run_sql_script('tear_down.sql')

if __name__ == '__main__':
	global config
	with open('config_tests.json', 'r') as f:
		config = json.load(f)
	logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
	unittest.main(verbosity=2)









'''
	def test_inserir_cidade(self):
		print("\n-Teste 1 - inserir cidade")
		connection = pymysql.connect(
			host='localhost',
			user='megadados',
			password='megadados2019',
			database='redesocial')

		db = partial(run_db_query, connection)
		query = "INSERT INTO cidades (nome_cidade) VALUES ('sao paulo');"
		run_db_query(connection, query)

		query = 'SELECT nome_cidade FROM cidades;'
		self.assertEqual(run_db_query(connection, query)[0][0], ('sao paulo'), "Nao retornou a mesma cidade inserida")


	def test_inserir_usuario(self):
		print("\n-Teste 2 - inserir cidade e usuario")
		connection = pymysql.connect(
			host='localhost',
			user='megadados',
			password='megadados2019',
			database='redesocial')
		db = partial(run_db_query, connection)
		query = "INSERT INTO cidades (nome_cidade) VALUES ('Sao paulo')"
		run_db_query(connection, query)
		query = "INSERT INTO usuario (nome_usuario, email, nome_cidade) VALUES ('Peter', 'teste@hotmail.com', 'Sao Paulo')"
		run_db_query(connection, query)
		query = 'SELECT nome_usuario, email, nome_cidade FROM usuario'
		self.assertEqual(run_db_query(connection, query), [('Peter', 'teste@hotmail.com', 'Sao Paulo')], "Nao retornou os mesmos usuarios inseridos")

	def test_inserir_preferencia(self):
		print("\n-Teste 3 - inserir preferencia do usuario")
		connection = pymysql.connect(
			host='localhost',
			user='megadados',
			password='megadados2019',
			database='redesocial')

		db = partial(run_db_query, connection)
		query = "INSERT INTO passaro (nome_passaro) VALUES ('Falcao')"
		run_db_query(connection, query)

		query = "INSERT INTO cidades (nome_cidade) VALUES ('Sao paulo')"
		run_db_query(connection, query)

		query = "INSERT INTO usuario (nome_usuario, email, nome_cidade) VALUES ('Peter', 'teste@hotmail.com', 'Sao Paulo')"
		run_db_query(connection, query)

		query = "INSERT INTO usuario_passaro (email, nome_passaro) VALUES ('teste@hotmail.com', 'Falcao')"
		run_db_query(connection, query)

		query = 'SELECT email, nome_passaro FROM usuario_passaro'
		self.assertEqual(run_db_query(connection, query), [('teste@hotmail.com', 'Falcao')], "Nao retornou a mesmas preferencia/usuario inseridos")

'''
