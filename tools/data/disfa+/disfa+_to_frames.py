#!/usr/bin/env python3

import argparse
import os
import shutil
from pathlib import Path
import random

actions={
    'anger' : ['Anger'],
    'disgust' : ['Disgust'],
    'fear' : ['Fear'],
    'happiness' : ['Happy', 'Happiness'],
    'sadness' : ['Sad', 'Sadness'],
    'surprise' : ['Surprise']
}

def dump_output(output, test, val, train):
    layout = [
        (test, 'test'),
        (val, 'val'),
        (train, 'train')
    ]

    prefix='rawframes'
    ds_name='disfa+'

    # Create each directory in the layout
    for split, directory in layout:
        directory_path = output.joinpath(f'{prefix}_{directory}')
        os.makedirs(directory_path)
        
        list_path = output.joinpath(f'{ds_name}_{directory}_list_rawframes.txt')
        list_file = open(list_path, 'w')

        random.shuffle(split)

        for video in split:
            action = video[0]
            trail = video[1]
            video_name = video[2]

            action_path = directory_path.joinpath(action)
            if not action_path.exists():
                os.makedirs(action_path)

            # Copy the trail directory into the action_path
            video_path = action_path.joinpath(video_name)
            shutil.copytree(trail, video_path)

            # Append the entry to the rawframes file
            num_files = len(list(video_path.glob('*.jpg'))) - 1
            action_index = list(actions.keys()).index(action)
            list_file.write(f'{os.path.join(action, video_name)} {num_files} {action_index}\n')
            

def build_video_name(subject, trail):
    """
    Builds a video name from the subject and trail number
    """
    return f'{subject}_{trail}'

def extract_action_from_trail(trail):
    """
    Find which action matches best the name in the trail
    """    
    for action in actions:
        for variant in actions[action]:
            if variant in trail:
                return action
    return None
    

def traverse_dataset(root):
    """
    Traverses the disfa+ dataset and creates the directory layout
    """

    videos = []
    for subject in root.joinpath('Images').glob('SN*/'):
        for trail in subject.iterdir():
            action = extract_action_from_trail(trail.name)
            if not action:
                continue

            video_name = build_video_name(subject.name, trail.name)
            videos.append((action, trail, video_name))

    return videos

def split_group (group, test_split, val_split):
    """
    Splits a group of videos into train, test and validation
    """

    test = []
    train = []
    val = []

    # shuffle the group
    random.shuffle(group)

    # Split the sorted videos into train, test and validation
    test_split = int(len(group) * test_split)
    val_split = int(len(group) * val_split)

    val = group[:val_split]
    test = group[val_split:val_split+test_split]
    train = group[val_split+test_split:]

    return test, val, train

def split_dataset(videos, test_split, val_split):
    """
    Splits the dataset into train, test and validation
    """

    test = []
    train = []
    val = []
    
    for action in actions:
        action_group = [video for video in videos if video[0] == action]
        action_test, action_val, action_train = split_group(action_group, test_split, val_split)
        test += action_test
        val += action_val
        train += action_train
        
    return test, val, train

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--disfa', type=Path, required=True, help='Path to the input disfa+ dataset')
    parser.add_argument('--output', type=Path, required=True, help='Path to output directory')
    parser.add_argument('--test_split', type=float, default=0.12, help='Percentage of the dataset to use for testing')
    parser.add_argument('--val_split', type=float, default=0.08, help='Percentage of the dataset to use for validation')
    
    args = parser.parse_args()

    # If the output directory does not exist, create it
    if not args.output.exists():
        os.makedirs(args.output)
    # Otherwise check that it is empty
    #elif os.listdir(args.output):
    #    raise Exception('Output directory is not empty')

    # Validate that the input exists
    if not args.disfa.exists():
        raise FileNotFoundError('Input directory does not exist')
    # If it does exist, validate that the Images and Labels subdirectories exist
    elif (not args.disfa.joinpath('Images').exists() or not args.disfa.joinpath('Labels').exists()):
        raise Exception('Input directory is not a disfa+ dataset')

    # Validate that the test and val splits don't exceed 1
    if args.test_split + args.val_split >= 1:
        raise ValueError('Test and val splits cannot be equal to or exceed 1')

    videos = traverse_dataset(args.disfa)
    test, val, train = split_dataset(videos, args.test_split, args.val_split)

    dump_output(args.output, test, val, train)
    
    print(f'From {len(videos)} videos, {len(test)} were used for testing, {len(val)} for validation and {len(train)} for training')

if __name__ == '__main__':
    main()
