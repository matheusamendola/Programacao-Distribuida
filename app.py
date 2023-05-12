from flask import Flask, render_template
import sqlite3
import uuid

con = sqlite3.connect("banco.db")
cur = con.cursor()
#cur.execute("CREATE TABLE movie(title, year, score)")


class Carteira:
    def __init__(self, criptomoeda) -> None:
        id = uuid.uuid1()
        saldo = 0
        criptomoeda = criptomoeda

    
        

app = Flask(__name__)

@app.route("/")
def hello_world():
    carteira = Carteira("bitcoin")
    print(carteira)
    return render_template("index.html", title="Hello")

@app.route('/criar_carteira', methods=['POST'])
def criar_carteira():
    pass

@app.route('/consulta_carteira', methods=['GET'])
def consulta_carteira():
    return render_template('expression')

@app.route('/transferencia_carteira', methods=['POST'])
def transferencia_carteira(foo):
    return render_template('expression')

@app.route('/deletar_carteira', methods=['DELETE'])
def deletar_carteira():
    return render_template('expression')