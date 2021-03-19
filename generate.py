from tree_node import TreeNode
from file_nav import FileNav
from template import HTMLTemplate
import sys

def __drawProgressBar(percent, bar_length = 20):
    """
    This function will draw a progress status bar

    Args:
        percent (float): The percent of the operation completed.
        bar_length (int): The length of the desired progress bar.
    """
    # percent float from 0 to 1. 
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(bar_length * percent), bar_length, percent * 100))
    sys.stdout.flush()

def createOutput(run_path, error_log, depth_limit=-1):
    """
    This function creates the output of the overall script

    Args:
        run_path (str): The complete path of the target directory.
        error_log (IO): The IO file to write errors to.
        depth_limit (int): The depth limit to write for the outputs
    """

    # get a list of all the files in the root directory
    file_nav = FileNav(run_path)
    file_list = file_nav.get_files(recurse=True)
    owners = {}

    # each file is processed into a TreeNode structure
    for i, file_path in enumerate(file_list):
        try:
            file_size = file_nav.get_file_size(file_path)
            file_owner = file_nav.get_file_owner(file_path)
        except(OSError):
            error_log.write("Could not open: " + file_path + "\n")
            continue
        except(KeyError):
            error_log.write("Key Error for: " + file_path+ "\n")
            continue
        
        if file_owner not in owners:
            owners[file_owner] = TreeNode(file_owner)

        owners[file_owner].create_node(run_path, file_path, file_size)
        __drawProgressBar((i+1)/len(file_list))
    sys.stdout.write("\n")

    # structure owner data into required format
    owner_data = {}
    for o in owners:
        owner_data[o] = round(owners[o].memory_size, 2)
        createOwnerHTML(o, owners[o], depth_limit)

    # sort owner_data in descending order
    sorted_owner_data = {k: v for k, v in sorted(owner_data.items(), key=lambda item: item[1], reverse=True)}

    # create overall HTML file
    html_data = HTMLTemplate.create_html("Member Usage", "Username", "Data Usage (GB)", sorted_owner_data)

    # write HTML file with all aggregated data
    with open("result.html", "w") as f_html:
        f_html.write(html_data)

    return owners

def writeOwnerFileTree(owner_data, file_name="file_tree.txt", depth_limit=-1):
    """
    This function writes the file tree structure for all the owners identified.

    Args:
        owner_data (dict): A dictionary containing the data label and value of a row
            The input object has the form::
                    {
                        'data_row': 0.00,
                        'data_row2': 0.00,
                        ...
                    }
        file_name (str): The name for the output file.
        depth_limit (int): The depth limit to write for the outputs.
    """

    with open(file_name, "w") as f_tree:
        for o in owner_data:
            f_tree.write("-----" + o + "-----" + "\n")
            owner_data[o].write_node_data(f_tree, depth_limit=depth_limit)
            f_tree.write("\n")

def createOwnerHTML(name, owner_root, depth_limit=-1):
    """
    This function creates an HTML output for each owner

    Args:
        owner_root (TreeNode): The TreeNode root object for the specified owner
        depth_limit (int): The depth limit to write for the outputs
    """
    # retrieve the 4 largest directories
    owner_largest_directories = owner_root.largest_directories(depth_limit)
    owner_data = {}
    for directory in owner_largest_directories : owner_data[directory.path] = directory.memory_size
    
    # create overall HTML file
    html_data = HTMLTemplate.create_html("Largest Directories - " + name, "Directory Path", "Data Usage (GB)", owner_data)

    # write HTML file with all aggregated data
    with open(name + "_result.html", "w") as f_html:
        f_html.write(html_data)

# -----Print File Structure-----
# for o in owners:
#     print("-----" + o + "-----")
#     owners[o].print_node_data()
#     print("")