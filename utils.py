import os 

def ensure_directory_exists(path):
    """
    Creates a directory if it does not exist.

    Args:
        path (str): Path to the directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)