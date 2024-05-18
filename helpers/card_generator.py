import abc
import json

from openai import OpenAI

from schema.card_result import CardResult


class CardGenerator(abc.ABC):
    @abc.abstractmethod
    def generate(self, param: str) -> CardResult:
        raise NotImplementedError


get_card_infor_tool = {
    "type": "function",
    "function": {
        "name": "CardResult",
        "description": "Generate a card result",
        "parameters": CardResult.model_json_schema()
    }
}


class CardGeneratorImpl(CardGenerator):
    def __init__(self, client: OpenAI):
        self.model = "gpt-3.5-turbo"
        self.client = client
        self.prompt = "You are a great assistant. You will received an input in English. You will provide the necessary information about the input. If you are asking to provide Chinese, make sure you're returning it in Traditional Chinese. The input could be very different, before you return a result, you can take your time to think about it. If the input is invalid, you can ask for a new input."

    def generate(self, param: str) -> CardResult:
        chat_response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": param},
            ],
            tools=[get_card_infor_tool]
        )

        msg = chat_response.choices[0].message
        tool_calls = msg.tool_calls
        if tool_calls:
            arguments = tool_calls[0].function.arguments
            return CardResult(**json.loads(arguments))
        else:
            raise ValueError(msg.content)
