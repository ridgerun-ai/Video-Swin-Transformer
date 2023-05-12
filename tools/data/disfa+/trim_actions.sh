#!/usr/bin/env bash

echo -n "Trimming train actions..."
./trim_actions.py action_start_train.txt
echo -e -n "done!\nTrimming val actions..."
./trim_actions.py action_start_val.txt
echo -e -n "done!\nTrimming test actions..."
./trim_actions.py action_start_test.txt
echo "done!"

echo "Fixing annotations"
./fix_annotations.sh
