import copy
from io import BytesIO

import pandas as pd
from pandas import DataFrame, ExcelWriter

from model import GroupedWords, col_word, col_frequency, col_sums

xlsx_mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
csv_mime = "text/csv"


def _convert_df_to_xlsx(df: DataFrame) -> bytes:
    output = BytesIO()
    df[col_frequency] = df[col_frequency].apply(lambda x: str(x).replace(".", ","))
    df[col_sums] = df[col_sums].apply(lambda x: str(x).replace(".", ","))
    with ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    output.seek(0)
    return output.getvalue()


def _convert_df_to_csv(df: DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def convert_df(df: DataFrame, file_type: str) -> bytes:
    if file_type == "csv":
        return _convert_df_to_csv(df)
    elif file_type == "xlsx":
        return _convert_df_to_xlsx(df)
    else:
        raise ValueError(f"Invalid file type: {file_type}")


def join_same_idx_grouped_words(grouped_words: list[GroupedWords]) -> list[GroupedWords]:
    result = {}
    for group in grouped_words:
        if group.index in result:
            result[group.index].append_list(group)
        else:
            result[group.index] = copy.deepcopy(group)

    return list(result.values())


def get_data_to_download(words_data: list[GroupedWords], file_type: str) -> bytes:
    if not words_data:
        return b""
    words_data_joined = join_same_idx_grouped_words(words_data)
    data = []
    sums = []
    for group in words_data_joined:
        group_data = [(word, freq) for word, freq in group.frequencies.items()]
        df_group = DataFrame(group_data, columns=[col_word, col_frequency])
        df_group[col_frequency] = pd.to_numeric(df_group[col_frequency], errors="coerce")
        # frequency sum row with empty word
        total = df_group[col_frequency].sum()
        sums.append(total)
        total_row = DataFrame([["", total]], columns=[col_word, col_frequency])
        df_group = pd.concat([df_group, total_row], ignore_index=True)
        df_group[col_frequency] = df_group[col_frequency].apply(
            lambda x: format(x, ".15f").rstrip("0").rstrip(".")
        )
        data.append(df_group)

    final_df = pd.concat(data, ignore_index=True)
    # add total sum column
    final_df[col_sums] = ""
    N = len(sums)
    final_df.loc[: N - 1, col_sums] = sums
    return convert_df(final_df, file_type)
