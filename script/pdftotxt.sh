#!/bin/bash
FILES=data/raw/argument_transcripts/*.pdf
echo "Processing files."

for f in $FILES
do
  # take action on each file. $f store current file name
	filename=`echo $f |  cut -d'/' -f4`	
	# echo "filename = "$filename
	outputfilename=`echo $filename|cut -d'.' -f1`
	outputfilename=$outputfilename".txt"
	#echo "outputfilename = "$outputfilename
	pdftotext -layout $f $outputfilename
	OUT=$?
	if [ $OUT -ne 0 ];then
		echo $f >> errorfiles.txt
	fi
done