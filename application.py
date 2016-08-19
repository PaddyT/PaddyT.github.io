from flask import Flask, request, render_template, flash, send_file, redirect, url_for
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
import re

# Config
SECRET_KEY = 'none'
DEBUG = False
MAIL_SERVER = 'smtp.virgin.net'
MAIL_DEFAULT_SENDER = 'donotreply@patricktesh.com'

EMAIL_REGEX = re.compile(r'[\w]+@[.\w]+')

app = Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)
bootstrap = Bootstrap(app)
nav = Nav(app)

"""
TODO:   FRONT PAGE WITH BIO
        BLOG PAGE
        SOCIAL MEDIA LINKS
"""

nav.register_element('navigation',
                     Navbar(View('Home', 'front'),
                            View('Contact', 'contact'),
                            View('CV', 'cv')
                            )
                     )


@app.route('/')
def front():
    return render_template('front.html')


@app.route('/contact')
def contact(error=None):
    return render_template('contact.html', error=error)


@app.route('/cv')
def cv():
    return send_file('assets/PTeshCV.pdf')


@app.route('/send', methods=['POST'])
def sender():
    error = None
    txt = request.form['message']
    email = request.form['email']
    if EMAIL_REGEX.fullmatch(email):
        msg = Message(subject='Submission',
                      sender='noreply@PaddyT.github.io',
                      recipients=['patrick_tesh@outlook.com'],
                      body=' - '.join([email, txt]))
        mail.send(msg)
        flash('Message sent!')
    else:
        error = 'Invalid email'
        flash('Invalid email', category=error)
    return redirect(url_for('contact', error=error))


if __name__ == "__main__":
    app.run()
