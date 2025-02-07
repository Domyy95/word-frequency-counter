from wordfreq import word_frequency

languages = {"it": "🇮🇹", "en": "🇬🇧", "fr": "🇫🇷", "es": "🇪🇸", "de": "🇩🇪", "nl": "🇳🇱"}


def get_word_frequencies(words: list[str], language_code: str) -> dict:
    results = {}
    for word in words:
        word_f = word_frequency(word, language_code)
        word_f_decimal_notation = "{:.15f}".format(word_f)
        results[word] = word_f_decimal_notation

    return results
