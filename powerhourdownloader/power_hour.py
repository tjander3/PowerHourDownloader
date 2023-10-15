from pathlib import Path


class PowerHour:
    def __init__(self) -> None:
        raise NotImplementedError

    def create_power_hour(self) -> Path:
        raise NotImplementedError

    def save_power_hour(self) -> Path:
        raise NotImplementedError

    def upload_power_hour(self) -> None:
        raise NotImplementedError
