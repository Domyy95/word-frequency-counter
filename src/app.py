import io
import zipfile
import copy
import pandas as pd
import streamlit as st
from frequency_page import frequency_tab
from model import FrequencyPageManager

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
    for tab in tabs.values():
        if tab.results:
            if tab.language in to_download:
                to_download[tab.language].update(tab.results)
            else:
                to_download[tab.language] = copy.deepcopy(tab.results)

    st.session_state.data = to_download


def prepare_zip() -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for language, results in st.session_state.data.items():
            df = pd.DataFrame(results.items(), columns=["Word", "Frequency"])
            zf.writestr(f"wf_{language}.csv", df.to_csv(index=False).encode("utf-8"))

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
        "This app retrieves the frequencies of words in many languages, based on many sources of data using the [wordfreq](https://pypi.org/project/wordfreq/) python library"
    )
    add_tab_col, prepare_download, download_all_col = st.columns([0.08, 0.12, 0.8])
    add_tab_col.button("Add tab", on_click=add_tab)

    prepare_download.button("Aggregate Data", on_click=prepare_download_all)

    with download_all_col:
        if "data" in st.session_state:
            if len(st.session_state.data) > 1:
                zip_buffer = prepare_zip()
                st.download_button(
                    label="Download",
                    data=zip_buffer,
                    file_name="wf.zip",
                    mime="application/zip",
                )

            else:
                language, results = list(st.session_state.data.items())[0]
                df = pd.DataFrame(results.items(), columns=["Word", "Frequency"])
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download",
                    data=csv,
                    file_name=f"wf_{language}.csv",
                    mime="text/csv",
                )

    tabs_objs = st.tabs([tab_name.format(n=n) for n in st.session_state.tabs.keys()])

    for tab, tab_n in zip(tabs_objs, st.session_state.tabs.keys()):
        with tab:
            frequency_tab(st.session_state.tabs[tab_n])


if __name__ == "__main__":
    main()
