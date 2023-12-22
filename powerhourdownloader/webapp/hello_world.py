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
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap  # TODO fix this
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# TODO left off here https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

app = Flask(__name__)
print(f'{app.template_folder=}')

foo = secrets.token_urlsafe(16)
app.secret_key = foo
# Bootstrap-Flask requires this line
bootstrap = Bootstrap(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

# @app.route('/')
# def hello_world():
#    return 'Hello, World!'


@app.route('/', methods=['GET', 'POST'])
def index():
    messages = [{'title': 'Message One',
                 'content': 'Message One Content'},
                {'title': 'Message Two',
                 'content': 'Message Two Content'}
                ]

    return render_template('index.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('create.html')

# TODO left off here: https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
# TODO left off at step 3


class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?',
                       validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Submit')
