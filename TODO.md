# TODO

Since I am doing small incremental work on this project it would take too much time to create issues for inital code develpment. Instead I will just add some tasks to this file so I can keep up to date on what I am doing / need to do.

- [x] Bring in my bashrc
- [ ] Create README.md
- [ ] .github ci/cd once tests framework is stood up
- [ ] Start adding tests for classes
- [ ] Start implementing the classes (come up with order to implement first)
- [ ] List of classes
    - PowerHourRunner
    - PowerHour
    - PowerHourParser
    - MyTube60Parser
    - Location
    - TextVideoOverlay
    - Transition
    - TransitionVideo
    - TransitionImage
    - YoutubeVideo
    - VideoLink

- [ ] Is is possible to not download all of youtube video (just a section)?
- [x] -nsync is not downloading in webapp
- [x] add mp3
    - [x] youtube audio class
    - [x] need to fix power_hour to reflect this as well
- [x] Progress for downloading
    - [x] command line
    - [>] HTML (moved below)
- [x] Download options
    - [x] single mp4
    - [x] single mp3 (option to keep transitions or not)
    - [>] multiple mp3 (no transitions)
- [x] name resulting power hour based on the name of the given power hour... duh
- webpage
    - [ ] download the power hour
    - [ ] show status
    - [ ] navigate to other pages while downloading
- auto upload
    - [ ] google drive
        - [ ] update class diagram
        - [ ] authentication?
        - [ ] implement

## TODO list order

- Status Bar
    - https://blog.miguelgrinberg.com/post/using-celery-with-flask
    - https://github.com/miguelgrinberg/flask-celery-example/blob/master/templates/index.html
- Deploy / Get to Andy
    - python executable
- version it
- Upload to drive
    - create shared drive terpmail
    - create way to authenticate to google
    - upload to terpmail drive (will need to be shared with user)
- clean up webpage
    - only keep needed menus
    - make it pretty

- Download power hour not working in app
- document how to build: `pyinstaller --onefile --add-data "templates;templates" .\hello_world.py`
- rename `hello_world.py`
- display 1/60 2/60 etc in webapp
- dont allow double submit


C:\Users\tjand\AppData\Local\Temp\_MEI240322\powerhourdownloader\videos\2000s-Power-Hour.mp4
uploads=WindowsPath('C:/Users/tjand/AppData/Local/Temp/videos')

