# Word Frequency Counter App

This Streamlit app allows users to retrieve the frequencies of words in various languages based on multiple sources of data using the [wordfreq](https://pypi.org/project/wordfreq/) Python library.

The app is also available on [link](https://word-frequency-counter.streamlit.app/)

## Getting Started

### Prerequisites
- Python 3.8 or higher

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your_username/your_repository.git
   ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Usage
1. Run the app:
    ```sh
    streamlit run app.py
    ```

2. Select the language for word frequency analysis from the dropdown menu.

3. Enter text in the provided text area or upload text files for analysis.

4. Click the "Compute frequency" button to generate word frequency results.

5. View the results in a table and download the results as a CSV file using the "Press to Download" button.

### Built With
- [Streamlit](https://docs.streamlit.io/) - The web framework used
- [Pandas](https://pandas.pydata.org/) - Data manipulation and analysis library for Python
- [wordfreq](https://pypi.org/project/wordfreq/) - Python library for looking up the frequency of words in various languages

### Authors
- Dominic Crippa @Domyy95
