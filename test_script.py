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

class TestCase(unittest.TestCase):
	def test_meu_teste(self):
		pass

def setUpClass(TestCase):
	with open("script.sql",'rb') as f:
		res = subprocess.run('mysql -u root -proot'.split(), stdin=f)
		print(res)

if __name__ == '__main__':
	unittest.main()