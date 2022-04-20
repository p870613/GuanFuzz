#!/bin/bash

for file in `find ./exe_dir/ -type f`
do
    echo $file
    /bin/bash $file
    read a
done
