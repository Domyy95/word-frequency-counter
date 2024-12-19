import streamlit as st
import pandas as pd
from src.logic import languages, get_word_frequencies


def compute_frequencies(words, language):
    results = {}
    try:
        results = get_word_frequencies(words, language)
        results = {key.capitalize(): f for key, f in results.items()}
    except Exception as e:
        st.error(f"Error computing word frequencies: {e}")
    return results


def increment_n():
    # Increment the session state n by 0.5 because at every click the button is like is clicked twice
    st.session_state.n += 0.5


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


def frequency_tab(tab_n: int):
    language = st.selectbox(
        key=f"language_{tab_n}",
        label="Language",
        options=languages,
        format_func=lambda x: format_language_option(x),
    )

    text_area_col, upload_txt_col = st.columns([0.6, 0.4])

    with text_area_col:
        words_inserted = st.text_area(
            key=f"words_{tab_n}", label="Enter text here", height=300
        )

    with upload_txt_col:
        uploaded_files = st.file_uploader(
            key=f"upload_{tab_n}",
            label="or Upload txt/csv files",
            accept_multiple_files=True,
        )

    words_from_file = process_files_input(uploaded_files)
    words = words_inserted.split()
    words.extend(words_from_file)
    words = list(
        dict.fromkeys(words)
    )  # remove double strings keeping the order of the list

    click = st.button(
        key=f"compute_{tab_n}",
        label="Compute frequencies",
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

            # Display download button
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                key=f"download_{tab_n}",
                label="Download csv",
                data=csv,
                file_name=f"wf_{language}.csv",
                mime="text/csv",
            )

    elif click:
        st.write("No words to process")
