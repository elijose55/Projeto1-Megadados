'''
criar user--
apagar user--
criar post--
apagar post--
marcar user--
marcar passaro--
visualizar post(guardar dados de view)--
adicionar preferencia--

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

- ao apagar um post, seu estado muda de ativo para inativo, as marcacoes se mantem e as views tambem (nada)

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

        # Tenta adicionar o mesmo usuario duas vezes.
        try:
            adiciona_usuario(conn, nome_usuario, email, nome_cidade)
            self.fail('Nao deveria ter adicionado o mesmo usuario duas vezes.')
        except ValueError as e:
            pass

        # Checa se o usuario ainda existe.
        id = acha_usuario(conn, email)
        self.assertIsNone(id)

        # Checa se ainda existe algum post ativo daquele usuario
        id = procura_post_ativo_por_autor(conn, email)
        self.assertIsNone(id)

        # Checa se ainda existe alguma preferencia daquele usuario
        id = procura_passaro_por_usuario(conn, email)
        self.assertIsNone(id)

        # Checa se ainda existe alguma marcacao aquele usuario
        id = procura_post_por_usuario_tag(conn, email)
        self.assertIsNone(id)

    def test_adiciona_preferencia(self):
        conn = self.__class__.connection

        nome_usuario = 'eli joseph'
        email = 'elijose55@hotmail.com'
        nome_cidade = "sp"
        nome_passaro = 'pica pau'

        # Adiciona um usuario não existente.
        adiciona_usuario(conn, nome_usuario, email, nome_cidade)

        # Checa se o usuario existe.
        id = acha_usuario(conn, email)
        self.assertIsNotNone(id)

        # Adiciona uma preferencia ao usuario
        cria_preferencia(conn, email, nome_passaro)

        # Checa se a preferencia foi adicionada
        passaro = procura_passaro_por_usuario(conn, email)
        self.assertIsNotNone(id)
        self.assertEqual(passaro, nome_passaro)

    def test_adiciona_post(self):
        conn = self.__class__.connection

        titulo = 'Meu primeiro post sobre passaros!'
        texto = 'Voce sabia que um avestruz.'
        email = 'elijose55@hotmail.com'
        url = 'auera.app'

        # Adiciona um post.
        adiciona_post(conn, titulo, texto, url, email)

        # Checa se o post existe e esta ativo.
        post_id = acha_post_ativo(conn, post_id)
        self.assertIsNotNone(post_id)

        # Tenta achar um post inexistente.
        id = acha_post_ativo(conn, 123)
        self.assertIsNone(id)

    def test_remove_post(self):
        conn = self.__class__.connection

        titulo = 'Meu primeiro post sobre passaros!'
        texto = 'Voce sabia que um avestruz tem o mesmo tamanho de um camelo – 1,80 a 2,50 metros de altura.'
        email = 'elijose55@hotmail.com'
        email_marcado = 'pedroazambuja@hotmail.com'
        email_visualizacao = 'picapau@hotmail.com'
        url = 'auera.app'
        tipo_aparelho = 'android'
        browser = 'chrome'
        ip = '192.168.203.16'

        # Adiciona um post.
        adiciona_post(conn, titulo, texto, url, email)

        # Checa se o post existe e esta ativo.
        post_id = acha_post_ativo(conn, post_id)
        self.assertIsNotNone(post_id)

        # Marca passaro no post
        marca_passaro(conn, post_id, nome_passaro)

        # Marca usuario no post
        marca_usuario(conn, post_id, email_marcado)

        # Visualiza o post
        visualiza_post(conn, email_visualizacao, post_id,
                       tipo_aparelho, browser, ip)

        # Remove o post
        remove_post(conn, post_id)

        # Checa se o post existe e nao esta ativo.
        id = acha_post_ativo(conn, post_id)
        self.assertIsNone(id)

    def test_marca_usuario(self):
        conn = self.__class__.connection

        titulo = 'Meu primeiro post sobre passaros!'
        texto = 'Voce sabia que um avestruz tem o mesmo tamanho de um camelo – 1,80 a 2,50 metros de altura.'
        email = 'elijose55@hotmail.com'
        url = 'auera.app'

        # Adiciona um post.
        adiciona_post(conn, titulo, texto, url, email)

        # Checa se o post existe e esta ativo.
        post_id = acha_post_ativo(conn, post_id)
        self.assertIsNotNone(post_id)

        # Marca um usuario
        marca_usuario(conn, post_id, email)

        # Checa se o usuario foi marcado
        post = procura_post_por_usuario_tag(conn, email)
        self.assertIsNotNone(post)
        self.assertEqual(post, post_id)

    def test_marca_passaro(self):
        conn = self.__class__.connection

        titulo = 'Meu primeiro post sobre passaros!'
        texto = 'Voce sabia que um avestruz tem o mesmo tamanho de um camelo – 1,80 a 2,50 metros de altura.'
        email = 'elijose55@hotmail.com'
        url = 'auera.app'
        nome_passaro = 'avestruz'

        # Adiciona um post.
        adiciona_post(conn, titulo, texto, url, email)

        # Checa se o post existe e esta ativo.
        post_id = acha_post_ativo(conn, post_id)
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
        email_visualizacao = 'picapau@hotmail.com'
        url = 'auera.app'
        tipo_aparelho = 'android'
        browser = 'chrome'
        ip = '192.168.203.16'

        # Adiciona um post.
        adiciona_post(conn, titulo, texto, url, email)

        # Checa se o post existe e esta ativo.
        post_id = acha_post_ativo(conn, post_id)
        self.assertIsNotNone(post_id)

        # Visualiza o post
        visualiza_post(conn, email_visualizacao, post_id,
                       tipo_aparelho, browser, ip)

        # Checa se a visualizacao foi adicionada na tabela VISUALIZACAO
        post = procura_visualizacao_por_usuario(conn, email_visualizacao)
        self.assertIsNotNone(post)
        self.assertEqual(post, post_id)


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


