from tree_node import TreeNode
from file_nav import FileNav
from template import HTMLTemplate
import sys

def drawProgressBar(percent, barLen = 20):
    # percent float from 0 to 1. 
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(barLen * percent), barLen, percent * 100))
    sys.stdout.flush()

# run_path = "/mnt/c/Coding_Projects/Renne_Lab/Data_Usage/TEST"

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

    # create HTML file
    html = HTMLTemplate()
    html_data = html.create_html(owner_data)

    # write HTML file with all aggregated data
    with open("result.html", "w") as f_html:
        f_html.write(html_data)

    return owners

# -----Print File Structure-----
# for o in owners:
#     print("-----" + o + "-----")
#     owners[o].print_node_data()
#     print("")