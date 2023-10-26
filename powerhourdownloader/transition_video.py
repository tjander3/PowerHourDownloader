from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
#from powerhourdownloader.text_video_overlay import TextVideoOverlay
#from powerhourdownloader.transition import Transition


@dataclass
class TransitionVideo():#Transition):
    video: Path
    text: Optional[str] = None #Optional[TextVideoOverlay] = None
    audio: Optional[Path] = field(default=None)

    def _add_text_to_video(self) -> None:
        # TODO this could be in the parent class
        # Python program to write
        # text on video
        import cv2


        cap = cv2.VideoCapture(Path('.') / '..' / 'videos' / 'hello-there.mp4')

        while(True):

            # Capture frames in the video
            ret, frame = cap.read()

            # describe the type of font
            # to be used.
            font = cv2.FONT_HERSHEY_SIMPLEX

            # Use putText() method for
            # inserting text on video
            cv2.putText(frame,
                        'TEXT ON VIDEO',
                        (50, 50),
                        font, 1,
                        (0, 255, 255),
                        2,
                        cv2.LINE_4)

            # Display the resulting frame
            cv2.imshow('video', frame)

            # creating 'q' as the quit
            # button for the video
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # release the cap object
        cap.release()
        # close all windows
        cv2.destroyAllWindows()

    def _add_audio_to_video(self) -> None:
        raise NotImplementedError

def main():
    tv = TransitionVideo(video='', text='Hello there', audio='xxx')
    tv._add_text_to_video()

if __name__ == '__main__':
    main()
