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

TODO
    - rename this file

"""
import hashlib
import logging
import os
import secrets
import sys
import webbrowser
from pathlib import Path
from threading import Timer

from flask import (Flask, flash, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_bootstrap import Bootstrap  # TODO fix this
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import powerhourdownloader.debug_variables as ph_vars
from powerhourdownloader import __version__
from powerhourdownloader.mytube60_parser import (MyTube60Parser,
                                                 example_mytube60_parser_setup)
from powerhourdownloader.power_hour import DownloadStatusEnum
from powerhourdownloader.power_hour_runner import PowerHourRunner
from powerhourdownloader.transition import Transition
from powerhourdownloader.transition_video import TransitionVideo
from powerhourdownloader.video_link import VideoLink
from powerhourdownloader.youtube_video import YoutubeVideo

# TODO left off here https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html

app = Flask(__name__)
print(f'{app.template_folder=}')

foo = secrets.token_urlsafe(16)
app.secret_key = foo
## Bootstrap-Flask requires this line
#bootstrap = Bootstrap(app)
## Flask-WTF requires this line
#csrf = CSRFProtect(app)

# TODO deal with this
#messages = [
#    {
#        'title': 'Message One',
#        'content': 'tyler-output.mp3'
#    },  # TODO dont hardcode
#    {
#        'title': 'Message Two',
#        'content': 'tyler-output.mp4'
#    },  # TODO dont hardcode
#]

messages = []

# TODO test tyler
power_hour_runner = None
mytube60 = None
percentage = 0  # TODO remove this
combine_percentage = 5
write_percentage = 25
pyinstaller_in_use = False

if getattr(sys, 'frozen', False):
    # When running app as executable from pyinstaller
    pyinstaller_in_use = True
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # When running app from command line
    app = Flask(__name__)

def hash_file(filename):
    """Generate SHA-256 hash of the specified file."""
    hash_sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in chunks of 4K
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

if getattr(sys, 'frozen', False):
    # The application is frozen
    exe_path = sys.executable
else:
    # The application is not frozen
    # (e.g., running in a development environment)
    exe_path = __file__


print("Executable Path:", exe_path)
file_hash = hash_file(exe_path)
print("SHA-256 Hash:", file_hash)

# @app.route('/')
# def hello_world():
#    return 'Hello, World!'


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    global pyinstaller_in_use
    if pyinstaller_in_use:
        uploads = Path(__file__).parent / 'powerhourdownloader' / 'videos'
    else:
        uploads = Path(__file__).parent.parent / 'videos'
    return send_from_directory(str(uploads), filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', messages=messages)

@app.route('/info')
def info():
    return render_template('info.html', version=__version__, file_hash=file_hash, exe_path=exe_path)


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


@app.route('/download-status')
def download_status():
    global power_hour_runner
    global mytube60

    if power_hour_runner is None:
        if mytube60 is not None:
            status = f'Verifying video #{mytube60.videos_verified}'
        else:
            status = DownloadStatusEnum.WAITING
    else:
        status = power_hour_runner.parser.power_hour.power_hour_status

        if status == DownloadStatusEnum.VIDEOS_DOWNLOADING:
            videos_downloaded = power_hour_runner.parser.power_hour.videos_downloaded
            total_videos = power_hour_runner.parser.power_hour.total_videos
            status += f': {videos_downloaded}/{total_videos}'

    return f'{{"status": "{status}"}}'


@app.route('/progress')
def progress():
    # Using the following two to try this
    # https://stackoverflow.com/questions/37531829/how-to-create-a-progress-bar-using-flask
    # https://stackoverflow.com/questions/24251898/flask-app-update-progress-bar-while-function-runs
    # TODO deal with progress for the final step of combining the video
    global percentage
    global power_hour_runner
    global combine_percentage
    global write_percentage

    if power_hour_runner is None:
        return str(0)

    videos_downloaded = power_hour_runner.parser.power_hour.videos_downloaded
    total_videos = power_hour_runner.parser.power_hour.total_videos

    percentage = 0
    if total_videos is None:
        percentage = 0
    else:
        if (
            power_hour_runner.parser.power_hour.power_hour_status == DownloadStatusEnum.VIDEOS_DOWNLOADING
            or power_hour_runner.parser.power_hour.power_hour_status == DownloadStatusEnum.VIDEOS_COMBINING
        ):
            base = 100 - combine_percentage - write_percentage
        elif power_hour_runner.parser.power_hour.power_hour_status == DownloadStatusEnum.VIDEOS_WRITING:
            base = 100 - write_percentage
        elif power_hour_runner.parser.power_hour.power_hour_status == DownloadStatusEnum.VIDEOS_DONE:
            base = 100
        else:
            base = 0
        percentage = (videos_downloaded / total_videos) * base

    print(percentage)
    return str(percentage)


@app.route('/ph/', methods=('GET', 'POST'))
def create_power_hour():
    if request.method == 'POST':
        # TODO left off here what do we need next,
        # options
        """
        mytube60link
        transition / link
        mp3 only

        also need to add download option
        """
        # TODO verify webpage link
        # TODO verify webpage link x2
        webpage_link = request.form['webpage_link']
        audio_only = 'audio_only' in request.form
        transition_link = request.form['transition_link']
        start_time = request.form.get('start_time', None)
        end_time = request.form.get('end_time', None)

        # Convert start and end times to integers if provided
        start_time = int(start_time) if start_time else None
        end_time = int(end_time) if end_time else None
        if not webpage_link:
            flash('Webpage link is required!')
        else:
            # This is where you would add your logic to use these inputs
            print("Webpage Link:", webpage_link)
            print("Audio Only:", audio_only)
            print("Start Time:", start_time)
            print("End Time:", end_time)
            print('Hello Tyler')
            if not ph_vars.flask_log:
                log = logging.getLogger('werkzeug')
                log.setLevel(logging.ERROR)
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            # TODO transitions not implemented yet
            global mytube60
            mytube60 = MyTube60Parser(link=webpage_link)
            mytube60.parse(audio_only=audio_only)
            # TODO this needs to be gifured out
            if transition_link != '':
                transition_video = YoutubeVideo(
                        video_link=VideoLink(video_link=transition_link),
                        name=None,
                        video=None,
                        start_time=start_time,
                        end_time=end_time,
                )
                transition_video.download()
                mytube60.power_hour.transitions = TransitionVideo(
                    video=transition_video.video,
                )
            global power_hour_runner
            power_hour_runner = PowerHourRunner(parser=mytube60)
            power_hour_runner.run()

            # TODO verify what happens after button is hit and you change fields (maybe click mp3 button)

            # TODO show status
            # TODO make this downloadable link
            # We dont want to redirect but I want to keep this here to show how to redirect
            messages.append(
                {
                    'title': str(power_hour_runner.parser.power_hour.title),
                    'content': str(power_hour_runner.parser.power_hour.output.name),
                }
                 )
            return redirect(url_for('index'))
    return render_template('ph.html')
# TODO left off here: https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
# TODO left off at step 3, finished it but not working fully. Does not update the main page yet when submiting a form


class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?',
                       validators=[DataRequired(), Length(10, 40)])
    submit = SubmitField('Submit')

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')


def main():
    Timer(1, open_browser).start()
    app.run()

if __name__ == '__main__':
    main()
