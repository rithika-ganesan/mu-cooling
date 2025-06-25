#!/bin/bash

##### Gets all instances of 'lowerWidth' in a file and stores them

input="HFOFO-original-cleaned.in"
output="abs_widths.txt"

echo "period index width" > $output 

awk '/lowerWidth=/ {
	split($6, width, "=");
	split($7, zstr, "=");
	split(zstr[2], z, "+");
	split(z[2], period, "*");
	print period[2], (z[1] - 150) / 700, width[2]
}' $input > $output 
