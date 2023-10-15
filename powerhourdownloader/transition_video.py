from powerhourdownloader.transition import Transition


class TransitionVideo(Transition):
    def __init__(self) -> None:
        raise NotImplementedError

    def _add_text_to_video(self) -> None:
        raise NotImplementedError

    def _add_audio_to_video(self) -> None:
        raise NotImplementedError
