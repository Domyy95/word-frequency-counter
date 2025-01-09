from wordfreq_logic import get_word_frequencies


class FrequencyPage:
    def __init__(self, id):
        self.id = id
        self.n = 0
        self.words_inserted_before = []
        self.results = {}

    def increment_n(self):
        # Increment the session state n by 0.5 because at every click the button is like is clicked twice
        self.n += 0.5

    def compute_frequencies(self, words, language):
        self.words_inserted_before = words
        results = {}
        try:
            results = get_word_frequencies(words, language)
            results = {key.capitalize(): f for key, f in results.items()}
        except Exception as e:
            print(f"Error computing word frequencies: {e}")

        self.results = results
