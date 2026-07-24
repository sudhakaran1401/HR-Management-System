import pandas as pd

from .column_mapper import COLUMN_MAP


def normalize_column(col):
   
    return (
        str(col)
        .strip()
        .lower()
        .replace("-", "_")
        .replace(" ", "_")
    )


def build_reverse_map():
   
    reverse = {}

    for standard_name, aliases in COLUMN_MAP.items():

        reverse[normalize_column(standard_name)] = standard_name

        for alias in aliases:
            reverse[normalize_column(alias)] = standard_name

    return reverse


def load_excel(filepath, required_columns=None, optional_defaults=None):

    df = pd.read_excel(filepath)

    # Normalize uploaded headers
    df.columns = [normalize_column(c) for c in df.columns]

    reverse_map = build_reverse_map()

    renamed = {}

    for col in df.columns:

        if col in reverse_map:
            renamed[col] = reverse_map[col]

    df.rename(columns=renamed, inplace=True)
    df = df.loc[:, ~df.columns.duplicated()]

    # Ignore unknown columns
    known_columns = set(reverse_map.values())

    df = df[[c for c in df.columns if c in known_columns]]

    # Create optional columns automatically
    if optional_defaults:

        for column, default in optional_defaults.items():

            if column not in df.columns:
                df[column] = default

    # Validate required columns
    if required_columns:

        missing = []

        for column in required_columns:

            if column not in df.columns:
                missing.append(column)

        if missing:
            raise ValueError(
                f"Missing required columns: {', '.join(missing)}"
            )

    return df