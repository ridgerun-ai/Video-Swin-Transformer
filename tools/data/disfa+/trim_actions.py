#!/usr/bin/env python3

import os
import argparse

def rename_files(directory_path, start_number):
    # verify that the directory exists
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return

    # get a list of all the JPG files in the directory
    jpg_files = [f for f in os.listdir(directory_path) if f.endswith('.jpg')]

    # verify that the start number is lower than the number of JPG files in the directory
    if start_number >= len(jpg_files):
        print(f"Start number {start_number} is higher than or equal to the number of JPG files in the directory.")
        return

    # remove all files whose name is lower than the start number
    for file_name in jpg_files:
        if int(file_name.split('.')[0]) < start_number:
            os.remove(os.path.join(directory_path, file_name))

    # rename all JPG files such that the new sequence starts from 0
    jpg_files = sorted([f for f in os.listdir(directory_path) if f.endswith('.jpg')])
    for i, file_name in enumerate(jpg_files):
        new_file_name = str(i).zfill(3) + '.jpg'
        os.rename(os.path.join(directory_path, file_name), os.path.join(directory_path, new_file_name))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename JPG files in directories specified in a text file.')
    parser.add_argument('directories_file', type=str, help='Path to the text file containing the list of directories and start numbers.')
    args = parser.parse_args()

    with open(args.directories_file, 'r') as f:
        for line in f:
            directory_path, start_number = line.strip().split(',')
            rename_files(directory_path, int(start_number))
