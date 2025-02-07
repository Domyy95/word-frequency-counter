from io import BytesIO

from docx import Document
from pandas import DataFrame, ExcelWriter
from streamlit import error

xlsx_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
csv_mime = "text/csv"


def convert_df_to_xlsx(df: DataFrame) -> bytes:
    output = BytesIO()
    with ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    output.seek(0)
    return output.getvalue()


def convert_df_to_csv(df: DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def convert_df(df: DataFrame, file_type: str) -> bytes:
    if file_type == "csv":
        return convert_df_to_csv(df)
    elif file_type == "xlsx":
        return convert_df_to_xlsx(df)
    else:
        raise ValueError(f"Invalid file type: {file_type}")


def split_input(text: str) -> list[str]:
    new_line = text.split("\n")
    comma = [word.strip() for line in new_line for word in line.split(",")]
    semicolon = [word.strip() for word in comma for word in word.split(";")]
    dot = [word.strip() for word in semicolon for word in word.split(".")]
    return dot


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
