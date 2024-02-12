from csv import writer
from wordfreq import word_frequency  # , zipf_frequency
from tqdm import tqdm
import os

languages = [
    "ar",
    "bn",
    "bs",
    "bg",
    "ca",
    "zh",
    "hr",
    "cs",
    "da",
    "nl",
    "en",
    "fi",
    "fr",
    "de",
    "el",
    "he",
    "hi",
    "hu",
    "is",
    "id",
    "it",
    "ja",
    "ko",
    "lv",
    "lt",
    "mk",
    "ms",
    "nb",
    "fa",
    "pl",
    "pt",
    "ro",
    "ru",
    "sl",
    "sk",
    "sr",
    "es",
    "sv",
    "fil",
    "ta",
    "tr",
    "uk",
    "ur",
    "vi",
]


def get_word_frequencies(file_path, language_code):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            words = [line.strip() for line in file.readlines()]

        results = {}
        for word in tqdm(words, desc="Calcolo delle frequenze", unit="parole"):
            word_f = word_frequency(word, language_code)
            word_f_decimal_notation = "{:.15f}".format(word_f)
            # zipf_f = zipf_frequency(word, language_code)
            # results[word] = (word_f_decimal_notation, zipf_f)
            results[word] = word_f_decimal_notation

        return results

    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non è stato trovato.")
    except Exception as e:
        print(
            f"Errore: Si è verificato un problema durante l'elaborazione del file. Dettagli: {str(e)}"
        )


def save_to_csv(frequencies, output_file):
    try:
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = writer(csvfile)
            # csv_writer.writerow(["Parola", "Frequenza", "Frequenza Zipf"])
            csv_writer.writerow(["Parola", "Frequenza"])

            for word, frequency in frequencies.items():
                # csv_writer.writerow([word, frequency[0], frequency[1]])
                csv_writer.writerow([word, frequency])

        print(f"I risultati sono stati salvati in '{output_file}'.")

    except Exception as e:
        print(
            f"Errore: Si è verificato un problema durante il salvataggio del file CSV. Dettagli: {str(e)}"
        )


def get_input(
    prompt: str,
    default: str,
    expected_extension: str = "",
    check_file_exists: bool = False,
    possible_values: list = [],
):
    while True:
        input_data = input(prompt)
        input_data = input_data if input_data != "" else default

        if expected_extension != "":
            if input_data.lower().endswith(expected_extension):
                if check_file_exists and not os.path.isfile(input_data):
                    print(f"Errore: Il file {input_data} non è stato trovato.")
                else:
                    return input_data
            else:
                print(f"Errore: Il file non è in formato {expected_extension}")

        elif possible_values != []:
            if input_data in possible_values:
                return input_data
            else:
                print(
                    f"Errore, l'input deve essere uno di questi valori {possible_values}"
                )

        else:
            return input_data


def run():
    input_file = get_input(
        "Inserisci file di input in formato txt (default words.txt): ",
        "words.txt",
        ".txt",
        True,
    )
    output_file = get_input(
        "Inserisci file di output in formato csv (default results.csv): ",
        "results.csv",
        ".csv",
    )
    language_code = get_input(
        "Inseriscila lingua (default it): ",
        "it",
        possible_values=languages,
    )

    frequencies = get_word_frequencies(input_file, language_code)
    if frequencies:
        save_to_csv(frequencies, output_file)


if __name__ == "__main__":
    run()
