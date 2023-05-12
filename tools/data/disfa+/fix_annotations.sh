#!/usr/bin/env bash

fix_annotation() {
    base="../../../data/disfa+/"
    prefix=$1
    anno=$2
    bkup="${anno}.bkup"

    cp $base/$anno $base/$bkup

    rm $base/$anno

    # Open the file for reading
    while read line; do
	filedir=`echo $line | awk '{print $1}'`
	dir="$base/$prefix/$filedir"
	label=`echo $line | awk '{print $3}'`
	numfiles=$(( `find $dir -type f -name "*.jpg" | wc -l | tr -d ' '` - 1 ))
	echo "$filedir $numfiles $label" >> $base/$anno
    done < $base/$bkup
}

fix_annotation rawframes_test disfa+_test_list_rawframes.txt
fix_annotation rawframes_train disfa+_train_list_rawframes.txt
fix_annotation rawframes_val disfa+_val_list_rawframes.txt
