"""
# ============================ LISTING TOOLS ============================ #
"""

# EXPORT
__all__ = [
    "listdirectory"
]

# IMPORT
import dragonfly
import os
import pathlib


def listdirectory(dirpath: str, *,
                  extensions: str | tuple[str] = (""),
                  excluded_folders: str | tuple[str] = ("")) -> list[str]:
    """get the list of the files in a directory and subdirectories
    with possibility to select extensions and exclude some folders

    Args:
        dirpath (str): path of the directory to assess (absolute or relative)
        extensions (str | tuple[str], optional): tuple of the
         selected extension.
            Defaults all with ("").
        excluded_folders (str | tuple[str], optional): tuple of
         folders to exclude.
            Defaults all with ("").

    Returns:
        list[str]: _description_
    """
    # define folder exclusion strategy
    grab_all_folders = False
    if not excluded_folders:
        grab_all_folders = True

    # define extension strategy
    if not extensions:
        grab_all_extensions = True
    else:
        extensions = dragonfly.utils.validation.validateExtensionDefinition(
            extensions)
        grab_all_extensions = False

    # initiate result
    result = set()

    # iterate over files
    for dir_, _, files in os.walk(dirpath):

        if ((not any(substring in dir_
                     for substring in excluded_folders))
           or grab_all_folders):
            for file_name in files:
                if ((pathlib.Path(file_name).suffix in extensions)
                   or grab_all_extensions):
                    rel_dir = os.path.relpath(dir_, dirpath)
                    rel_file = os.path.join(rel_dir, file_name)
                    result.add(rel_file)

    return list(result)
