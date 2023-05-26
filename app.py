from flask import Flask, render_template, jsonify, request
import sqlite3
import uuid
from datetime import datetime
import requests

class Carteira:
    def __init__(self, usuario) -> None:
        self.id = uuid.uuid1()
        self.saldo = 0
        self.usuario = usuario

app = Flask(__name__)
#/criar_carteira?usuario=matheus6

### É um POST porém tive que fazer um GET pois o GitHub Codespaces redireciona.
@app.route('/criar_carteira', methods=['GET'])
def criar_carteira():
    usuario = request.args.get('usuario')
    carteira = Carteira(usuario)
    
    #Salvando o banco de dados SQLITE, precisa criar uma noba conexão por questão das Threads
    con = sqlite3.connect("banco.db")
    cur = con.cursor()
    cur.execute("insert into USUARIOS (id, saldo, usuario) values (?, ?, ?)",
        (str(carteira.id), carteira.saldo, carteira.usuario))
    con.commit()
    return jsonify(carteira.id, carteira.saldo, carteira.usuario)

#/consulta_carteira?usuario=matheus2
@app.route('/consulta_carteira', methods=['GET'])
def consulta_carteira():
    usuario = request.args.get('usuario')

    con = sqlite3.connect("banco.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM USUARIOS WHERE usuario=?", (usuario,))
    rows = cur.fetchall()

    for row in rows:
        print(row)

        return jsonify(row)
    
# /transferencia_carteira?origem=matheus6&destino=matheus1&valor=100
### É um POST porém tive que fazer um GET pois o GitHub Codespaces redireciona.
@app.route('/transferencia_carteira', methods=['GET'])
def transferencia_carteira():
    origem = request.args.get('origem')
    destino = request.args.get('destino')
    valor = request.args.get('valor')

    con = sqlite3.connect("banco.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM USUARIOS WHERE usuario=?", (origem,))
    origemBanco = cur.fetchone()

    if float(valor) > origemBanco[1]:
        return jsonify("Saldo na conta não disponível")
    else:
        cur.execute("SELECT * FROM USUARIOS WHERE usuario=?", (destino,))
        destinoBanco = cur.fetchone()

        if destinoBanco:
            try:
                valorNovoOrigem = origemBanco[1] - float(valor)
                valorNovoDestino = destinoBanco[1] + float(valor)

                sql_update_query = """Update USUARIOS set saldo = ? where usuario = ?"""
                data = (valorNovoOrigem, origem)
                cur.execute(sql_update_query, data)

                sql_update_query = """Update USUARIOS set saldo = ? where usuario = ?"""
                data = (valorNovoDestino, destino)
                cur.execute(sql_update_query, data)

                cur.execute("insert into HISTORICO (origem, destino, valor, data) values (?, ?, ?, ?)",
                    (origem, destino, valor, str(datetime.now())))
                con.commit()

                con.commit()

                return jsonify("Transferencia realizada com sucesso!")

            except Exception as exception:
                con.rollback()
                return jsonify(exception)

### É um DELETE porém tive que fazer um GET pois o GitHub Codespaces redireciona.
@app.route('/deletar_carteira', methods=['GET'])
def deletar_carteira():
    try:
        usuario = request.args.get('usuario')

        con = sqlite3.connect("banco.db")
        cur = con.cursor()
        cur.execute("DELETE FROM USUARIOS WHERE usuario=?", (usuario,))

        return jsonify("Usuário deletado com sucesso!")

    except Exception as exception:
        return jsonify("Erro a deletar usuário" + exception)

#/historico?usuario=matheus6
@app.route('/historico', methods=['GET'])
def historico():
    try:
        usuario = request.args.get('usuario')

        con = sqlite3.connect("banco.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM HISTORICO WHERE origem=?", (usuario,))
        rows = cur.fetchall()

        for row in rows:
            print(row)

        return jsonify(rows)

    except Exception as exception:
        return jsonify("Erro a deletar usuário" + exception)


#/historico?usuario=matheus6
@app.route('/get_bitcoin_price', methods=['GET'])
def get_bitcoin_price():

    url = 'https://rest.coinapi.io/v1/exchangerate/BTC/BRL'
    headers = {'X-CoinAPI-Key' : '2262DFFD-E100-4D8E-A6BE-427C976C146A'}
    response = requests.get(url, headers=headers)
    
    return jsonify(response.json())


@app.route('/buy_bitcoin_price', methods=['GET'])
def buy_bitcoin_price():

    url = 'https://rest.coinapi.io/v1/exchangerate/ETC/BRL'
    headers = {'X-CoinAPI-Key' : '2262DFFD-E100-4D8E-A6BE-427C976C146A'}
    response = requests.get(url, headers=headers)
    res = response.json()
    print(res['rate'])


    
    
    return jsonify(response.json())






