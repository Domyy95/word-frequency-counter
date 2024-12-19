import streamlit as st
from frequency_page import frequency_tab

tab_name = "Tab {n}"


def initialize_session_states():
    st.session_state.n = 0
    st.session_state.words_inserted_before = []
    st.session_state.results = {}
    st.session_state.tabs = 1


def main():
    st.set_page_config(layout="wide")
    if "n" not in st.session_state:
        initialize_session_states()

    st.title("Word frequency counter")
    st.write(
        "This app retrieve the frequencies of words in many languages, based on many sources of data using the [wordfreq](https://pypi.org/project/wordfreq/) python library"
    )

    tabs = st.session_state["tabs"]
    if st.button("Add tab"):
        st.session_state.tabs += 1

    tabs_objs = st.tabs([tab_name.format(n=n) for n in range(1, tabs + 1)])

    for i, tab in enumerate(tabs_objs):
        with tab:
            frequency_tab(i)


if __name__ == "__main__":
    main()
