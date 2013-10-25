import os
import fnmatch
import math
import numpy


class _mem:
    debug_mode = True
    debug_level = 100
    

def output_dist_matrix(dist_matrix, entry_list, output_file, varPrefix=''):
    '''Outputs the computed distance matrix to an output file.'''
    
    matrix_output = []
    
    data_matrix = numpy.array(dist_matrix)
    row = 0
    
    for row_data in data_matrix:
        col = 0
        row_output = []
        for colData in row_data:
            row_output.append([colData, row, col])
            col += 1
        matrix_output.append(row_output)
        row += 1
    print 'Outputting distance matrix variables for heat map with prefix \''+varPrefix+'\'.'
    
    output_file.write('var maxData'+varPrefix+' = ' + str(numpy.amax(data_matrix)) + ";\n")
    output_file.write('var minData'+varPrefix+' = ' + str(numpy.amin(data_matrix)) + ";\n")
    output_file.write('var data'+varPrefix+' = ' + str(matrix_output) + ";\n")
    output_file.write('var cols'+varPrefix+' = ' + str(entry_list) + ";\n")
    output_file.write('var rows'+varPrefix+' = ' + str(entry_list) + ";\n")


def add_to_dict(work_dict, item):
    if(work_dict.has_key(item)):
        work_dict[item] += 1
    else:
        work_dict[item] = 1


def find_files (path, fltr):
    for root, _, files in os.walk(path):
        for f in fnmatch.filter(files, fltr):
            yield os.path.join(root, f)


def debug_out(workStr, level=50):
    if(_mem.debug_mode):
        if(level<_mem.debug_level):
            print workStr


def _cosine_denom(work_dict):
    '''Calculates the denominator portion for a given dictionary.'''
    
    work_denom = 0
    for term in work_dict.keys():
        work_denom += (work_dict[term]*work_dict[term])

    return math.sqrt(work_denom)


def cosine_distance(dictA, dictB):
    '''Calculates the cosine similarity between to dictionaries of word counts.'''
    debug_value = 500
    
    keysA = dictA.keys()
    keysB = dictB.keys()
    
    union = list(set(keysA) | set(keysB))
    
    numerator = 0
    
    for term in union:
        if term in keysA:
            aVal = dictA[str(term)]
        else:
            aVal = 0
        if term in keysB:
            bVal = dictB[str(term)]
        else:
            bVal = 0 
        numerator += aVal * bVal
        
    a_denom = _cosine_denom(dictA)
    b_denom = _cosine_denom(dictB)

    cosine_dist = 1 - numerator/(a_denom*b_denom)
    debug_out('cosine_dist is '+str(cosine_dist), debug_value)
    return cosine_dist
    
def jaccard_distance(dictA, dictB):
    '''Calculate the jaccard distance between two dictionaries.'''
    debug_value = 500
            
    cmdsA = dictA
    cmdsB = dictB
    
    debug_out("cmdsA ="+str(cmdsA),debug_value)
    debug_out("cmdsB ="+str(cmdsB),debug_value)
    keysA = cmdsA.keys()
    keysB = cmdsB.keys()
    intersect = list(set(keysA) & set(keysB))
    union = list(set(keysA) | set(keysB))
    if len(union) > 0:
        dist = 1 - ((len(intersect)*1.0)/(len(union)*1.0))
    else:
        if len(intersect) > 0:
            dist = 0.0
        else:
            dist = 1.0
    
    debug_out("keysA ="+str(keysA), debug_value)
    debug_out("keysB ="+str(keysB), debug_value)
    debug_out("len(intersect) = "+str(len(intersect)), debug_value)
    debug_out("len(union) = "+str(len(union)), debug_value)
    debug_out("dist = "+str(dist), debug_value)
    debug_out("------------", debug_value)
    return dist


def create_tag_cloud(text, outputName):
    YOUR_TEXT = "A tag cloud is a visual representation for text data, typically\
        used to depict keyword metadata on websites, or to visualize free form text."

#    tags = make_tags(get_tag_counts(YOUR_TEXT), maxsize=80)

#    create_tag_image(tags, 'cloud_large.png', size=(900, 600), fontname='Lobster')
