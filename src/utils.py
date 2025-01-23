from pandas import DataFrame, ExcelWriter
from io import BytesIO
from docx import Document
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


def process_files_input(uploaded_files: list) -> list:
    words_from_file = []
    for uploaded_file in uploaded_files:
        try:
            file_extension = uploaded_file.name.split(".")[-1].lower()

            if file_extension in ["txt", "csv"]:
                data = uploaded_file.read().decode("utf-8")
                words_from_file.extend(data.split())

            elif file_extension == "docx":
                doc = Document(BytesIO(uploaded_file.read()))
                for para in doc.paragraphs:
                    words_from_file.extend(para.text.split())

            else:
                error(f"Unsupported file format: {uploaded_file.name}")

        except Exception as e:
            error(f"Error processing file {uploaded_file.name}: {e}")

    return words_from_file
