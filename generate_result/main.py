#!/usr/bin/python
import json
from get_times_scenarios import *
from make_plot import *

def main():
    data = get_times_scenarios()
    make_plot(data)
    
if __name__ == '__main__':
    main()
