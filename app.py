import os
import json
import sqlite3 as sql3
from flask import Flask, render_template as render, request, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_bcrypt import Bcrypt
from openpyxl import Workbook

with open("/home/gabriel/prog/json_config/congreso.json") as config_file:
    sec_config = json.load(config_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = sec_config['SECRET_KEY']


@app.route('/', methods=['GET', 'POST'])
def home():

    return render('index.html')


@app.route('/exponen', methods=['GET', 'POST'])
def exponen():
    if request.method == 'POST':
        try:
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            email = request.form['email']
            phone = request.form['phone']
            empresa = request.form['empresa']
            cargo = request.form['cargo']
            tema = request.form['tema']
            titulo = request.form['titulo']
            comentarios = request.form['comentarios']
            
            with sql3.connect("/home/gabriel/prog/sena/congres/instance/IVcongress.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO Ponente (nombres,apellidos,email,phone,empresa,cargo,tema,titulo,comentarios) VALUES (?,?,?,?,?,?,?,?,?)",(nombres,apellidos,email,phone,empresa,cargo,tema,titulo,comentarios) )
                
                conn.commit()
                flash('La inscripción se realizó correctamente')
        except:
            conn.rollback()
            flash('Algo paso y no se ejecuto la operación, por favor intentelo de nuevo')
        
        finally:
            conn.close()
            return redirect(url_for('home'))

    return render("expoform.html")


@app.route('/asisten', methods=['GET', 'POST'])
def asisten():
    if request.method == 'POST':
        try:
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            email = request.form['email']
            phone = request.form['phone']
            empresa = request.form['empresa']
            cargo = request.form['cargo']
            
            with sql3.connect("/home/gabriel/prog/sena/congres/instance/IVcongress.db") as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO Asistente (nombres,apellidos,email,phone,empresa,cargo) VALUES (?,?,?,?,?,?)",(nombres,apellidos,email,phone,empresa,cargo) )
                
                conn.commit()
                flash('La inscripción se realizó correctamente')
        except:
            conn.rollback()
            flash('Algo paso y no se ejecuto la operación, por favor intentelo de nuevo')
        
        finally:
            conn.close()
            return redirect(url_for('home'))
            
    return render("asistform.html")


if __name__ == '__main__':
    #app.run(debug=True, host="172.16.170.128", port=8080)
    app.run(debug=True, host="localhost", port=8080)

