import re

import pandas as pd

from utils import process_files_input, split_input
from wordfreq_logic import get_word_frequencies


class GroupedWords:
    def __init__(self, words: list[str], language, index):
        self.index = index
        self.words = words
        self.frequencies = self.compute_frequencies(language)

    def __eq__(self, other):
        return self.index == other.index and self.words == other.words

    def append_list(self, grouped_obj: "GroupedWords") -> None:
        if grouped_obj:
            unique_words = dict.fromkeys(self.words + grouped_obj.words)
            self.words = list(unique_words.keys())
            self.frequencies.update(grouped_obj.frequencies)

    def compute_frequencies(self, language: str) -> dict:
        frequencies = get_word_frequencies(self.words, language)
        frequencies = {key.capitalize(): f for key, f in frequencies.items()}
        return frequencies


class FrequencyPageManager:
    def __init__(self, id: int):
        self.id = id
        self.n = 0
        self.words_inserted_before = []
        self.words = []
        self.language = ""

    def clean_word(self, text: str) -> str:
        # Remove any character that is not a letter or a space, keeping accented characters
        cleaned_text = re.sub(r"[^a-zA-ZàùèòìáéíóúâêîôûÀÙÈÒÌÁÉÍÓÚÂÊÎÔÛ\s]", "", text)
        return cleaned_text.strip()

    def clean_words(self, words: list[str]) -> dict[GroupedWords]:
        grouped_words = {}
        current_group = []
        current_index = None

        for word in words:
            match = re.match(r"(\d+)\s*\)", word)
            if match:
                if current_group:
                    current_group = list(dict.fromkeys(current_group))
                    grouped_words[current_index] = GroupedWords(
                        current_group, self.language, current_index
                    )

                current_index = int(match.group(1))
                current_group = []

            cleaned_word = self.clean_word(word)
            if cleaned_word:
                current_group.append(cleaned_word)

        if current_group:
            current_group = list(dict.fromkeys(current_group))
            grouped_words[current_index] = GroupedWords(current_group, self.language, current_index)

        return grouped_words

    def get_words(self, words_input: str, uploaded_files: list[str]) -> list[GroupedWords]:
        words = self.clean_words(split_input(words_input))
        files_content = process_files_input(uploaded_files)
        words_file = self.clean_words(split_input(files_content))

        merged_words = []
        for key in set(words.keys()).union(words_file.keys()):
            to_append = words.get(key, GroupedWords([], self.language, key))
            to_append.append_list(words_file.get(key, None))
            merged_words.append(to_append)

        return merged_words

    def compute_frequencies(
        self, words_input: str, uploaded_files: list[str], language: str
    ) -> None:
        self.language = language
        self.words = self.get_words(words_input, uploaded_files)
        words_inserted = [group.words for group in self.words]
        if words_inserted == self.words_inserted_before:
            return
        self.words_inserted_before = words_inserted.copy()
        self.n += 1

    def to_df(self) -> pd.DataFrame:
        data = {}
        for group in self.words:
            data.update(group.frequencies)

        df = pd.DataFrame(data.items(), columns=["Word", "Frequency"])
        df["Frequency"] = pd.to_numeric(df["Frequency"])
        df["Frequency"] = df["Frequency"].apply(lambda x: format(x, ".15f").rstrip("0").rstrip("."))
        return df

    def total_words(self) -> int:
        return len(set(word for group in self.words for word in group.words))
