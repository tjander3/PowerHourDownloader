from dataclasses import dataclass

from powerhourdownloader.power_hour_parser import PowerHourParser
from powerhourdownloader.mytube60_parser import example_mytube60_parser_setup


@dataclass
class PowerHourRunner:
    parser: PowerHourParser

    def run(self):
        # TODO check to see if already parsed if not parse
        # self.parser.parse()
        power_hour = self.parser.power_hour
        power_hour.create_power_hour()

def main() -> None:
    power_hour_parser = example_mytube60_parser_setup()
    power_hour_runner = PowerHourRunner(parser=power_hour_parser)

    power_hour_runner.run()


if __name__ == 'main':
    main()
