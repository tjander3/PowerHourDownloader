from pathlib import Path
import pytest

from powerhourdownloader.mytube60_parser import MyTube60Parser, main

class TestMyTube60Parser:
    pytest.mark.skip
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
    def test_mytube60_parser(self, test_name, link, webpage_path, golden):
        # If no internet connection use the pre downloaded file
        if webpage_path:
            with open(
                webpage_path,
                'r',
                encoding='utf-8',
            ) as f:
                webpage = f.read()
        else:
            webpage = webpage_path


        mytube60 = MyTube60Parser(link=link)
        mytube60.parse(debug=webpage)

        gold = golden.open(f'test_mytube60_parser/{test_name}.yml')
        assert mytube60.power_hour == gold.out["output"]

    def test_main(self):
        # We just want to verify main runs without any errors
        main()
