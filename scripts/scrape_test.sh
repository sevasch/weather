#!/bin/sh
#export PATH=/usr/local/sbin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin

# Script to web scrape data and store to file to temp folder. 

echo "Start web scraping..."

# Remove all files from temp 
rm -f temp/*

# Download data and store in temp folder
TIMESTAMP=$(date +%s)
curl -X 'GET' \
  'https://api.existenz.ch/apiv1/hydro/latest?locations=2135&parameters=temperature%2Cflow&version=1.0.42' \
  -H 'accept: */*' > /temp/aaredata_$TIMESTAMP.json

echo "Web scraping completed!"
