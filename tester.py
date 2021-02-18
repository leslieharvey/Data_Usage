from tree_node import TreeNode
from file_nav import FileNav
from template import HTMLTemplate

run_path = "/mnt/c/Coding_Projects/Renne_Lab/Data_Usage/Test_Env"

# get a list of all the files in the root directory
file_nav = FileNav(run_path)
file_list = file_nav.get_files(recurse=True)
owners = {}

# each file is processed into a TreeNode structure
for file in file_list:
    file_size = file_nav.get_file_size(file)
    file_owner = file_nav.get_file_owner(file)

    if file_owner not in owners:
        owners[file_owner] = TreeNode(file_owner)

    owners[file_owner].create_node(run_path, file, file_size)

# -----Print File Structure-----
# for o in owners:
#     print("-----" + o + "-----")
#     owners[o].print_node_data()
#     print("")

# structure owner data into required format
owner_data = {}
for o in owners:
    owner_data[o] = round(owners[o].memory_size, 2)

# create HTML file
html = HTMLTemplate()
html_data = html.create_html(owner_data)

# write HTML file with all aggregated data
with open("result.html", "w") as file:
    file.write(html_data)