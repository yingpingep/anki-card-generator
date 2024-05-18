from helpers.card_generator import CardGenerator
from schema.card_result import CardResult


class FakeCardGenerator(CardGenerator):
    def generate(self, param: str) -> CardResult:
        if param == "apple":
            return CardResult(
                word=param,
                partOfSpeech="noun",
                plural="apples",
                meaning="a fruit",
                pronunciation="ˈapəl",
                example="An apple a day keeps doctor away",
                speakFilePath="path/to/speakFile",
                chinese="蘋果",
            )
        else:
            return CardResult(
                word=param,
                partOfSpeech="phrase",
                meaning="to move quickly",
                pronunciation="ˈrən fæst",
                speakFilePath="path/to/speakFile",
                example="Run Barry run fast",
                chinese="跑快點",
            )
