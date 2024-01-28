```mermaid
---
title: Power Hour Downloader
---
%% The details of mermaid classDiagram are found here: https://mermaid.js.org/syntax/classDiagram.html
classDiagram
    PowerHourRunner -- PowerHourParser
    class PowerHourRunner {
        PowerHourParser parser
        FileStorage file_storage

        run() -> None
        main() -> None
        store_file()
    }

    PowerHour "1" --o "*" Video: has
    PowerHour "1" --o "*" Transition: has
    class PowerHour {
        list[Video] videos
        list[Transition] transitions

        create_power_hour() -> Path
        save_power_hour() -> Path
        upload_power_hour() -> None
    }

    PowerHourParser -- PowerHour
    class PowerHourParser {
        <<abstract>>
        PowerHour power_hour

        parse() -> PowerHour
    }

    PowerHourParser <|-- MyTube60Parser
    class MyTube60Parser {
        PowerHour power_hour
        Path link

        parse() -> PowerHour
    }

    class Location {
        %% Coordinates for where TextOverlay will be placed
        %% Default should be the center of the screen
        int x = 0
        int y = 0
    }


    TextVideoOverlay "1" --* "1" Location : located at
    class TextVideoOverlay {
        str text
        Color text_color
        Location text_location
    }

    class Transition {
        <<abstract>>
        Path video
        TextVideoOverlay text = None
        Audio audio = None

        _add_text_to_video() -> None
        _add_audio_to_video() -> None
    }

    Transition <|-- TransitionVideo
    class TransitionVideo {
        Path video
        TextVideoOverlay text = None
        Audio audio = None

        _add_text_to_video() -> None
        _add_audio_to_video() -> None
    }

    Transition <|-- TransitionImage
    class TransitionImage {
        int _length
        Image _image
        Path video
        TextVideoOverlay text = None
        Audio audio = None

        _image_to_video() -> None
        _add_text_to_video() -> None
        _add_audio_to_video() -> None
    }

    class Video{
        <<abstract>>
        VideoLink video_link
        Path video
        str name
        float start_time
        float end_time

        download() -> None
        setup_download_dir() -> None:
    }

    Video <|-- YoutubeVideo
    class YoutubeVideo {
        VideoLink video_link
        Path video
        str name
        float start_time
        float end_time

        download(start_time=None, end_time=None) -> None
    }

    YoutubeVideo <|-- YoutubeAudio
    class YoutubeAudio {
        VideoLink video_link
        Path video
        str name
        float start_time
        float end_time

        download(start_time=None, end_time=None) -> None
    }

    Video -- VideoLink
    class VideoLink {
        str video_link

        verify_video_link() -> bool
    }

    PowerHourRunner -- FileStorage
    class FileStorage {
        Path file
        StorageProvider storageProvider

        store_file()
    }

    FileStorage -- StorageProvider
    class StorageProvider {
        <<abstract>>

        authenticate()
        file_upload()
    }

    StorageProvider <|-- GoogleDrive
    class GoogleDrive {

        authenticate()
        file_upload()
    }
```
