#!/bin/bash

HOSTNAME=a4329518-3cfd-46b8-8e86-109e8893306b@a4329518-3cfd-46b8-8e86-109e8893306b-00-skzrs3tf1p0f.worf.replit.dev

# We only deploy the main branch
current_branch=adding-streamlit

if [ -z "$current_branch" ]; then
    echo "No branch name found"
    exit 1
fi  

# Create a ZIP archive of the current branch
git archive -v -o output.zip "$current_branch"

if [ $? -ne 0 ]; then
    echo "Failed to create archive"
    exit 1
fi  

echo "Created archive of branch '$current_branch' in output.zip"

# Upload the ZIP file using SCP
scp -i ~/.ssh/replit -P 22 output.zip "$HOSTNAME":~/

if [ $? -ne 0 ]; then
    echo "Failed to upload archive"
    exit 1
fi

echo "Uploaded archive to Replit"

# Run the deploy script on Replit
ssh -i ~/.ssh/replit -p 22 "$HOSTNAME" "cd ~/workspace && unzip -o ~/workspace/output.zip && exit"

if [ $? -ne 0 ]; then
    echo "Failed to unzip archive"
    exit 1
fi

echo "Deployed to Replit"
