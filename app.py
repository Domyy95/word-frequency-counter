import streamlit as st
import pandas as pd
from logic import languages, get_word_frequencies


def format_language_option(language_code):
    return f"{language_code.upper()}  {languages[language_code]}"


st.title("Word frequency counter")
st.write(
    "This app retrieve the frequencies of words in many languages, based on many sources of data using the [wordfreq](https://pypi.org/project/wordfreq/) python library"
)

language = st.selectbox(
    "Language", languages, format_func=lambda x: format_language_option(x)
)

col1, col2 = st.columns([0.6, 0.4])

with col1:
    text = st.text_area("Enter text here", height=300)

with col2:
    uploaded_files = st.file_uploader("or Upload txt files", accept_multiple_files=True)
    words_from_file = []
    for uploaded_file in uploaded_files:
        data = uploaded_file.read().decode("utf-8")
        words_from_file.extend(data.split())

if st.button("Compute frequency"):
    st.subheader("Results")
    words = text.split()
    words.extend(words_from_file)

    if len(words) > 0:
        results = get_word_frequencies(words, language)
        df = pd.DataFrame(results.items(), columns=["Word", "Frequency"])
        st.data_editor(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Press to Download",
            csv,
            f"wf_{language}.csv",
            "text/csv",
            key="download-csv",
        )

    else:
        st.write("No words to process")