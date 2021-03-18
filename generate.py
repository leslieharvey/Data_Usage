from tree_node import TreeNode
from file_nav import FileNav
from template import HTMLTemplate
import sys

def drawProgressBar(percent, barLen = 20):
    # percent float from 0 to 1. 
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(barLen * percent), barLen, percent * 100))
    sys.stdout.flush()

def createOutput(run_path, error_log):
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
        drawProgressBar((i+1)/len(file_list))
    sys.stdout.write("\n")

    # structure owner data into required format
    owner_data = {}
    for o in owners:
        owner_data[o] = round(owners[o].memory_size, 2)
        createOwnerHTML(o, owners[o])

    # sort owner_data in descending order
    sorted_owner_data = {k: v for k, v in sorted(owner_data.items(), key=lambda item: item[1], reverse=True)}

    # create overall HTML file
    html_data = HTMLTemplate.create_html("Member Usage", "Username", "Data Usage (GB)", sorted_owner_data)

    # write HTML file with all aggregated data
    with open("result.html", "w") as f_html:
        f_html.write(html_data)

    return owners

def writeOwnerData(owner_data, file_name="file_tree.txt"):
    with open(file_name, "w") as f_tree:
        for o in owner_data:
            f_tree.write("-----" + o + "-----" + "\n")
            owner_data[o].write_node_data(f_tree)
            f_tree.write("\n")

def createOwnerHTML(name, owner_root):
    owner_largest_directories = owner_root.largest_directories(4)
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