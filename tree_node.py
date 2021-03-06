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
            file(IO): file to write the data to
            indent (str): The amount of indent to make the output user friendly
        """
        file.write(indent + self.file_name + " | " + str(self.file_size) + " GB" + "\n")  

class TreeNode:
    """
    This class contains all the information to construct a TreeNode object. A 
    TreeNode object represents a directory of a file system.

    Attributes:    
        owner (str): The name of the owner of the file
        files (dict): The files in the TreeNode object
        directories (dict): The directories in the TreeNode object
    """
    def __init__(self, owner):
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
                self.directories[element] = TreeNode(element)
            
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

    def write_node_data(self, file, indent="", directory="ROOT"):
        """
        This function writes the created file structure in an user friendly format

        Args:
            file (IO): the file to write the node data to
            indent (str): The amount of indent to make the output user friendly
            directory (str): The name of the current directory
        """
        increased_indent = "   " + indent

        file.write(indent + "=> " + directory + " (" + str(self.memory_size) + " GB)" + "\n")
        for d in self.directories:
            self.directories[d].write_node_data(file, increased_indent, d)
      
        for f in self.files:
            self.files[f].write_file_data(file, increased_indent)
        
    
    