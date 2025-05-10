#!/bin/bash

# Download the NAVAll.txt file
curl -s https://www.amfiindia.com/spages/NAVAll.txt -o NAVAll.txt

# Extract Scheme Name ($4) and Net Asset Value ($5), save to TSV
awk -F';' 'NF>=5 && $4!="" {print $4 "\t" $5}' NAVAll.txt > nav_data.tsv

# Remove the downloaded file
rm NAVAll.txt
