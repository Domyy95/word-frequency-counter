import streamlit as st
import pandas as pd
from logic import languages, get_word_frequencies


def initialize_session_states():
    st.session_state.n = 0
    st.session_state.words_inserted_before = []
    st.session_state.results = {}


def increment_n():
    # Increment the session state n by 0.5 because at every click the button is like is clicked twice
    st.session_state.n += 0.5


def format_language_option(language_code: str):
    return f"{language_code.upper()}  {languages[language_code]}"


def compute_frequencies(words, language):
    results = {}
    try:
        results = get_word_frequencies(words, language)
    except Exception as e:
        st.error(f"Error computing word frequencies: {e}")
    return results


def process_files_input(uploaded_files):
    words_from_file = []
    for uploaded_file in uploaded_files:
        try:
            data = uploaded_file.read().decode("utf-8")
            words_from_file.extend(data.split())
        except Exception as e:
            st.error(f"Error processing file: {e}")
    return words_from_file


def main():
    # Initialize session state
    if "n" not in st.session_state:
        initialize_session_states()

    # App
    st.title("Word frequency counter")
    st.write(
        "This app retrieve the frequencies of words in many languages, based on many sources of data using the [wordfreq](https://pypi.org/project/wordfreq/) python library"
    )

    language = st.selectbox(
        "Language", languages, format_func=lambda x: format_language_option(x)
    )

    text_area_col, upload_txt_col = st.columns([0.6, 0.4])

    with text_area_col:
        words_inserted = st.text_area("Enter text here", height=300)

    with upload_txt_col:
        uploaded_files = st.file_uploader(
            "or Upload txt/csv files", accept_multiple_files=True
        )

    words_from_file = process_files_input(uploaded_files)
    words = words_inserted.split()
    words.extend(words_from_file)

    click = st.button(
        "Compute frequencies",
        on_click=increment_n()
        if len(words) > 0 and st.session_state.words_inserted_before != words
        else None,
    )

    if words:
        st.markdown("---")
        results_title_col, n_col = st.columns([0.12, 0.88])
        with results_title_col:
            st.subheader("Results")
        with n_col:
            st.write(int(st.session_state.n))

        if st.session_state.words_inserted_before != words and click:
            st.session_state.words_inserted_before = words
            st.session_state.results = compute_frequencies(words, language)

        # Display results
        table_col, data_col = st.columns([0.6, 0.4])
        with table_col:
            df = pd.DataFrame(
                st.session_state.results.items(), columns=["Word", "Frequency"]
            )
            df["Frequency"] = pd.to_numeric(df["Frequency"])
            df["Frequency"] = df["Frequency"].apply(
                lambda x: format(x, ".15f").rstrip("0").rstrip(".")
            )
            st.dataframe(
                df,
                width=350,
            )

        with data_col:
            frequency_sum = (
                "{:.15f}".format(sum(df["Frequency"].astype(float).to_list()))
                .rstrip("0")
                .rstrip(".")
            )
            st.write(f"Words: {len(words)}")
            st.write(f"Sum frequencies: {frequency_sum}")

            # Display download button
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download csv",
                csv,
                f"wf_{language}.csv",
                "text/csv",
                key="download-csv",
            )

    elif click:
        st.write("No words to process")


if __name__ == "__main__":
    main()
