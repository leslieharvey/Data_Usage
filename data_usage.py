#!/usr/bin/env python3
# Leslie O. Harvey III
# Changelog:
#   2021-09-28 : v01, Initial Version
"""This script produces an HTML output of the current data usage"""

import argparse
import os
import sys
from tree_node import TreeNode
from file_nav import FileNav
from template import HTMLTemplate
from generate import createOutput, writeOwnerFileTree
from email_config import emailSender

DEFAULT_PATH = os.path.dirname(os.path.abspath(__file__))
# Depth of 0 indicates the directories at the root level are computed
DEFAULT_DEPTH = 1
DEFAULT_LIMIT = 20

if __name__ == '__main__':
    sys.path.append(os.path.join('..', os.path.dirname(__file__)))


def main_function(f, **kwargs):
    """
    Runs the Data Usage specification
    """
    required_args = ['path', 'depth', 'limit']
    _check_req_args(required_args, kwargs, 'data_usage')

    run_path = kwargs['path']

    owner_data = createOutput(
        run_path, f, depth_limit=kwargs['depth'], length_limit=kwargs['limit'])

    if kwargs['write']:
        # -----Write File Structure-----
        writeOwnerFileTree(owner_data, depth_limit=kwargs['depth'])

    if kwargs['email']:
        # ---------Send Emails----------
        emailSender()


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
    in_opts.add_argument('-d', '--depth', default=DEFAULT_DEPTH, type=int,
                         help='The depth of directories to write in outputs')
    in_opts.add_argument('-l', '--limit', default=DEFAULT_LIMIT, type=int,
                         help='The limit of the amount of directories to return in user output')

    out_opts = parser.add_argument_group('Output Options')
    out_opts.add_argument('-w', '--write', action='store_true',
                          help=('Write the file tree structure to text file'))
    out_opts.add_argument('-e', '--email', action='store_true',
                          help=('Send results via email to specified users'))

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
    with open("error_log.txt", "w") as f:
        main_function(f, **args_info)
