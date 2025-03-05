import streamlit as st

from model import FrequencyPageManager, col_frequency
from output import csv_mime, get_data_to_download, xlsx_mime
from wordfreq_logic import languages


def format_language_option(language_code: str) -> str:
    return f"{language_code.upper()}  {languages[language_code]}"


def remove_tab(id: int):
    if len(st.session_state.tabs) > 1:
        st.session_state.tabs.pop(id)


def frequency_tab(data: FrequencyPageManager):
    language_selector_col, compute_freq_button_col, remove_tab_col = st.columns([0.15, 0.82, 0.04])

    language = language_selector_col.selectbox(
        key=f"language_{data.id}",
        label="Language",
        label_visibility="collapsed",
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
        label="or Upload txt/csv/docx files",
        accept_multiple_files=True,
    )

    something_inserted = words_inserted != "" or len(uploaded_files) > 0
    click = compute_freq_button_col.button(key=f"compute_{data.id}", label="Compute frequencies")

    # if something_inserted and click:
    if something_inserted:
        st.markdown("---")
        results_title_col, n_col, _ = st.columns([0.09, 0.1, 0.81])
        results_title_col.subheader("Results")

        if click:
            data.compute_frequencies(words_inserted, uploaded_files, language)

        n_col.write(int(data.n))

        # Results
        table_col, data_col = st.columns([0.6, 0.4])
        with table_col:
            df = data.to_df()
            st.dataframe(
                data=df,
                width=350,
            )

        with data_col:
            frequency_sum = (
                "{:.15f}".format(sum(df[col_frequency].astype(float).to_list()))
                .rstrip("0")
                .rstrip(".")
            )
            st.write(f"**Words**: {data.total_words()}")
            st.write(f"**Sum frequencies**: {frequency_sum}")

            st.download_button(
                key=f"download_{data.id}_csv",
                label="Download csv",
                data=get_data_to_download(data.words, "csv"),
                file_name=f"wf_{language}.csv",
                mime=csv_mime,
            )

            st.download_button(
                key=f"download_{data.id}_xlsx",
                label="Download xlsx",
                data=get_data_to_download(data.words, "xlsx"),
                file_name=f"wf_{language}.xlsx",
                mime=xlsx_mime,
            )

    elif click:
        st.write("No words to process")
