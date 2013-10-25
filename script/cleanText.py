import sys
import re
import os.path

def remove_line_numbers(line):
	components = re.split("\s+",line)
	if(re.search("\d+:?",components[0])):
		return " ".join(components[1:])
	else:
		return line

for filename in sys.argv[1:]:
	with open(filename) as f:
		name = os.path.basename(filename)
		outputName = filename.split(".")[0]+".cleaned.txt"
		out = open(outputName,'w')
		
		for line in f.readlines():
			if not line.isspace():
				if not line.strip().startswith('1111 '):
					if line.strip()[0].isdigit():
						workLine = line.strip()
						finalLine = remove_line_numbers(workLine)
						if len(finalLine) > 0:
							out.write(finalLine+"\n")
#							print finalLine.strip()
		
