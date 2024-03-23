from pathlib import Path
from typing import Optional
import pytest

from powerhourdownloader.mytube60_parser import MyTube60Parser, main

class TestMyTube60Parser:
    @pytest.mark.parametrize(
        'test_name, link, webpage_path',
        (
            (
                'emo_night',
                None,
                Path(__file__).parent / 'webpages' / 'mytube60-test-webpage-emo-night.html',
            ),
            # The following used internet to get webpage so this could fail
            (
                'emo_night',
                'https://www.mytube60.com/video/on/emo-night/b664367fb7ee40799dccbe693015d6f6.html',
                None,
            ),
        )
    )
    def test_mytube60_parser(self, test_name: str, link: str, webpage_path: Optional[Path], golden):
        # If no internet connection use the pre downloaded file
        if webpage_path:
            # Title is with - but test_name is with _. just hardcoding here.
            # If we add anymore tests we will need to rethink this line.
            test_debug = test_name.upper().replace('_', '-')
            with open(
                webpage_path,
                'r',
                encoding='utf-8',
            ) as f:
                webpage = f.read()
        else:
            test_debug = None
            webpage = webpage_path

        mytube60 = MyTube60Parser(link=link, test_debug=test_debug)
        mytube60.parse(debug=webpage)

        gold = golden.open(f'test_mytube60_parser/{test_name}.yml')
        # Hack to get golden-test to work
        mytube60.power_hour.power_hour_status = str(mytube60.power_hour.power_hour_status)
        # Dont keep full path as it will be different on different systems
        # TODO update goldens not working with these hardcoded things. pytewt-golden trying to recreate object
        mytube60.power_hour.output = str(mytube60.power_hour.output.name)
        assert mytube60.power_hour == gold.out["output"]

    def test_main(self):
        # We just want to verify main runs without any errors
        main()
