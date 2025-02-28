import io
import zipfile

import streamlit as st

from frequency_page import frequency_tab
from model import FrequencyPageManager
from output import csv_mime, get_data_to_download, xlsx_mime
from wordfreq_logic import languages

tab_name = "Tab {n}"


def initialize_session_states():
    st.session_state.tabs = {1: FrequencyPageManager(1)}
    st.session_state.tabs_counter = 1


def add_tab():
    st.session_state.tabs_counter += 1
    st.session_state["tabs"][st.session_state.tabs_counter] = FrequencyPageManager(
        st.session_state.tabs_counter
    )


def prepare_download_all():
    tabs = st.session_state.tabs
    to_download = {}
    for tab_obj in tabs.values():
        if len(tab_obj.words) > 0:
            if tab_obj.language not in to_download:
                to_download[tab_obj.language] = []
            to_download[tab_obj.language].extend(tab_obj.words)

    st.session_state.data_to_download = to_download


def prepare_zip(file_type: str) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for language, grouped_words_lists in st.session_state.data_to_download.items():
            zf.writestr(
                f"wf_{language}.{file_type}", get_data_to_download(grouped_words_lists, file_type)
            )

    zip_buffer.seek(0)
    return zip_buffer


def main():
    st.set_page_config(layout="wide")

    with open("src/style.css") as f:
        css_content = f.read()
    st.markdown(
        f"""
        <style>
               {css_content}
        </style>""",
        unsafe_allow_html=True,
    )

    if "tabs" not in st.session_state:
        initialize_session_states()

    # Page
    st.title("Word frequency counter")
    st.write(
        """This app retrieves word frequencies across multiple languages using various data sources,
        powered by the [wordfreq](https://pypi.org/project/wordfreq/) Python library.
        """
    )
    features_col, _ = st.columns([0.7, 0.3])
    with features_col.expander("**Main features** 🚀"):
        st.write(
            f"""
                - **Multiple languages** supported: {" ".join(list(languages.values()))}
                - **Upload files** in TXT, CSV, or DOCX formats for processing.
                - **Add multiple tabs** to analyze different datasets simultaneously.
                - **Download results** from individual tabs or aggregate them in CSV or XLSX format.
                - **Download all results** as a ZIP file, with aggregated data organized by language.
                - **Process numbered list inputs** summing word frequencies within each list entry.
                For example, the input `1) a,b,c 2) d,e,f` will generate individual word frequencies, as well as summed frequencies for the groups 'a, b, c' and 'd, e, f'.

        """
        )
    add_tab_col, prepare_download, file_type_col, _ = st.columns([0.08, 0.12, 0.1, 0.7])
    add_tab_col.button("Add tab", on_click=add_tab)

    prepare_download.button("Aggregate Data", on_click=prepare_download_all)

    file_type = file_type_col.selectbox(
        label="File type",
        label_visibility="collapsed",
        options=["xlsx", "csv"],
    )

    if "data_to_download" in st.session_state and len(st.session_state.data_to_download) > 0:
        st.markdown("---")
        st.subheader("Aggregated data")

        cols = st.columns(len(st.session_state.data_to_download))
        for idx, (language, grouped_words_lists) in enumerate(
            st.session_state.data_to_download.items()
        ):
            frequency_sum = sum(
                [
                    sum([float(freq) for _, freq in group.frequencies.items()])
                    for group in grouped_words_lists
                ]
            )
            words = sum([len(group.frequencies) for group in grouped_words_lists])

            with cols[idx]:
                st.write(f"**Language**: {language.upper()}")
                st.write(f"Words: {words}")
                st.write(f"Sum frequencies: {frequency_sum}")

        if len(st.session_state.data_to_download) > 1:
            zip_buffer = prepare_zip(file_type)
            data = zip_buffer
            file_name = "wf.zip"
            mime = "application/zip"

        else:
            language, grouped_words_list = list(st.session_state.data_to_download.items())[0]
            data = get_data_to_download(grouped_words_list, file_type)
            file_name = f"wf_{language}.{file_type}"
            mime = csv_mime if file_type == "csv" else xlsx_mime

        st.download_button(
            label="Download",
            data=data,
            file_name=file_name,
            mime=mime,
        )

    elif "data_to_download" in st.session_state and len(st.session_state.data_to_download) == 0:
        st.write("No data computed to download")

    tabs_objs = st.tabs([tab_name.format(n=n) for n in st.session_state.tabs.keys()])

    for tab, tab_n in zip(tabs_objs, st.session_state.tabs.keys()):
        with tab:
            frequency_tab(st.session_state.tabs[tab_n])


if __name__ == "__main__":
    main()
