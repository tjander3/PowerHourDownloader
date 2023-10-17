from dataclasses import dataclass

from powerhourdownloader.power_hour_parser import PowerHourParser


@dataclass
class PowerHourRunner:
    parser: PowerHourParser

    def run(self):
        raise NotImplementedError

def main() -> None:
    raise NotImplementedError

if __name__ == 'main':
    main()
