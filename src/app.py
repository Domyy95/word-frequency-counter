import streamlit as st
from frequency_page import frequency_tab
from model import FrequencyPage

tab_name = "Tab {n}"


def initialize_session_states():
    st.session_state.tabs = {1: FrequencyPage(1)}
    st.session_state.tabs_counter = 1


def main():
    with open("src/style.css") as f:
        css_content = f.read()
    st.set_page_config(layout="wide")
    st.markdown(
        f"""
        <style>
               {css_content}
        </style>""",
        unsafe_allow_html=True,
    )
    if "tabs" not in st.session_state:
        initialize_session_states()

    st.title("Word frequency counter")
    st.write(
        "This app retrieve the frequencies of words in many languages, based on many sources of data using the [wordfreq](https://pypi.org/project/wordfreq/) python library"
    )

    tabs = st.session_state["tabs"]
    if st.button("Add tab"):
        st.session_state.tabs_counter += 1
        tabs[st.session_state.tabs_counter] = FrequencyPage(st.session_state.tabs_counter)

    tabs_objs = st.tabs([tab_name.format(n=n) for n in st.session_state.tabs.keys()])

    for tab, tab_n in zip(tabs_objs, st.session_state.tabs.keys()):
        with tab:
            frequency_tab(st.session_state.tabs[tab_n])


if __name__ == "__main__":
    main()
