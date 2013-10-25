import json
import sys
from os.path import basename
import numpy
import util


def output_distances(speakers,output_file):
    '''Given an array of speakers, creates a file for distance matrixes for d3.'''
    speaker_names = []
    
    num_speakers = len(speakers)
    work_cosine_dist_matrix = numpy.zeros((num_speakers,num_speakers))
    work_jaccard_dist_matrix = numpy.zeros((num_speakers,num_speakers))

    for outer_counter, outer_speaker in enumerate(speakers):        
        outer_name = outer_speaker['name']  
        speaker_names.append(str(outer_name))
        word_list = outer_speaker['dictionary']
        outer_dict = {}
        for entry in word_list:
            outer_dict[entry['word']] = entry['count']
        for inner_counter, inner_speaker in enumerate(speakers):
            word_list = inner_speaker['dictionary']
            inner_dict = {}
            for entry in word_list:
                inner_dict[entry['word']] = entry['count']
#             inner_name = inner_speaker['name']
            cosine_dist = util.cosine_distance(outer_dict, inner_dict)
            work_cosine_dist_matrix[outer_counter,inner_counter] = cosine_dist
            jaccard_dist = util.jaccard_distance(outer_dict, inner_dict)
            work_jaccard_dist_matrix[outer_counter,inner_counter] = jaccard_dist
            
    util.output_dist_matrix(work_jaccard_dist_matrix,speaker_names,output_file,'_jaccard')
    util.output_dist_matrix(work_cosine_dist_matrix,speaker_names,output_file,'_cosine')


def output_tag_cloud(speakers, output_file):
    '''Outputs a tag cloud for dictionaries of the speakers included.'''
    
    speaker_names = []
    
    for counter,entry in enumerate(speakers):
        word_list = []
        count_list = []
        var_suffix = 'speaker_'+str(counter)
        
        words_var_str = 'var words_'+var_suffix+' = '
        count_var_str = 'var count_'+var_suffix+' = '

        speaker_name = entry['name']
        speaker_names.append(str(speaker_name))
        name_var_str = 'var name_'+var_suffix+' = \''+speaker_name+'\''

        for dict_entry in entry['dictionary']:
            word_list.append(str(dict_entry['word']))
            count_list.append(str(dict_entry['count']))

        words_var_str += str(word_list)
        count_var_str += str(count_list)
        
        output_file.write(name_var_str+'\n'+words_var_str+'\n'+count_var_str+'\n')
    
    output_file.write("var speakers_names = "+str(speaker_names)+"\n")
        

def output_worduse(speakers, output_file):
    '''Outputs information used to create a word_use table'''
    
    # create var for columns
    # create var for rows
    
    num_rows = len(speakers)
    print 'There are',str(num_rows),'speakers.'
    
    for speaker in speakers:
        num_words_used = len(speaker['dictionary'])
        speaker_name = speaker['name']
        print speaker_name, 'used', str(num_words_used),'words.'


def main(argv):
    '''Reads in a json speaker file and generates data for tag cloud.'''

    # Generate an output of json data for tag cloud
    # Generate a distance matrix for the speakers
    
    speaker_filename = argv[0]
    speaker_file = open(speaker_filename,'r')
    
    output_filename_base = basename(speaker_filename).split('.')[0]

    www_output_dir = 'www/'
    js_output_dir = www_output_dir+'js/'
    
    output_dist_filename = js_output_dir+output_filename_base+'_dist.js'
    output_dist_file = open(output_dist_filename, 'w')
 
    output_tag_filename = js_output_dir+output_filename_base+'_tag.js'
    output_tag_file = open(output_tag_filename, 'w')

    output_worduse_filename = js_output_dir+output_filename_base+'_word_use.js'
    output_worduse_file = open(output_worduse_filename, 'w')
 
    speakers = []    
    for line in speaker_file:
        speaker_entry = json.loads(line)
        speakers.append(speaker_entry)
 
    output_distances(speakers, output_dist_file)
    output_tag_cloud(speakers, output_tag_file)
    output_worduse(speakers, output_worduse_file)

    output_dist_file.close()
    output_tag_file.close()
            
if __name__ == "__main__":
    main(sys.argv[1:])  