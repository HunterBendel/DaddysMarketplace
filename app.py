import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField #can also add ImageField
from wtforms.validators import InputRequired, Email, Length #if you didnt type something in the field it will alert, (there's validators for email addresses)
from flask_sqlalchemy import SQLAlchemy #database
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)  # Create application object
app.config['SECRET_KEY'] = 'This is my super secret key'
db_path = os.path.join(os.path.dirname(__file__), 'user_data.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(15), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class LoginForm(FlaskForm):
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
	remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
	email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
	username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
	password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def index():
    return render_template('index_page.html')

@app.route('/home')
@login_required
def home():
    return render_template('home_page.html', name=current_user.username)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile_page.html', name=current_user.username)

@app.route('/settings')
@login_required
def settings():
    return render_template('settings_page.html', name=current_user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password, form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for('home'))

		return '<h1>Invalid username or password</h1>'

	return render_template('login_page.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = RegisterForm()

	if form.validate_on_submit():
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()

		return '<h1>New user has been created!</h1><p>You may now <a class="btn btn-lg btn-primary btn-block" href="login" role="button">Log in</a></p>'

	return render_template('signup_page.html', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)  # Run our application

# #add database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# #Initialize The Database
# db = SQLAlchemy(app)
# #Create Model
# class User(db.Model):
# 	id = db.Column(db.Integer,primary_key=True) #will assign id automatically
# 	username = db.Column(db.String, unique=True, nullable=False)
# 	name = db.Column(db.String(200), nullable=False) #nullable=False means that their name cant be blank
# 	email = db.Column(db.String(120), nullable=False, unique=True) # unique=true, email can only be used once.
# 	date_added = db.Column(db.DateTime, default = datetime.utcnow)


# 	def __repr__(self):
# 		return '<Name %r>' % self.name


# # with app.app_context():
# # 	db.create_all()

# # 	db.session.add(User(username="example"))
# # 	db.session.commit()

# # 	users = db.session.execute(db.select(User)).scalars()
