#!/bin/bash
current_dir=$(basename "$PWD") # Get current directory name
if ./push.sh; then 
cd .. 
rm -rf "$current_dir" # Run the push script 1st , then back out,
fi
# Streamline procwaa