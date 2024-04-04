from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

import youtube_dl

from powerhourdownloader.debug_variables import ci_youtube_dl_down


@dataclass
class VideoLink:
    video_link: str

    def verify_video_link(self) -> bool:
        """Verify if video link works.

        We use youtube-dl so if youtubedl does not support the website
        this will make it false.

        We also check to make sure that the video is possible to downlad to avoid downloading bad videos.
        """
        # Got this from here: <https://stackoverflow.com/questions/61465405/how-to-check-if-a-url-is-valid-that-youtube-dl-supports>
        if ci_youtube_dl_down:
            return True
        try:
            youtube_dl.YoutubeDL({'quiet': True}).extract_info(self.video_link, download=False)
            return True
        except Exception:
            return False

def verify_video_link_concurrently(video_links: list[VideoLink]):
    """Verify a list of video links concurrently."""
    from powerhourdownloader.video import Video  # TODO this is terrible practice
    with ThreadPoolExecutor() as executor:
        if isinstance(video_links[0], Video):
            future_to_link = {executor.submit(link.video_link.verify_video_link): link for link in video_links}
        else:  # Video Link
            future_to_link = {executor.submit(link.verify_video_link): link for link in video_links}

        for future in as_completed(future_to_link):
            link = future_to_link[future]
            try:
                result = future.result()
                yield (link, result)
            except Exception as exc:
                yield (link, False)

def main():
    # Power hour with bad link https://www.mytube60.com/video/on/ttpmoose---movies/db30aa60461b4a3fa4375724b61b8013.html
    bad_link = 'https://www.youtube.com/watch?v=xxx'
    assert not VideoLink(bad_link).verify_video_link()

    good_link = 'https://www.youtube.com/watch?v=mvVBuG4IOW4'
    assert VideoLink(good_link).verify_video_link()

    video_links = [VideoLink(good_link), VideoLink(bad_link)]
    results = list(verify_video_link_concurrently(video_links))
    assert (VideoLink(good_link), True) in results
    assert (VideoLink(bad_link), False) in results


if __name__ == '__main__':
    main()
