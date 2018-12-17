#!/usr/bin/python
from datetime import datetime
import json

def calc_duration(start_time,stop_time):
    split_start_time = start_time.split(':')
    start_hour = int(split_start_time[0])
    start_minutes = int(split_start_time[1])
    start_seconds = int(split_start_time[2].split(".")[0])
    start_miliseconds = int(split_start_time[2].split(".")[1])
    
    split_stop_time = stop_time.split(':')
    stop_hour = int(split_stop_time[0])
    stop_minutes = int(split_stop_time[1])
    stop_seconds = int(split_stop_time[2].split(".")[0])
    stop_miliseconds = int(split_stop_time[2].split(".")[1])
    
    base_time = datetime.now()

    start_time = datetime(base_time.year, base_time.month, base_time.day, start_hour, start_minutes, start_seconds, start_miliseconds)
    stop_time = datetime(base_time.year, base_time.month, base_time.day, stop_hour, stop_minutes, stop_seconds, stop_miliseconds)
    duration_in_seconds = (stop_time - start_time).total_seconds()
    return duration_in_seconds


def open_file():
    file=open('times.json','r')
    data = file.read()
    file.close()
    #print "data= %s" % data
    return json.loads(data)

def get_times_scenarios():
    content = open_file()
    for i in range(1,5):
        scenario = 'scenario%s' % i 
        start = content[scenario]['start_time']
        stop = content[scenario]['stop_time']
        content[scenario]['duration'] = calc_duration(start,stop)
        """
        print scenario
        print "Start: %s" % content[scenario]['start_time']
        print "Stop:  %s" % content[scenario]['stop_time']
        print "Duration:  %s" % content[scenario]['duration']
        print
        print
        """
    #print content
    # return the content in json format
    return content


