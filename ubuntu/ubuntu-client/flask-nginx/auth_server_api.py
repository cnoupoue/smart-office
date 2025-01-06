import bcrypt
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cameronnasser'
app.config["MONGO_URI"] = "mongodb://hepl:heplhepl@localhost:27017/reservationDB?authSource=admin"
mongo = PyMongo(app)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode('utf-8')
    return hashed_password, salt.decode('utf-8')

def check_password(stored_hash, salt, password):
    return stored_hash.encode('utf-8') == bcrypt.hashpw(password.encode(), salt.encode('utf-8'))

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error_message = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = mongo.db['client'].find_one({"email": email})
        if user:
            if check_password(user['password'], user['salt'], password):
                return jsonify(message="Login successful"), 200
            else:
                error_message = "Invalid credentials. Please, try again"
                #return jsonify(message="Invalid credentials"), 401
        else:
            error_message = "User not found"
            #return jsonify(message="User not found"), 404
    return render_template('login.html', form=form, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

