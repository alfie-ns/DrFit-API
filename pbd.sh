#!/bin/bash
if ./push.sh; then
    echo "Pushed successfully"
    cd ..
    rm -rf drfit-api # remove the cloned repository
else
    echo "Push failed"
fi