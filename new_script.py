#!/bin/env python
#-------------------------------------------------------------------------------
# Name:        new_script
# Purpose:     Generate new script based on a template
#
# Author:      allroundcoder
#
# Created:     2018-10-17
# Copyright:   (c) allroundcoder 2018
# Licence:     Mozilla Public License 2.0
#-------------------------------------------------------------------------------
import argparse
import os
import shutil

def select_something(level,folder):
    selection = None
    
    dir_list = sorted([x for x in os.listdir(folder) if os.path.isdir(os.path.join(folder, x))])
    file_list = sorted([x for x in os.listdir(folder) if not os.path.isdir(os.path.join(folder, x))])
    folder_content = dir_list + file_list

    while selection is None:
        # print menu
        print("\n{}".format(folder))
        print("=" * len(folder))

        if level == 0:
            print("[0] Exit")
        else:
            print("[0] < .. >")

        for idx,f in enumerate(folder_content):
            if os.path.isdir(os.path.join(folder, f)):
                print("[{}] < {} >".format(idx + 1,f))
            else:
                print("[{}] {}".format(idx + 1,f))

        # process choice
        choice = raw_input("Please enter number: ")
        if choice.isdigit():
            choice_nr = int(choice) 
            if choice_nr > 0 and choice_nr <= len(folder_content):
               selection = os.path.join(folder,folder_content[choice_nr - 1])
               if os.path.isdir(selection):
                    selection = select_something(level + 1, selection)
            elif choice_nr > len(folder_content):
                print("[{}] out of range!".format(choice_nr)) 
            else:
                # Exit
                break
        else:
            print("[{}] not supported!".format(choice))

    return selection

def main():
    parser = argparse.ArgumentParser(description="Generate new script based on a template")
    parser.add_argument("subdir", nargs='*',help="Start in sub directory (e.g. the script language)")
    parser.add_argument("-o","--output_file", required=True, help="Output file")

    args = parser.parse_args()

    template_dir = os.path.dirname(os.path.realpath(__file__))
    
    for s in args.subdir:
        template_dir = os.path.join(template_dir, s)
    
    if not os.path.exists(template_dir):
        print("ERROR:  template dir {} does not exist!".format(template_dir))
        exit(1)

    src_path = select_something(0, template_dir)

    if src_path is not None:
        shutil.copy(src_path,args.output_file)
        print("Copied {} to {}".format(src_path,args.output_file))

if __name__ == '__main__':
    main()
