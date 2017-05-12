#!/bin/sh

# This script creates an installer for the application

PWD=`pwd`
cd `dirname $0`

# Step 1: Update version information inside version.py
VERSION_FILE=app/version.py

# Get build info
BUILD_NO=`git rev-parse --short HEAD`

# Update values inside the version.py script
sed -i "s#BUILD = \"[a-zA-Z0-9]\+\"#BUILD = \"$BUILD_NO\"#" $VERSION_FILE

# Step 2: Create the installer
pyinstaller --onefile kuvasz.py

cd $PWD