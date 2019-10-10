import pymysql

def adiciona_perigo(conn, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO perigo (nome) VALUES (%s)', (nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela perigo')

def acha_perigo(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM perigo WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def muda_nome_perigo(conn, id, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE perigo SET nome=%s where id=%s', (novo_nome, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela perigo')

def remove_perigo(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM perigo WHERE id=%s', (id))

def lista_perigos(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id from perigo')
        res = cursor.fetchall()
        perigos = tuple(x[0] for x in res)
        return perigos

def adiciona_comida(conn, nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO comida (nome) VALUES (%s)', (nome))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {nome} na tabela comida')

def acha_comida(conn, nome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM comida WHERE nome = %s', (nome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def remove_comida(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM comida WHERE id=%s', (id))

def muda_nome_comida(conn, id, novo_nome):
    with conn.cursor() as cursor:
        try:
            cursor.execute('UPDATE comida SET nome=%s where id=%s', (novo_nome, id))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso alterar nome do id {id} para {novo_nome} na tabela comida')

def lista_comidas(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id from comida')
        res = cursor.fetchall()
        comidas = tuple(x[0] for x in res)
        return comidas

def adiciona_perigo_a_comida(conn, id_perigo, id_comida):
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO comida_perigo VALUES (%s, %s)', (id_comida, id_perigo))

def remove_perigo_de_comida(conn, id_perigo, id_comida):
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM comida_perigo WHERE id_perigo=%s AND id_comida=%s',(id_perigo, id_comida))

def lista_comidas_de_perigo(conn, id_perigo):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_comida FROM comida_perigo WHERE id_perigo=%s', (id_perigo))
        res = cursor.fetchall()
        comidas = tuple(x[0] for x in res)
        return comidas

def lista_perigos_de_comida(conn, id_comida):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_perigo FROM comida_perigo WHERE id_comida=%s', (id_comida))
        res = cursor.fetchall()
        perigos = tuple(x[0] for x in res)
        return perigos
