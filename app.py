"""
app.py
"""
import re

from flask import Flask, flash, render_template, request, redirect, \
    send_file, url_for
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View


# Debug flag
DEBUG = False

SECRET_KEY = 'none'

# Flask Mail
MAIL_SERVER = 'smtp.virgin.net'
MAIL_DEFAULT_SENDER = 'donotreply@PaddyT.github.io'
EMAIL_REGEX = re.compile(r'[\w]+@[.\w]+')

# Create app
app = Flask(__name__)
app.config.from_object(__name__)

# Flask Mail
mail = Mail(app)

# Flask Bootstrap
bootstrap = Bootstrap(app)

# Naviagtion bar
nav = Nav(app)
nav.register_element('navigation',
                     Navbar(View('Home', 'front'),
#                            View('Sign Up', 'signup'),
                            View('Contact', 'contact'),
                            View('CV', 'cv')))


@app.route('/')
def front():
    return render_template('front.html')


@app.route('/signup')
def signup(error=None):
    return render_template('signup.html', error=error)


@app.route('/contact')
def contact(error=None):
    return render_template('contact.html', error=error)


@app.route('/cv')
def cv():
    return send_file('assets/PTeshCV.pdf',
                     )


@app.route('/send', methods=['POST'])
def sender():
    error = None
    txt = request.form['message']
    email = request.form['email']
    print(txt, email)
    if EMAIL_REGEX.fullmatch(email):
        msg = Message(subject='Contact',
                      sender=email,
                      recipients=['patrickjamestesh@gmail.com'],
                      body=txt)
        mail.send(msg)
        flash('Message sent!')
    else:
        error = 'Invalid email'
        flash('Invalid email', category=error)
    return redirect(url_for('contact', error=error))


if __name__ == "__main__":
    app.run(host='127.0.0.1',
            port=8080)
