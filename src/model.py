import pandas as pd
from wordfreq_logic import get_word_frequencies


class FrequencyPageManager:
    def __init__(self, id):
        self.id = id
        self.n = 0
        self.words_inserted_before = []
        self.results = {}
        self.language = ""

    def increment_n(self):
        # Increment the session state n by 0.5 because at every click the button is like is clicked twice
        self.n += 0.5

    def compute_frequencies(self, words, language):
        self.words_inserted_before = words
        self.language = language
        results = {}
        try:
            results = get_word_frequencies(words, language)
            results = {key.capitalize(): f for key, f in results.items()}
        except Exception as e:
            print(f"Error computing word frequencies: {e}")

        self.results = results

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self.results.items(), columns=["Word", "Frequency"])
        df["Frequency"] = pd.to_numeric(df["Frequency"])
        df["Frequency"] = df["Frequency"].apply(lambda x: format(x, ".15f").rstrip("0").rstrip("."))
        return df
