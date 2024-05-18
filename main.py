import os

from dotenv import load_dotenv
from openai import OpenAI

from helpers.card_generator import CardGeneratorImpl

load_dotenv()

if __name__ == "__main__":
    card_generator = CardGeneratorImpl(OpenAI(api_key=os.environ.get("OPENAI_API_KEY")))
    result = card_generator.generate("Great Refractor")
    print(result.get_csv_line())
