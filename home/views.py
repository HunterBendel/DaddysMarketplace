from flask import Blueprint, render_template

home_view = Blueprint('home_view', __name__)

@home_view.route('/')  # Route for the page
def display_home_page():
	return render_template('home_page.html', num=10)

@home_view.route('/profile_page') # Route for the profile page
def display_profile_page():
	return render_template('profile_page.html', num=10)

@home_view.route('/settings_page') # Route for the settings page
def display_settings_page():
	return render_template('settings_page.html', num=10)

@home_view.route('/login_page') # Route for the settings page
def display_login_page():
	return render_template('login_page.html', num=10)
