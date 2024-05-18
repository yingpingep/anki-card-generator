from openai import OpenAI
from pytest_mock import MockFixture

from helpers.anki_helper import AnkiHelper
from helpers.card_generator import CardGeneratorImpl


def create_fake_open_ai_client(mocker):
    client = mocker.MagicMock(spec=OpenAI).return_value

    def set_tool_calls(return_value: list):
        client.chat.completions.create.return_value.choices[0].message.tool_calls = return_value

    client.set_tool_calls = set_tool_calls
    return client


def test_should_handle_word(mocker: MockFixture):
    gpt_response = '{"word": "apple", "partOfSpeech": "noun", "plural": "apples", "meaning": "a fruit", "pronunciation": "ˈapəl", "example": "An apple a day keeps doctor away", "speakFilePath": "", "chinese": "蘋果"}'

    client = create_fake_open_ai_client(mocker)
    client.set_tool_calls([
        mocker.MagicMock(
            function=mocker.MagicMock(arguments=gpt_response)
        )
    ])

    anki_helper = AnkiHelper(CardGeneratorImpl(client))
    result = anki_helper.get_info_for("apple")

    assert result == "apple,noun,apples,a fruit,ˈapəl,,蘋果,An apple a day keeps doctor away,,"


def test_should_handle_phrase(mocker: MockFixture):
    gpt_response = '{"word": "run fast", "partOfSpeech": "phrase", "meaning": "to move quickly", "pronunciation": "ˈrən fæst", "example": "Run Barry run fast", "speakFilePath": "", "chinese": "跑快點"}'

    client = create_fake_open_ai_client(mocker)
    client.set_tool_calls([
        mocker.MagicMock(
            function=mocker.MagicMock(
                arguments=gpt_response
            )
        )
    ])

    anki_helper = AnkiHelper(CardGeneratorImpl(client))
    result = anki_helper.get_info_for("run fast")
    assert result == "run fast,phrase,,to move quickly,ˈrən fæst,,跑快點,Run Barry run fast,,"
