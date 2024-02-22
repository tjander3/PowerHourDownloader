from dataclasses import dataclass

import youtube_dl


@dataclass
class VideoLink:
    video_link: str

    def verify_video_link(self) -> bool:
        # Got this from here: <https://stackoverflow.com/questions/61465405/how-to-check-if-a-url-is-valid-that-youtube-dl-supports>
        try:
            youtube_dl.YoutubeDL({'quiet': True}).extract_info(self.video_link, download=False)
            return True
        except Exception:
            return False


def main():
    bad_link = 'https://www.youtube.com/watch?v=dpq4gmj-7ys'
    assert not VideoLink(bad_link).verify_video_link()

    good_link = 'https://www.youtube.com/watch?v=mvVBuG4IOW4'
    assert VideoLink(good_link).verify_video_link()

if __name__ == '__main__':
    main()
