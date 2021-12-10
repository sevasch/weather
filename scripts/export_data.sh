#!/bin/sh
#export PATH=/usr/local/sbin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin

# Script copies data from temporary dir to external data dir

echo "Exporting data to storage..."

cp -R /temp/* /data/

echo "Data Export complete! "