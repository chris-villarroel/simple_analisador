import os

def get_filename_without_extension(file_path):
    """
    This function returns the file name without its extension.
    
    :param file_path: str, path to the file
    :return: str, name of the file without extension
    """
    base_name = os.path.basename(file_path)  # Get the file name with extension
    file_name_without_extension, _ = os.path.splitext(base_name)  # Remove the extension
    return file_name_without_extension
