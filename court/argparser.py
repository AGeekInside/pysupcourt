import re
import logging
import sys
import json 
from os.path import basename
import util


class _mem_options:
    fileName = ""


class _mem_parse:
    startCaseInfo = ["- - - - - - - - - - - - - - - -X",
                     "- - - - - - - - - - - - - - - - - x"]
    startAppearances = "APPEARANCES:"
    startContents = "C O N T E N T S"
    startProceedings = "P R O C E E D I N G S"
    endProceedings = "The case is submitted."
    stopWords = []


class _mem_data:
    case_info = ""
    appearances = ""
    location_info = ""
    contents = ""
    proceedings = ""
    case_num = ""
    speakers = {}
    word_dict = {}
    speaker_dict = {}
    speaker_comments = {}

    
def sort_dict(workDict):
    return [ (k,workDict[k]) for k in sorted(workDict.keys())] 
 
 
def has_new_speaker(line):
    sColon = re.compile('[:]')
    #notAllCaps = re.compile('/[a-z]/')

    if line.find(":") > 0:
        actor_name = sColon.split(line)[0]
        if actor_name.isupper():
            return True, actor_name
        else:
            return False, ""
    else:
        return False, ""


def parse_oral_arguments(work_file):
    # parses the various parts of the file, using the _mem_parse object
    #  File format
    
    #    StartCaseInfo
    #    case Info
    #    EndCaseInfo
    #    LocationInfo
    #    appearanceSTart
    #    appearnces info
    #    Proceedings start
    #    Proceedings info
    
    is_case_info = False
    is_location_info = False
    is_appearances = False
    is_proceedings = False
    is_contents = False
    
    for work_line in work_file.readlines():
#        print work_line.strip()
        if((work_line.startswith(_mem_parse.startCaseInfo[0])) or
           (work_line.startswith(_mem_parse.startCaseInfo[1]))):
            if(not is_case_info):
                is_case_info = True
                continue
            else: #found the end of caseinfo
                is_case_info = False
                is_location_info = True
                continue
        if(work_line.startswith(_mem_parse.startAppearances)):
            is_location_info = False
            is_appearances = True
            continue
        if(work_line.startswith(_mem_parse.startContents)):
            is_appearances = False
            is_contents = True
            continue
        if(work_line.startswith(_mem_parse.startProceedings)):
            is_contents = False
            is_proceedings = True
            continue

        if(work_line.find(_mem_parse.endProceedings)>-1):
            is_proceedings = False
            continue
        
        if(is_case_info):
            _mem_data.case_info += work_line.strip()+"\n"
        if(is_location_info):
            _mem_data.location_info += work_line.strip() +"\n"
        if(is_appearances):
            _mem_data.appearances += work_line.strip() +"\n"
        if(is_contents):
            _mem_data.contents += work_line.strip() + "\n"
        if(is_proceedings):
            _mem_data.proceedings += work_line.strip() +"\n"
                    
            
def process_case_info():
    # logic to process caseinfo portion
    print "Processing Case Info.. NOT TESTED"
    
#    print _mem_data.case_info.replace("\n", " ")
    workInfo = _mem_data.case_info.replace("\n", " ").split(":")
#    print workInfo
    
    petitioners = []
    respondents = []
    
    isPetitioner = True
    isRespondent = False
    
    for item in workInfo:
        if(item.find("Petitioners")>-1):
            isPetitioner = False
        if(isPetitioner):
            petitioners.append(item.strip())
        if(item.find("v.")>-1):
            isRespondent = True
            continue
        if((isRespondent)&(len(item.strip())>0)):
            respondents.append(item.strip())

    _mem_data.respondents = respondents
    _mem_data.petitioners = petitioners
    

def process_appearances():
    # logic to process the appearance section of an oral argument
    print "Processing Appearance Block, NOT DONE"


def add_line_to_word_dict(line,speaker=None):
    # adds every word found to the dictionary for the proceeding
    words = line.split(" ")
    for word in words:
        word = re.sub(r'\W+', '',word)
        word = word.upper()
        if len(word) > 0:
            if not word in _mem_parse.stopWords:
                if speaker:
                    if speaker in _mem_data.speaker_dict.keys():
                        util.add_to_dict(_mem_data.speaker_dict[speaker],word)
                    else:
                        _mem_data.speaker_dict[speaker] = {}
                        util.add_to_dict(_mem_data.speaker_dict[speaker],word)
                else:
