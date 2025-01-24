import streamlit as st
from model import FrequencyPageManager
from wordfreq_logic import languages
from utils import (
    convert_df_to_csv,
    convert_df_to_xlsx,
    xlsx_mime,
    csv_mime,
    process_files_input,
    split_input,
)


def format_language_option(language_code: str) -> str:
    return f"{language_code.upper()}  {languages[language_code]}"


def remove_tab(id: int):
    if len(st.session_state.tabs) > 1:
        st.session_state.tabs.pop(id)


def frequency_tab(data: FrequencyPageManager):
    language_col, compute_freq_col, remove_tab_col = st.columns([0.15, 0.82, 0.04])

    language = language_col.selectbox(
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

    words_from_file = process_files_input(uploaded_files)
    words = split_input(words_inserted)
    words.extend(words_from_file)

    with compute_freq_col:
        click = st.button(
            key=f"compute_{data.id}",
            label="Compute frequencies",
            on_click=data.increment_n()
            if len(words) > 0 and data.input_is_changed(words=words)
            else None,
        )

    if words:
        st.markdown("---")
        results_title_col, n_col, _ = st.columns([0.09, 0.1, 0.81])
        results_title_col.subheader("Results")
        n_col.write(int(data.n))

        if data.input_is_changed(words=words) and click:
            data.compute_frequencies(language)

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
                "{:.15f}".format(sum(df["Frequency"].astype(float).to_list()))
                .rstrip("0")
                .rstrip(".")
            )
            st.write(f"**Words**: {len(data.words)}")
            st.write(f"**Sum frequencies**: {frequency_sum}")

            st.download_button(
                key=f"download_{data.id}_csv",
                label="Download csv",
                data=convert_df_to_csv(df),
                file_name=f"wf_{language}.csv",
                mime=csv_mime,
            )

            st.download_button(
                key=f"download_{data.id}_xlsx",
                label="Download xlsx",
                data=convert_df_to_xlsx(df),
                file_name=f"wf_{language}.xlsx",
                mime=xlsx_mime,
            )

    elif click:
        st.write("No words to process")
