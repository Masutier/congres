import os
import json
import sqlite3 as sql3
from flask import Flask, render_template as render, flash, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_bcrypt import Bcrypt
from openpyxl import Workbook


with open("/etc/congreso.json") as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_ADDRESS']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.app_context().push()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    active = db.Column(db.String(5), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username


class Asistente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(150), nullable=False)
    apellidos = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    empresa = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(150), nullable=False)


class Ponente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(150), nullable=False)
    apellidos = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    empresa = db.Column(db.String(150), nullable=False)
    cargo = db.Column(db.String(150), nullable=False)
    tema = db.Column(db.String(150), nullable=False)
    titulo = db.Column(db.String(150), nullable=False)
    comentarios = db.Column(db.String(150), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Nombre de Usuario"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Contraseña"})
    password2 = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Confirmar Contraseña"})
    submit = SubmitField("Registro")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("El nombre de usuario ya existe. Porfavor elija otro.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Nombre de Usuario"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Contraseña"})
    submit = SubmitField("Ingreso")


class AsistenteForm(FlaskForm):
    nombres = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Nombres"})
    apellidos = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Apellidos"})
    email = EmailField(validators=[InputRequired(), Email()], render_kw={"placeholder": "Correo Electronico"})
    phone = StringField(validators=[InputRequired(), Length(min=10, max=20)], render_kw={"placeholder": "Celular"})
    empresa = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Empresa"})
    cargo = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Cargo"})
    submit = SubmitField("Registro")


class PonenteForm(FlaskForm):
    nombres = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Nombres"})
    apellidos = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Apellidos"})
    email = EmailField(validators=[InputRequired(), Email()], render_kw={"placeholder": "Correo Electronico"})
    phone = StringField(validators=[InputRequired(), Length(min=10, max=20)], render_kw={"placeholder": "Celular"})
    empresa = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Empresa"})
    cargo = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Cargo"})
    tema = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Tema"})
    titulo = StringField(validators=[InputRequired(), Length(min=4, max=150)], render_kw={"placeholder": "Titulo"})
    comentarios = TextAreaField(validators=[InputRequired(), Length(min=4, max=2550)], render_kw={"placeholder": "Comentarios"})
    submit = SubmitField("Registro")


@app.route('/', methods=['GET', 'POST'])
def home():

    return render('index.html')


@app.route('/exponen', methods=['GET', 'POST'])
def exponen():
    form = PonenteForm()

    if form.validate_on_submit():
        new_ponente = Ponente(
            nombres = form.nombres.data,
            apellidos = form.apellidos.data,
            email = form.email.data,
            phone = form.phone.data,
            empresa = form.empresa.data,
            cargo = form.cargo.data,
            tema = form.tema.data,
            titulo = form.titulo.data,
            comentarios = form.comentarios.data,
            )
        db.session.add(new_ponente)
        db.session.commit()
        flash('La inscripción se realizó correctamente')
        return redirect(url_for('home'))

    return render("expoform.html", form=form)


@app.route('/asisten', methods=['GET', 'POST'])
def asisten():
    form = AsistenteForm()

    if form.validate_on_submit():
        new_assistant = Asistente(
            nombres = form.nombres.data,
            apellidos = form.apellidos.data,
            email = form.email.data,
            phone = form.phone.data,
            empresa = form.empresa.data,
            cargo = form.cargo.data,
            )
        db.session.add(new_assistant)
        db.session.commit()
        flash('La inscripción se realizó correctamente')
        return redirect(url_for('home'))

    return render("asistform.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        password=form.password.data
        password2=form.password2.data

        if password == password2:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password, active="NO")
            db.session.add(new_user)
            db.session.commit()
            flash('El registro se completo correctamente.')
            return redirect(url_for('loginPage'))
        else:
            flash('Algo salio mal. Intentelo otra vez')
            return redirect(url_for('register'))

    return render("register.html", form=form)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/loginPage', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                if user.active == "YES":
                    login_user(user)
                    return redirect(url_for("profile"))
                else:
                    flash('Aun no estas autorizado')
                    return render('index.html')
            else:
                flash('Algo salio mal. Intentelo otra vez')

    return render("loginPage.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    asist = Asistente.query.count()
    ponent = Ponente.query.count()

    asist = Asistente.query.count()
    return render("profile.html", asist=asist, ponent=ponent)


@app.route('/downpdf')
def downpdf():
    requisitos = 'static/docs/DOCUMENTO_CONGRESO.pdf'

    return send_file(requisitos, as_attachment=True)


@app.route('/downxlsxAssis')
def downxlsxAssis():
    pathFile = 'static/docs/Asistentes.xlsx'
    titles = ["_ID", "NOMBRES", "APELLIDOS", "CORREO", "CELULAR", "EMPRESA", "CARGO"]
    asistentes = Asistente.query.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Asistentes"
    ws.append(titles)

    for asistente in asistentes:
        ws.append([asistente.id, asistente.nombres, asistente.apellidos, asistente.email, asistente.phone, asistente.empresa, asistente.cargo])

    wb.save(pathFile)
    fileDown = pathFile

    return send_file(fileDown, as_attachment=True)


@app.route('/downxlsxPonne')
def downxlsxPonne():
    pathFile = 'static/docs/Ponentes.xlsx'
    titles = ["_ID", "NOMBRES", "APELLIDOS", "CORREO", "CELULAR", "EMPRESA", "CARGO", "TEMA", "TITULO", "COMENTARIO"]

    ponentes = Ponente.query.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Ponentes"
    ws.append(titles)

    for ponente in ponentes:
        ws.append([ponente.id, ponente.nombres, ponente.apellidos, ponente.email, ponente.phone, ponente.empresa, ponente.cargo, ponente.tema, ponente.titulo, ponente.comentarios])

    wb.save(pathFile)
    fileDown = pathFile

    return send_file(fileDown, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host="172.16.170.128", port=8080)

