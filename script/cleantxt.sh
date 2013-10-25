FILES=data/txt/*.txt
echo "Processing files."

for f in $FILES
do
	output=`echo $f|cut -d'.' -f1`
	output=$output"-cleaned.txt"
	echo $output
	while read line
	do
						
	done < $f
done