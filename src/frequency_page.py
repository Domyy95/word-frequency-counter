import streamlit as st
import pandas as pd
from model import FrequencyPageManager
from wordfreq_logic import languages


def format_language_option(language_code: str):
    return f"{language_code.upper()}  {languages[language_code]}"


def process_files_input(uploaded_files):
    words_from_file = []
    for uploaded_file in uploaded_files:
        try:
            data = uploaded_file.read().decode("utf-8")
            words_from_file.extend(data.split())
        except Exception as e:
            st.error(f"Error processing file: {e}")
    return words_from_file


def remove_tab(id):
    if len(st.session_state.tabs) > 1:
        st.session_state.tabs.pop(id)


def frequency_tab(data: FrequencyPageManager):
    language_col, _, remove_tab_col = st.columns([0.15, 0.82, 0.04])

    language = language_col.selectbox(
        key=f"language_{data.id}",
        label="Language",
        options=languages,
        format_func=lambda x: format_language_option(x),
    )

    remove_tab_col.button(
        key=f"remove_{data.id}",
        label="X",
        on_click=lambda: remove_tab(data.id),
        type="primary",
    )

    text_area_col, upload_txt_col = st.columns([0.6, 0.4])
    words_inserted = text_area_col.text_area(
        key=f"words_{data.id}", label="Enter text here", height=300
    )

    uploaded_files = upload_txt_col.file_uploader(
        key=f"upload_{data.id}",
        label="or Upload txt/csv files",
        accept_multiple_files=True,
    )

    words_from_file = process_files_input(uploaded_files)
    words = words_inserted.split()
    words.extend(words_from_file)
    words = list(dict.fromkeys(words))  # Remove double strings keeping the order of the list

    click = st.button(
        key=f"compute_{data.id}",
        label="Compute frequencies",
        on_click=data.increment_n()
        if len(words) > 0 and data.words_inserted_before != words
        else None,
    )

    if words:
        st.markdown("---")
        results_title_col, n_col, _ = st.columns([0.09, 0.1, 0.81])
        results_title_col.subheader("Results")
        n_col.write(int(data.n))

        if data.words_inserted_before != words and click:
            data.compute_frequencies(words, language)

        # Results
        table_col, data_col = st.columns([0.6, 0.4])
        with table_col:
            df = pd.DataFrame(data.results.items(), columns=["Word", "Frequency"])
            df["Frequency"] = pd.to_numeric(df["Frequency"])
            df["Frequency"] = df["Frequency"].apply(
                lambda x: format(x, ".15f").rstrip("0").rstrip(".")
            )
            st.dataframe(
                data=df,
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

            # Download button
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                key=f"download_{data.id}",
                label="Download csv",
                data=csv,
                file_name=f"wf_{language}.csv",
                mime="text/csv",
            )

    elif click:
        st.write("No words to process")
