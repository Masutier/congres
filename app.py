import os
import json
import sqlite3 as sql3
from datetime import datetime, timedelta
from flask import Flask, render_template as render, flash, redirect, request, url_for, send_file

with open("/home/gabriel/prog/json_config/csvTools.json") as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.secret_key = config['SECRET_KEY']

app.config['SECRET_KEY'] = 'Bury_me_in_a_nameless_grave'


@app.route('/', methods=['GET', 'POST'])
def home():

    return render('index.html')


@app.route('/exponen', methods=['GET', 'POST'])
def exponen():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        email = request.form['email']
        phone = request.form['phone']
        empresa = request.form['empresa']
        cargo = request.form['cargo']
        tema = request.form['tema']
        titulo = request.form['titulo']
        comentarios = request.form['comentarios']

        if not nombres and not apellidos and not email:
            flash('Falta informacion necesaria!')
        else:
            query = f""" INSERT INTO Ponente (nombres, apellidos, email, phone, empresa, cargo, tema, titulo, comentarios) VALUES ('{nombres}', '{apellidos}', '{email}', '{phone}', '{empresa}', '{cargo}', '{tema}', '{titulo}', '{comentarios}') """
            conn = sql3.connect(config['DB_ADDRESS'])
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            flash('La inscripción se creo correctamente')
            return redirect(url_for('home'))

    return render("expoform.html")


@app.route('/asisten', methods=['GET', 'POST'])
def asisten():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        email = request.form['email']
        phone = request.form['phone']
        empresa = request.form['empresa']
        cargo = request.form['cargo']

        if not nombres and not apellidos and not email:
            flash('Falta informacion necesaria!')
        else:
            query = f""" INSERT INTO Participante (nombres, apellidos, email, phone, empresa, cargo) VALUES ('{nombres}', '{apellidos}', '{email}', '{phone}', '{empresa}', '{cargo}') """
            conn = sql3.connect('/home/gabriel/prog/sena/congress/IIIcongres/dbs/IIIcongress.db')
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            flash('La inscripción se creo correctamente')
            return redirect(url_for('home'))

    return render("asistform.html")


@app.route('/downpdf')
def downpdf():
    requisitos = 'static/docs/ipython.pdf'

    return send_file(requisitos, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
