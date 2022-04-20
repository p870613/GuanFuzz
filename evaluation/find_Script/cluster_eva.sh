#!/bin/bash
seed_path='/home/lin/Desktop/Guan-fuzz-change/opjcopy_mean_eva/out/queue/'
#seed_path='/home/lin/libjpeg-turbo-guan-no-asan/build/jpegtran_test/out/queue/'
seed_info_path='/home/lin/Desktop/Guan-fuzz-change/opjcopy_mean_eva/out/20/'
#binary= '/home/lin/libjpeg-turbo-guan-no-asan/build/jpegtran_test/jpegtran'

count=0
current=0
valid=0
valid_error=0
valid_cur=0
invalid=0
invalid_error=0
invalid_cur=0

for file in `find $seed_path -type f | sort`
do
    file_name=""
    file_name_array=$(echo $file | tr "/" "\n")
    for i in $file_name_array
    do
        file_name=$i
    done
    echo $file_name
    predict=`cat $seed_info_path$file_name`
    echo "" 
    /home/lin/Desktop/Guan-fuzz-change/opjcopy_mean_eva/objcopy  $file 1> /dev/null 2> /dev/null
    result=$?
    echo $result"="
    if [ $result -eq 0 ]; then
        valid=$(($valid+1))
        if [ $predict -eq 1 ]; then
            valid_cur=$(($valid_cur+1))
            
        else
            valid_error=$(($valid_error+1))
            #/home/lin/Desktop/Guan-fuzz-change/djpeg_mean_eva/djpeg $file
            #read
        fi
    elif [ $result -eq 1 ]; then
        invalid=$(($invalid+1))
        if [ $predict -eq 0 ]; then
            invalid_cur=$(($invalid_cur+1))
        else
            #exec_argvread
            #/home/lin/Desktop/Guan-fuzz-change/djpeg_mean_eva/djpeg $file
            #read
            invalid_error=$((invalid_error+1))
        fi
    else 
        valid=$(($valid+1))
        if [ $predict -eq 1 ]; then
            valid_cur=$(($valid_cur+1))
        else
            valid_error=$(($valid_error+1))
            #/home/lin/Desktop/Guan-fuzz-change/djpeg_mean_eva/djpeg $file
            #read
        fi
    fi
    #if [ $predict -eq 1 ]; then
        #if [ $result -eq 0 ]; then
            #current=$(($current+1))
            #valid_cur=$((valid_cur+1))
        #else
            #valid_error=$((valid_error+1))
        #fi
    #fi 
    
    #if [ $predict -eq 0 ]; then
        #if [ $result -eq 1 ]; then
            #current=$(($current+1))
            #invalid_cur=$((invalid_cur+1))
        #else
            #invalid
        #fi
    #fi 

    count=$((count+1))
    if [ $count -eq 1000 ] ;then
        break;
    fi

    
done
echo $current
echo "valid" $valid $valid_cur $valid_error 
echo "scale=2; $valid_cur*100/$valid" | bc
echo "invalid" $invalid $invalid_cur $invalid_error 
echo "scale=2; $invalid_cur*100/$invalid" | bc
total=$(($invalid_cur+$valid_cur))
echo "total:" $(($total))
