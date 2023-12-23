import pandas as pd

# kwargs to consider: delimiter=',', quotechar='"', encoding='utf-8', dtype=None, chunksize=None,
# delimiter (str, default ','): Delimiter to use for separating entries.
# quotechar (str, default '"'): Character used to quote fields.
# encoding (str, default 'utf-8'): Encoding of the file.
# dtype (Type name or dict of column -> type, optional): Data type for data or columns.
# chunksize (int, optional): Number of rows per chunk if reading large files.

def load_csv(file_path, header='infer',  **kwargs):
    """Loads data from a CSV file into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file to be loaded.
        header (int, list of int, str, or None, default 'infer'): Row number(s) to use as the column names.
        **kwargs: Additional keyword arguments to pass to pandas.read_csv().

    Returns:
        pd.DataFrame or Iterator[pd.DataFrame]: DataFrame or Iterator of DataFrames if chunksize is given.

    Raises:
        FileNotFoundError: If the file cannot be found.
        ValueError: If there are issues with CSV formatting.
        UnicodeDecodeError: If there's an encoding error in the file.
    """
    try:
        return pd.read_csv(file_path, header=header, **kwargs)
    except FileNotFoundError as fnf_error:
        raise FileNotFoundError(f"File not found: {file_path}") from fnf_error
    except pd.errors.ParserError as parse_error:
        raise ValueError("CSV parsing error - check delimiter and quotechar") from parse_error
    except UnicodeDecodeError as unicode_error:
        raise UnicodeDecodeError(f"Encoding error in file: {file_path}") from unicode_error