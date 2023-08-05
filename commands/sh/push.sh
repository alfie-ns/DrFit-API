#!/bin/bash

# Push code to repository, pulling the latest changes first

cd .. cd .. 
git pull origin main
git add -A
git commit -m "Update"
git push origin main
