#!/bin/bash
for file in data/txt/cleaned/*.txt; do
   python argparser.py "$file" 
done


