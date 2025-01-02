from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cameronnasser'
app.config['JWT_SECRET_KEY'] = 'cameronnasser'
jwt = JWTManager(app)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Si le formulaire est soumis
        username = form.username.data
        password = form.password.data
        
        # Authentification simplifiée
        if username == 'admin' and password == 'password':
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        
        return render_template('login.html', form=form, error="Invalid credentials")
    
    return render_template('login.html', form=form)


@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

