#!/bin/sh

# This script packs the application:
# 1. Creates a self-contained binary
# 2. Creates an RPM package

PWD=`pwd`
cd `dirname $0`

# Step 1: Update version information inside version.py
VERSION_FILE=app/version.py

# Get version info
VERSION_NO=`cat app/version`

# Get build info
BUILD_NO=`git rev-parse --short HEAD`

# Update values inside the version.py script
sed -i "s#VERSION = \"[.0-9]\+\"#VERSION = \"$VERSION_NO\"#" $VERSION_FILE
sed -i "s#BUILD = \"[a-zA-Z0-9]\+\"#BUILD = \"$BUILD_NO\"#" $VERSION_FILE

# Step 2: Create the binary
cd bin
./generate.sh
cd ..

# Step 3: Create the rpm package
cd rpm
./generate.sh $VERSION_NO $BUILD_NO
cd ..

# Step 4: Create the deb package
cd deb
./generate.sh
cd ..

cd $PWD