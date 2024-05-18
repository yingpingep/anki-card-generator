from helpers.card_generator import CardGenerator


class AnkiHelper:
    def __init__(self, card_generator: CardGenerator):
        self.card_generator = card_generator

    def get_info_for(self, param: str):
        result = self.card_generator.generate(param)
        msg = result.get_csv_line()
        return msg
