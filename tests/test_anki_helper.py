import pytest

from helpers.anki_helper import AnkiHelper
from tests.fake_impl import FakeCardGenerator


@pytest.fixture
def card_generator():
    return FakeCardGenerator()


def test_should_handle_word(card_generator):
    anki_helper = AnkiHelper(card_generator)
    assert anki_helper.get_info_for(
        "apple") == "apple,noun,apples,a fruit,ˈapəl,path/to/speakFile,蘋果,An apple a day keeps doctor away,,"


def test_should_handle_phrase(card_generator):
    anki_helper = AnkiHelper(card_generator)
    assert anki_helper.get_info_for(
        "run fast") == "run fast,phrase,,to move quickly,ˈrən fæst,path/to/speakFile,跑快點,Run Barry run fast,,"
