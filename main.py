import csv
import os
import signal

from dotenv import load_dotenv
from openai import OpenAI

from helpers.card_generator import CardGeneratorImpl

load_dotenv()


def interrupt_handler(sign, handler):
    print("\nExiting...")
    exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)

    content_path = os.path.join(os.path.dirname(__file__), "out/content.csv")
    keyes = set()
    if os.path.exists(content_path):
        with open(content_path, "r") as f:
            csv_reader = csv.reader(f.readlines())
            for row in csv_reader:
                if len(row) == 0:
                    continue
                keyes.add(row[0])
    else:
        with open(content_path, "w") as f:
            f.write("word,partOfSpeech,plural,meaning,pronunciation,speakFilePath,chinese,example,pastTense,pp")

    card_generator = CardGeneratorImpl(OpenAI(api_key=os.environ.get("OPENAI_API_KEY")))

    while True:
        word = input("Enter a word: ")

        if word in keyes:
            print("The word is already in the list")
            continue

        try:
            result = card_generator.generate(word)
        except ValueError as e:
            print(e)
            continue

        with open(content_path, "a") as f:
            f.write("\n")
            f.write(result.get_csv_line())
