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
        # TODO left off here: see this https://stackoverflow.com/questions/54607447/opencv-how-to-overlay-text-on-video
        # TODO this could be in the parent class
        # Python program to write
        # text on video
        import cv2
        video_path = Path(__file__).parent / '..' / 'videos' / 'hello-there.mp4'
        print(video_path.absolute())
        print(f'video exits: {video_path.exists()}')
        from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

        video = VideoFileClip(str(video_path))#.subclip(50,60)

        # Make the text. Many more options are available.
        txt_clip = ( TextClip("My Holidays 2013",fontsize=70,color='white')
                     .set_position('center')
                     .set_duration(10) )  # TODO duration should be whole clip

        result = CompositeVideoClip([video, txt_clip]) # Overlay text on video
        result.write_videofile("myHolidays_edited.mp4",fps=25) # Many options...

        return
        # TODO left off here please clean up this code

        tree_video = cv2.VideoCapture(str(video_path))

        print(tree_video)

        fps = tree_video.get(cv2.CAP_PROP_FPS)
        print(fps)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('tyler.avi', fourcc, 20.0, (640,480))
        # This is from here : https://stackoverflow.com/questions/73663569/python-opencv-how-to-write-text-on-video-output-mp4-empty
        # TODO having problems getting write out to work
        try:
            while(True):

                # Capture frames in the video
                ret, frame = tree_video.read()

                font = cv2.FONT_HERSHEY_SIMPLEX

                cv2.putText(frame,
                            'TEXT ON VIDEO',
                            (50, 50),
                            font, 1,
                            (0, 640, 480),
                            2,
                            cv2.LINE_4)
                out.write(frame)
                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


            #tree_video.release()
            #out.release()


            #cv2.destroyAllWindows()
        except:
            print("Video has ended.")
        tree_video.release()
        out.release()
        cv2.destroyAllWindows()

        return
        frame_ = 0

        while True:
            ret, frame = tree_video.read()
            font = cv2.FONT_HERSHEY_SIMPLEX

            #on_video_text = text_update(frame_)
            on_video_text = 'Hello There'
            cv2.putText(frame, on_video_text, (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)

            frame_ = frame_ + 1

            cv2.imshow('poem on video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            tree_video.release()
            cv2.destroyAllWindows()

            if frame_ > 1000000:
                break


        return


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
