"""
Test flask app.

To run do the following:

Linux:
```
$ export FLASK_APP=hello.py
$ flask run
```

Windows:
cmd:

```
C:\path\to\app>set FLASK_APP=hello.py
$ flask run
```

powershell:

```
PS C:\path\to\app> $env:FLASK_APP = "hello.py"
$ flask run
```

other notes:

you can also run with:

```
$ python -m flask run
```

"""
import secrets
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap  # TODO fix this
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# TODO left off here https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

app = Flask(__name__)
print(f'{app.template_folder=}')

foo = secrets.token_urlsafe(16)
app.secret_key = foo
## Bootstrap-Flask requires this line
#bootstrap = Bootstrap(app)
## Flask-WTF requires this line
#csrf = CSRFProtect(app)

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

# @app.route('/')
# def hello_world():
#    return 'Hello, World!'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/ph/', methods=('GET', 'POST'))
def create_power_hour():
    if request.method == 'POST':
        print('Hello Tyler')
    return render_template('ph.html')

# TODO left off here: https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
# TODO left off at step 3, finished it but not working fully. Does not update the main page yet when submiting a form


class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?',
                       validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Submit')
