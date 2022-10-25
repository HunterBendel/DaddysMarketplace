from flask import Flask, render_template
from home.views import home_view
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField #can also add ImageField
from wtforms.validators import DataRequired, InputRequired, Email, Length #if you didnt type something in the field it will alert, (there's validators for email addresses)
from flask_sqlalchemy import SQLAlchemy #database
from datetime import datetime #keeps track of things added to the database


app = Flask(__name__)  # Create application object
app.config['SECRET_KEY'] = "my super secret key"

# #Create a Form Class
class NamerForm(FlaskForm):
	name = StringField("Enter Username", validators=[DataRequired()])
	submit = SubmitField("Submit")

#Create profile Page
@app.route('/login_page', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	#Validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''

	return render_template("login_page.html",
		name = name,
		form = form)

app.register_blueprint(home_view)
#set route
@app.route('/')

#set template to route
def index():
	return render_template("home_page.html")

# localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
	return render_template("login_page.html", name=name)


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
