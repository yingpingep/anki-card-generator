import abc
import json
import logging
import os.path

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
        self.logger = logging.getLogger(__name__)
        self.model = "gpt-3.5-turbo"
        self.client = client
        self.prompt = "You will act like a dictionary search engine. Your job is to retrieve necessary result about the input. The input could be a phrase, a noun, or a verb. If you are asking to provide Chinese, make sure you're returning it in Traditional Chinese. Take your time to think about it. You should keep the input as it is."

    def generate(self, param: str) -> CardResult:
        card_result = self._gen_result_via_gpt(param)

        self._gen_audio_file(param)

        card_result.speakFilePath = f"[sound:{param.replace(" ", "_")}.mp3]"
        return card_result

    def _gen_audio_file(self, param):
        speech_file_path = f"out/{param.replace(' ', '_')}.mp3"

        if os.path.exists(speech_file_path):
            self.logger.info(f"Speech file already exists: {speech_file_path}")
            return

        with self.client.audio.with_streaming_response.speech.create(
                model="tts-1",
                voice="alloy",
                input=param
        ) as resp:
            resp.stream_to_file(speech_file_path)
            self.logger.info(f"Speech file generated: {speech_file_path}")

    def _gen_result_via_gpt(self, param):
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

        if not tool_calls:
            self.logger.error(msg.content)
            raise ValueError("No tool calls found in response")

        arguments = tool_calls[0].function.arguments
        card_result = CardResult(**json.loads(arguments))

        return card_result
