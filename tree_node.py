from file_nav import FileNav

class File:
    """
    This class contains all the information to construct a file object.

    Attributes:    
        owner (str): The name of the owner of the file
        file_name (str): The name of the file that the object referes to
        file_size (float): The size of the file in gigabytes
    """
    def __init__(self, owner, file_name, file_size):
        self.owner = owner
        self.file_name = file_name
        self.file_size = file_size  

    def print_file_data(self, indent):
        """
        This prints out the file information in a user friendly format.

        Args:
            indent (str): The amount of indent to make the output user friendly
        """
        print(indent + self.file_name + " | " + str(self.file_size) + " GB")  
    
    def write_file_data(self, file, indent):
        """
        This writes out the file information in a user friendly format.

        Args:
            file (IO): file to write the data to
            indent (str): The amount of indent to make the output user friendly
        """
        file.write(indent + self.file_name + " | " + str(self.file_size) + " GB" + "\n")  

class TreeNode:
    """
    This class contains all the information to construct a TreeNode object. A 
    TreeNode object represents a directory of a file system.

    Attributes: 
        level_name (str): The name of the level
        path (str): The path taken to get to the level   
        owner (str): The name of the owner of the file
        files (dict): The files in the TreeNode object
        directories (dict): The directories in the TreeNode object
        memory_size (float): The amount of memory the level consumes
    """
    def __init__(self, owner, level_name = "ROOT", from_path = ""):
        self.level_name = level_name
        self.path = from_path + level_name + "/"
        self.owner = owner
        self.files = {}
        self.directories = {}
        self.memory_size = 0.0

    def __insert_file(self, owner, file_name, file_size):
        """
        This function inserts a file into the current TreeNode object

        Args:
            owner (str): The name of the owner of the file
            file_name (str): The name of the file to insert
            file_size (str): The size (GB) of the file to insert
        """
        self.files[file_name] = File(owner, file_name, file_size)

    def create_node(self, root_path, file_path, file_size):
        """
        This function creates a node to represent the specified file

        Args:
            root_path (str): The root path of the inital search
            file_path (str): The path of the file to retrieve the information of
            file_size (str): The size (GB) of the file to insert
        """
        if root_path[:-1] != "/":
            root_path += "/"

        # remove the root path from the child_path
        child_path = file_path.replace(root_path, '')
        self.memory_size += file_size

        # insert needed directory nodes, recursion stops once the file can be inserted
        try:
            # If successful, then element is a directory
            element = child_path[:child_path.index("/")]
            if element not in self.directories:
                self.directories[element] = TreeNode(self.owner, element, self.path)
            
            directory_node = self.directories[element]
            directory_node.create_node(root_path + str(element), file_path, file_size)
                
        except(ValueError):
            # error: element is a file
            element = child_path
            file_size = FileNav(root_path).get_file_size(file_path)

            self.__insert_file(self.owner, element, file_size)

    def print_node_data(self, indent="", directory="ROOT"):
        """
        This function prints the created file structure in an user friendly format

        Args:
            indent (str): The amount of indent to make the output user friendly
            directory (str): The name of the current directory
        """
        increased_indent = "   " + indent

        print(indent + "=> " + directory + " (" + str(self.memory_size) + " GB)")
        for d in self.directories:
            self.directories[d].print_node_data(increased_indent, d)
      
        for f in self.files:
            self.files[f].print_file_data(increased_indent)

    def write_node_data(self, file, indent="", directory="ROOT", depth_limit=-1, current_level=0):
        """
        This function writes the created file structure in an user friendly format

        Args:
            file (IO): the file to write the node data to
            indent (str): The amount of indent to make the output user friendly
            directory (str): The name of the current directory
            depth_limit (int): The depth limit of directories to write
            current_level (int): The current level of directories traversed
        """
        if current_level > depth_limit and depth_limit != -1:
            return

        increased_indent = "   " + indent

        file.write(indent + "=> " + directory + " (" + str(self.memory_size) + " GB)" + "\n")
        for d in self.directories:
            self.directories[d].write_node_data(file, increased_indent, d, current_level=current_level + 1, depth_limit=depth_limit)
      
        for f in self.files:
            self.files[f].write_file_data(file, increased_indent)

    def __get_files_including_sub_directories(self, return_files = []):
        """
        This function is a recursive call to begin at a directory and collect all the
        files at that level, including ones in sub-directories

        Args:
            return_files (list): The list where files will be added to
        
        Returns:
            list: A list of File objects representing the files
        """
        return_files += self.files.values()
        for d in self.directories:
            self.directories[d].__get_files_including_sub_directories(return_files)

        return return_files

    def __get_directories_including_sub_directories(self, return_directories = []):
        """
        This function is a recursive call to begin at a directory and collect all the
        directories at that level, including ones in sub-directories

        Args:
            return_directories (list): The list where directories will be added to
        
        Returns:
            list: A list of TreeNode objects representing the directories
        """
        return_directories += self.directories.values()
        for d in self.directories:
            self.directories[d].__get_directories_including_sub_directories(return_directories)

        return return_directories

    def largest_files(self, amount_limit = -1):
        """
        This function will return the largest files relative to the TreeNode position
        the function is called on. The return will include files at the current level.
        The returned list will be ordered in a decresing format.

        Args:
            amount_limit (list): The limit of largest files to return. If no value 
                specified, all files are returned
        
        Returns:
            list: A list of TreeNode objects representing the largest files
        """

        all_files = self.__get_files_including_sub_directories()
        sorted_files = sorted(all_files, key=lambda item: item.file_size, reverse=True)
        
        return sorted_files if amount_limit == -1 else sorted_files[:amount_limit]

    def largest_directories(self, amount_limit = -1):
        """
        This function will return the largest directories relative to the TreeNode position
        the function is called on. The return will not include the TreeNode (directory) it
        is called on. The returned list will be ordered in a decresing format.

        Args:
            amount_limit (list): The limit of largest directories to return. If no value 
                specified, all directories are returned
        
        Returns:
            list: A list of TreeNode objects representing the largest directories
        """

        all_directories = self.__get_directories_including_sub_directories()
        sorted_directories = sorted(all_directories, key=lambda item: item.memory_size, reverse=True)
        
        return sorted_directories if amount_limit == -1 else sorted_directories[:amount_limit]
        
    
    