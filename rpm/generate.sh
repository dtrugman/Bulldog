#!/bin/bash

# This scripts generates an rpm using the spec file
# Args:
# $1 = VERSION
# $2 = BUILD

PKGS=pkgs
RPMROOT=~/rpmbuild
PROJROOT=`readlink -e ..`

# Remove old rpm files

rm -rf $RPMROOT

# Generate rpm

rpmbuild -bb --define "_version $1" --define "_build $2" --define "_projroot $PROJROOT" bulldog.spec
if [ $? -ne 0 ]; then
    echo "rpm generation failed!"
fi

# Copy newly created rpm

if [ ! -d $PKGS ]; then
    mkdir $PKGS
fi

cp $RPMROOT/RPMS/x86_64/* $PKGS/