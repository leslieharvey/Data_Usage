#!/usr/bin/env python3
# Leslie O. Harvey III
# Changelog:
#   2020-02-18 : v01, Initial Version
"""This script produces an HTML output of the current data usage"""

import argparse
import os
import sys
from tree_node import TreeNode
from file_nav import FileNav
from template import HTMLTemplate

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    sys.path.append(os.path.join('..', os.path.dirname(__file__)))

def main_function(**kwargs):
    """
    Runs the Data Usage specification
    """
    required_args = ['path']
    _check_req_args(required_args, kwargs, 'data_usage')

    run_path = kwargs['path']

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

    if kwargs['write']:
        # -----Write File Structure-----
        with open("file_tree.txt", "w") as file:
            for o in owners:
                file.write("-----" + o + "-----" + "\n")
                owners[o].write_node_data(file)
                file.write("\n")

def _dir_exists(dir_name, dir_type=''):
    """
    This function checks to see if the entered directory exists
    """
    if '~' in dir_name:
        dir_name = os.path.expanduser(dir_name)
    dir_name = os.path.abspath(dir_name)
    if not os.path.isdir(dir_name):
        message = ('Provided %s Directory: %s Does not exist.\n' % (dir_type.title(), dir_name)
                   + 'Exiting...\n')
        raise argparse.ArgumentTypeError(message)
    return dir_name

def _check_req_args(req_args, kwargs, fn_name):
    for req_arg in req_args:
        if req_arg not in kwargs:
            message = 'Missing required argument: %s ' % req_arg
            message += ' to function %s.' % fn_name
            print(message)
            raise Exception(message)

def parse_args(print_help=False):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='store_true',
                        help='Output program version information and exit.')
    
    in_opts = parser.add_argument_group('Input Options')
    in_opts.add_argument('-p', '--path', default=DEFAULT_PATH, type=_dir_exists,
                         help='The specified path to run the analyis on')

    out_opts = parser.add_argument_group('Output Options')
    out_opts.add_argument('-w', '--write', action='store_true',
                          help=('Write the file tree structure to text file'))

    if print_help:
        parser.print_help()
        return {}

    namespace = parser.parse_args()
    args_info = vars(namespace)
    return args_info

if __name__ == '__main__':
    args_info = parse_args()
    if not args_info:
        sys.exit()
    main_function(**args_info)