#                     print "adding ",word," to large dictionary"
                    util.add_to_dict(_mem_data.word_dict,word)


def add_comment_to(speaker,comment):
    if _mem_data.speaker_comments.has_key(speaker):
        _mem_data.speaker_comments[speaker].append(comment)
    else:
        _mem_data.speaker_comments[speaker] = [comment]
    # adds the comments to the speaker's dictionary
    add_line_to_word_dict(comment,speaker)


def ignore_line(line):
    # returns true if it's a line that should be ignore in 
    # the proceedings
    if(line.startswith("ORAL ARGUMENT OF ")):
        return True
    if(line.startswith("ON BEHALF")):
        return True
    return False


def process_proceedings():
    # process the proceedings to find some basic metadata
    # find all speakers
    # for each speaker
    #    find all content
    #    number of comments
    
    print "Processing Proceedings"
    has_speaker = False
    speaker_name = ""

    curr_comment = ""
    curr_speaker = ""
    work_proceeding = _mem_data.proceedings.split("\n")
    
    first_speaker = False
    for workLine in work_proceeding:
        if(not ignore_line(workLine)):            
            #print workLine
            has_speaker, speaker_name = has_new_speaker(workLine)
            if(has_speaker):
                if(first_speaker):
                    add_comment_to(curr_speaker,curr_comment)
                    # TODO-- Get the comment code working for speakers
                first_speaker = True
                # speaker found on line
                util.add_to_dict(_mem_data.speakers,speaker_name)
                #print workLine
                curr_speaker = speaker_name
                curr_comment = workLine.split(":")[1]
            else:
                curr_comment += " "+workLine
            add_line_to_word_dict(workLine)
            
#     _mem_data.word_dict = sort_dict(_mem_data.word_dict)

            
def process(arg_file):
    parse_oral_arguments(arg_file)    
    process_case_info()
#    process_appearances()
    process_proceedings()


def word_count_to_json(word_dict,output_json_array):
#     print word_dict
    for word in word_dict.keys():
        count = word_dict[word]
        output_json_array.append({"word" : word, "count" : count})
        
          
def output_json():
    # this takes all the case info and output it to a json file
    print "output json to "+_mem_data.output_JSON_filename+"... "
    
    output_json = { }
    output_json['case_num'] = _mem_data.case_num
    output_json['appearances'] = _mem_data.appearances 
    output_json['caseinfo'] = _mem_data.case_info
    output_json['dictionary'] = []
#     print "_mem_data.word_dict =",_mem_data.word_dict
    word_count_to_json(_mem_data.word_dict, output_json['dictionary'])
    output_json['speakers'] = []
    speaker_file = _mem_data.output_speakers_json_file
    for speaker in _mem_data.speakers:
        speaker_entry = {}
        speaker_comment_count = _mem_data.speakers[speaker]
        speaker_entry['name'] = speaker
        speaker_entry['comment_count'] = speaker_comment_count
        speaker_dict = _mem_data.speaker_dict[speaker]
        speaker_entry['dictionary'] = []
#         print speaker_dict
        word_count_to_json(speaker_dict, speaker_entry['dictionary'])
#         speaker_entry['dictionary'] = speaker_dict
        output_json['speakers'].append(speaker_entry)
        speaker_file.write(json.dumps(speaker_entry)+"\n")
        
#        print speaker_dict

#     print json.dumps(output_json, indent=4, sort_keys=True)
    speaker_file.close()
    output_file = open(_mem_data.output_JSON_filename,"w")
    output_file.write(json.dumps(output_json, indent=4, sort_keys=True))
    output_file.close()

    
def main(argv):
    print "Starting..."
    # Display progress logs on stdout
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

    work_filename = argv[0]
    work_case_num = basename(work_filename).split(".")[0]
    stop_words_file = open("stopwords.txt")
    for line in stop_words_file:
        _mem_parse.stopWords.append(line.strip().upper())

    #print _mem_parse.stopWords
    _mem_data.output_JSON_filename = work_filename.split(".")[0]+".json"
    output_speakers_json_filename = work_filename.split(".")[0]+"-speakers.json"
    _mem_data.output_speakers_json_file = open(output_speakers_json_filename, 'w')
    _mem_data.case_num = work_case_num
    arg_file = open(work_filename)
    print work_filename
    process(arg_file)
    #print _mem_data.wordDict
    output_json()
    
    
if __name__ == "__main__":
    main(sys.argv[1:])  