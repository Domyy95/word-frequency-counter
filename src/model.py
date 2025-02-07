import re

import pandas as pd

from utils import process_files_input, split_input
from wordfreq_logic import get_word_frequencies


class FrequencyPageManager:
    def __init__(self, id: int):
        self.id = id
        self.n = 0
        self.words_inserted_before = []
        self.words = []
        self.results = {}
        self.language = ""

    def clean_word(self, text: str) -> str:
        # Remove any character that is not a letter or a space, keeping accented characters
        cleaned_text = re.sub(r"[^a-zA-ZàùèòìáéíóúâêîôûÀÙÈÒÌÁÉÍÓÚÂÊÎÔÛ\s]", "", text)
        return cleaned_text

    def clean_words(self, words: list[str]) -> list[str]:
        result = list(dict.fromkeys(words))  # Remove double strings keeping the order of the list
        clean_result = []
        for word in result:
            clean_result.append(self.clean_word(word.strip()))
        clean_result = [word for word in clean_result if word]  # Remove empty words
        return clean_result

    def get_words(self, words_input: str, uploaded_files: list[str]) -> list[str]:
        words = self.clean_words(split_input(words_input))
        files_content = process_files_input(uploaded_files)
        words += self.clean_words(split_input(files_content))
        return words

    def compute_frequencies(
        self, words_input: str, uploaded_files: list[str], language: str
    ) -> None:
        self.words = self.get_words(words_input, uploaded_files)
        if self.words == self.words_inserted_before:
            return
        self.words_inserted_before = self.words.copy()
        self.language = language
        results = {}
        try:
            results = get_word_frequencies(self.words, language)
            results = {key.capitalize(): f for key, f in results.items()}
            self.n += 1
        except Exception as e:
            print(f"Error computing word frequencies: {e}")

        self.results = results

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.results.items(), columns=["Word", "Frequency"])
        df["Frequency"] = pd.to_numeric(df["Frequency"])
        df["Frequency"] = df["Frequency"].apply(lambda x: format(x, ".15f").rstrip("0").rstrip("."))
        return df
