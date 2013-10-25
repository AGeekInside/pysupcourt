import json
import sys
import os
import fnmatch
from os.path import basename
from pprint import pprint
import util

class _mem_data:
    commentCount = {}


def process_file(f):
    # processes file to determine comments from various speakers
    work_case_num = basename(f).split(".")[0]
    #print "work_case_num =",work_case_num
    _mem_data.commentCount[work_case_num] = {}
    
    json_data=open(f)

    data = json.load(json_data)
#    print data["speakers"]
    for entry in data["speakers"]:
#        print entry, data["speakers"][entry]
        _mem_data.commentCount[work_case_num][entry] = data["speakers"][entry]
        
    json_data.close()
    return


def main(argv):
    # Counts the counters of json files

    dirtocheck = argv[0]
    print "Cycle through all files..."

    for textFile in util.find_files(dirtocheck, '*.json'):
        try:
            process_file(textFile)
        except ValueError:            
            print "found error in",textFile
         
    for case in _mem_data.commentCount:
        print "_+_+_+_+_+_+_+_+_+_"
        print case
        print _mem_data.commentCount[case]

if __name__ == "__main__":
    main(sys.argv[1:])  