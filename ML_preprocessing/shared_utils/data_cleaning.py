import pandas as pd

def clean_data(df, remove_duplicate_rows=False, ):
    # Remove duplicate rows
    if remove_duplicate_rows:
        df.drop_duplicates()


    df_cleaned = remove_duplicates(df)
    df_filled = fill_missing_values(df_cleaned, strategy='median')
    df_corrected = correct_data_types(df_filled, {'col1': 'float'})
    return df_corrected


def fill_missing_values(df, fill_value=None, strategy='mean', columns=None):
    """Fills missing values in a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame in which to fill missing values.
        fill_value (optional): Value to use for filling missing values.
        strategy (str, optional): Strategy to use for imputation ('mean', 'median', 'mode').
        columns (list of str, optional): Columns to apply imputation. If None, apply to all.

    Returns:
        pd.DataFrame: DataFrame with missing values filled.
    """
    if columns:
        target_columns = columns
    else:
        target_columns = df.columns

    for column in target_columns:
        if strategy == 'mean':
            fill_value = df[column].mean()
        elif strategy == 'median':
            fill_value = df[column].median()
        elif strategy == 'mode':
            fill_value = df[column].mode()[0]
        df[column] = df[column].fillna(fill_value)

    return df

# Example usage
if __name__ == "__main__":
    # Example DataFrame
    data = {'col1': [1, 2, None, 4], 'col2': ['a', 'b', 'c', None]}
    df = pd.DataFrame(data)

    # Remove duplicates
    df_cleaned = remove_duplicates(df)

    # Fill missing values
    df_filled = fill_missing_values(df_cleaned, strategy='median')

    print(df_corrected)
