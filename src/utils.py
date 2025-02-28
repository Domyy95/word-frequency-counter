from io import BytesIO

from docx import Document
from streamlit import error


def split_input(text: str) -> list[str]:
    new_line = text.split("\n")
    comma = [word.strip() for line in new_line for word in line.split(",")]
    semicolon = [word.strip() for word in comma for word in word.split(";")]
    result = [word.strip() for word in semicolon for word in word.split(".")]
    return result


def process_files_input(uploaded_files: list[str]) -> list[str]:
    result = ""
    for uploaded_file in uploaded_files:
        try:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension in ["txt", "csv"]:
                data = uploaded_file.read().decode("utf-8")
                result += data

            elif file_extension == "docx":
                doc = Document(BytesIO(uploaded_file.read()))
                for para in doc.paragraphs:
                    result += para.text + "\n"

            else:
                error(f"Unsupported file format: {uploaded_file.name}")

        except Exception as e:
            error(f"Error processing file {uploaded_file.name}: {e}")

    return result
