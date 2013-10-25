import re
import matplotlib.pyplot as plt
import networkx as nx
import logging
import sys


def has_new_speaker( line ):
    sColon = re.compile('[:]')
    notAllCaps = re.compile('/[a-z]/')

    if (line.find(":") > 0):
        actorName = sColon.split(line)[0]
        if actorName.isupper():
            return True, actorName
        else:
            return False, ""
    else:
        return False, ""

def add_to_dict(work_dict, item):
    if(work_dict.has_key(item)):
        work_dict[item] += 1
    else:
        work_dict[item] = 1

def process():
    arg_file = open('samp/00-151.cleaned.txt')
    digraphFile = open('tempOut.gv','w')

    inProceedings = False
    speakerNum = 0
    prevSpeaker = ""
    justiceNames = {}
    nonJusticeNames = {}
    followCount = {}
    speakers = []
    commentCount = 0
    rankString = "\t{rank=same; "
    speakerCommentNodes = dict()
    speakerComments = dict()
    
    commentString = ""
        
    currentComment = ""
    
    for line in arg_file.readlines():
        # case heading
        # appearance
        # contents
        # proceedings
        print line.strip()+"\n"
        if (line.startswith("P R O C E E D I N G S")):
            #print "starting proceedings"
    #        print line.strip()
            inProceedings = True
        if (inProceedings):
            hasSpeaker, speakerName = has_new_speaker( line )
            #print line.strip()
            currentComment = currentComment + line
            if (hasSpeaker):
                speakerName = speakerName #+str(speakerNum)
                currCommentNode = "\"comment_"+str(commentCount)+"_"+speakerName+"\""
                commentCount = commentCount + 1
                if (not speakerName in speakers):
                    # first time the speaker is seen
                    speakers.append(speakerName)
                    speakerCommentNodes[speakerName] = []
                    speakerComments[speakerName] = []
                if (speakerNum>0):
                    speakerComments[speakerName] = currentComment
                    currentComment = ""
                    # add ability to capture the number of comments for a speaker
                    #print "-----"
                    #print "prevCommentNode = ",prevCommentNode
                    #print "currCommentNode = ",currCommentNode
                    #print "-----"
                    # add creation of comment node
                    commentString = commentString + "\t"+prevCommentNode +" -> "+currCommentNode+"\n"#+" [constraint=false]\n"
                    #commentString = ""
                speakerCommentNodes[speakerName].append(currCommentNode)
                prevSpeaker = speakerName
                prevCommentNode = currCommentNode
                if (speakerName.find("JUSTICE")>-1):
                    #print speakerName
                    add_to_dict(justiceNames, speakerName)
#                    if speakerName in justiceNames.keys():
#                        justiceNames[speakerName] = justiceNames[speakerName] + 1
#                    else:
#                        justiceNames[speakerName] = 1
                else:
                    add_to_dict(nonJusticeNames, speakerName)
#                    if speakerName in nonJusticeNames.keys():
#                        nonJusticeNames[speakerName] = nonJusticeNames[speakerName] + 1
#                    else:
#                        nonJusticeNames[speakerName] = 1
     #           digraphStr = digraphStr + "\t \""+speakerName+"\" -> \""+line+"\" \n"
                prevLine = line
     #           print "speakerName =",speakerName
                speakerNum = speakerNum + 1
    #            print line.strip()
    
    #print speakerComments
    #print speakerCommentNodes
            
    #print justiceNames
    #print nonJusticeNames
    #print followCount
    
    argGraph = nx.Graph()
    argGraph.add_nodes_from(justiceNames,bipartite=0)
    argGraph.add_nodes_from(nonJusticeNames,bipartite=1)
    
    #print argGraph.nodes()
    
    digraphStr = "digraph test { \n\t\n"
    #digraphStr = digraphStr + "\tsubgraph cluster0 {\n"
    
    #rankStr = "{rank = same; "
    
    clusterCount = 0 
    clusterStart = "\tsubgraph cluster"
    speakerLinkStr = ""
    
    for name in speakers:
        digraphStr = digraphStr + clusterStart+str(clusterCount)+" {\n\t\t\""+name+"\" [label=\""+name+"\" ]\n"
        rankString = rankString + " \""+name+"\" "
        for comment in speakerCommentNodes[name]:
            #commentString = ""
            digraphStr = digraphStr + "\t\t"+comment+"\n"
        if(clusterCount>0):
            speakerLinkStr = speakerLinkStr + "-> \""+name+"\""
        else:
            speakerLinkStr = "\t\""+name+"\""
        digraphStr = digraphStr + "\t}\n"
        clusterCount = clusterCount + 1
    #    rankStr = rankStr + "\""+justiceName+"\""
    
    rankString = rankString + " }\n"
    
    digraphStr = digraphStr + speakerLinkStr #+ "[style=invis]\n"
    #digraphStr = digraphStr + rankStr + "}\n"
    
    #rankStr = "{rank = same; "
    
    #digraphStr = digraphStr + "\tsubgraph cluster1 {\n"
    #for nonJusticeName in nonJusticeNames:
        
        #digraphStr = digraphStr + "\t\t\""+nonJusticeName+"\"\n"
    #    rankStr = rankStr + "\""+nonJusticeName+"\""
    
    #digraphStr = digraphStr + "\t}\n"
    
    #digraphStr = digraphStr + rankStr + "}\n"
    
    #digraphStr = digraphStr + "\n\tedge[constraint=false];\n\n"
    
    for workLine in followCount.keys():
        items = workLine.split("|")
        source = items[0]
        dest = items[1]
        label = followCount[workLine]
        argGraph.add_edge(source,dest,{'weight':int(label)})
    #    digraphStr = digraphStr + "\t\""+source+"\" -> \""+dest+"\"\n"
    
    digraphStr = digraphStr + "\n" +commentString
    
    digraphStr = digraphStr + "\n}\n"
    #print argGraph.edges()
    
    digraphFile.write(digraphStr)
    digraphFile.close()
    #print digraphStr

def main(argv):
    print "Starting..."
    # Display progress logs on stdout
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

    #fh = open('data/txt/cleaned/12-307.cleaned.txt')

    
    process()

if __name__ == "__main__":
    main(sys.argv[1:])  


#nx.draw(argGraph)
#nx.connected_components(argGraph)