#!/bin/bash

# remove empty lines of file
clean_file(){
    echo "Removing empty lines of cap$1.txt file"
    awk 'NF>0' cap$1.txt > tmp_cap$1.txt
}

# remove temp files
clean_directory(){
    echo "Removing temp files"
    for i in {1..4}
        do
            rm tmp_cap$i.txt
    done

}

get_first_line(){
    cat tmp_cap$1.txt | awk '{print $1}' | head -1
}

get_last_line(){
    cat tmp_cap$1.txt | awk '{print $1}' | tail -1
}


for i in {1..4}
    do
        echo "Getting times of experiment $i"
        clean_file $i
        first_line=$(get_first_line $i)
        last_line=$(get_last_line $i)
        string='{"start_time": "'$first_line'", "stop_time": "'$last_line'", "duration": ""}'
        vector_json[$i]=$string
done

struct_json='{"scenario1": '${vector_json[1]}',"scenario2": '${vector_json[2]}',"scenario3": '${vector_json[3]}',"scenario4": '${vector_json[4]}'}'
echo $struct_json > times.json
clean_directory



