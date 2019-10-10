'''
criar user
apagar user
criar post
apagar post
marcar user
marcar passaro
visualizar post(guardar dados de view)
procurar post por marcacao de passaro
procurar post por marcacao de user
procurar post por autor
procurar post por titulo
procurar view por tipo de aparelho
procurar view por browser
procurar view por IP
procurar view por instante de visualizacao
procurar user por cidade
procurar user por preferencia de passaro
testes de constrains
'''

import subprocess
import unittest
import pymysql
from functools import partial

def run_db_query(connection, query, args=None):
	with connection.cursor() as cursor:
		#print('Executando query:')
		cursor.execute(query, args)
		results = []
		for result in cursor:
			results.append(result)
		return results

class TestCase(unittest.TestCase):

	connection = pymysql.connect(
		host='localhost',
		user='megadados',
		password='megadados2019',
		database='redesocial')

	db = partial(run_db_query, connection)


	@classmethod
	def setupClass(TestCase):
		with open('script_01.sql' , 'rb') as f:
			res = subprocess.run('mysql -u root -proot < script_01.sql'.split(), stdin=f)
			print(res)   

	def test_meu_teste(self):
		print(" \n-Teste 0")
		print("Isso deve funcionar")
		pass

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

if __name__ == '__main__':
	unittest.main()










