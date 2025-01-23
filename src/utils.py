from pandas import DataFrame, ExcelWriter
from io import BytesIO

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
