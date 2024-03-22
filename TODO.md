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

- rename `hello_world.py`
- cleanup files everywhere
- github actions outline
- tests
- coverage
- Upload to drive
    - create shared drive terpmail
    - create way to authenticate to google
    - upload to terpmail drive (will need to be shared with user)
- clean up webpage
    - only keep needed menus
    - make it pretty
- github actions
    - coverage
    - documentation building with sphinx

- next
- orgnaize this
- why are sizes of videos tiny
- option to download both mp3 and mp4 at same time
- after this verify transitions work
- todo two power hours in a row with same name deal with that
- TODO cleanup debug messages, only mine not others
- todo when you do two in arow you get a status bar ful for a bit
- verify videos actually exist do this with threads
    - percentage validating?
- bookkeeping
    - document how to build: `pyinstaller --onefile --add-data "templates;templates" .\hello_world.py`
- core functionality
    - fix transitions
    - power hour with the same name?
- ci/cd
    - automate release
- gui
    - dont allow double submit
    - cancel button
    - queue
    - list bad videos found and option to cancel
- other
    - look into yt_dlp
    - get executable not seen as a virus


C:\Users\tjand\AppData\Local\Temp\_MEI240322\powerhourdownloader\videos\2000s-Power-Hour.mp4
uploads=WindowsPath('C:/Users/tjand/AppData/Local/Temp/videos')