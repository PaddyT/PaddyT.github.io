import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, send_file
from contextlib import closing
# from flask.ext.mail import Mail, Message
from flask_mail import Mail, Message

# configuration
DATABASE = '/tmp/mydb.db'
DEBUG = False
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
MAIL_SERVER = 'smtp.virgin.net'
MAIL_DEFAULT_SENDER = 'donotreply@patricktesh.com'

app = Flask(__name__)
app.config.from_object(__name__)
mail = Mail(app)

"""
TODO:   BOOTSTRAP
        REMOVE LOGIN
        FRONT PAGE WITH BIO
        BLOG PAGE
        SOCIAL MEDIA LINKS

"""

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/cv')
def cv():
    return send_file('assets/PTeshCV.pdf')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/send', methods=['POST'])
def sender():
    txt = request.form['message']
    email = request.form['email']
    msg = Message(subject='Inquiry',
                  sender=email,
                  recipients=["patrick_tesh@outlook.com"],
                  body=txt)
    mail.send(msg)
    flash('Message sent!')
    return redirect(url_for('contact'))


if __name__ == "__main__":
    init_db()
    app.run()
    # Finally we use the run() function to run the local server with our application. The if __name__ == '__main__':
    # makes sure the server only runs if the script is executed directly from the Python interpreter and not used as an
    # imported module.
