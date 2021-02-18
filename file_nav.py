from os import walk
from os import stat
import os
from pwd import getpwuid

# Based on:
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

class FileNav:
    """
    This class contains all the information needed to navigate a file system to 
    retrieve needed information.

    Attributes:    
        current_path (dict): The current path of the FileNav class.
    """
    def __init__(self, path):
        self.current_path = path

    def get_files(self, recurse=False):
        """
        This function returns a list of the files in the specified path.

        Args:
            path (str): The path to retrieve the information of.
            recurse (bool): Boolean on whether the function should be recursive or not.

        Returns:
            list: A list of the files in the specified path.
        """
        files = []
        for (dirpath, _, filenames) in walk(self.current_path):
            filenames_with_path = [os.path.join(dirpath, name) for name in filenames]
            files.extend(filenames_with_path)
            if not recurse:
                break
        return files

    def get_directories(self, path, recurse=False):
        """
        This function returns a list of the directories in the specified path.

        Args:
            path (str): The path to retrieve the information of.
            recurse (bool): Boolean on whether the function should be recursive or not.

        Returns:
            list: A list of the directories in the specified path.
        """
        directories = []
        for (_, dirnames, _) in walk(path):
            directories.extend(dirnames)
            if not recurse:
                break
        return directories

    def get_file_owner(self, filename):
        """
        This function returns the owner of a file.

        Args:
            filename (str): The path of the file to retrieve the information of.

        Returns:
            str: The owner of the specified file.
        """
        return getpwuid(stat(filename).st_uid).pw_name

    def get_file_size(self, filename):
        """
        This function returns the memory used by a file, in bytes.

        Args:
            filename (str): The path of the file to retrieve the information of.

        Returns:
            int: Memory used, in GB, by file.
        """
        return float(stat(filename).st_size / float(pow(10, 9)))