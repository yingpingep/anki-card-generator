from typing import Optional

from pydantic import BaseModel, Field


class CardResult(BaseModel):
    word: str
    partOfSpeech: str
    plural: Optional[str] = ""
    meaning: str
    pronunciation: str
    speakFilePath: Optional[str] = ""
    chinese: str = Field(..., description="Then Traditional Chinese translation of the word")
    example: str
    pastTense: Optional[str] = ""
    pp: Optional[str] = ""

    def get_csv_line(self):
        # word,partOfSpeech,plural,meaning,pronunciation,
        # speakFilePath,chinese,example,pastTense,pp
        return (f"{self.word},{self.partOfSpeech},{self.plural},{self.meaning},{self.pronunciation},"
                f"{self.speakFilePath},{self.chinese},{self.example},{self.pastTense},{self.pp}")
