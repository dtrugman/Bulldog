#!/bin/bash

# This scripts generates an RPM using the spec file
# Args:
# $1 = VERSION
# $2 = BUILD

PKGS=pkgs
RPMROOT=~/rpmbuild
PROJROOT=`readlink -e ..`

# Remove old RPM files

rm -rf $RPMROOT

# Generate RPM

rpmbuild -bb --define "_version $1" --define "_build $2" --define "_projroot $PROJROOT" kuvasz.spec
if [ $? -ne 0 ]; then
    echo "RPM generation failed!"
fi

# Copy newly created RPM

if [ ! -d $PKGS ]; then
    mkdir $PKGS
fi

cp $RPMROOT/RPMS/x86_64/* $PKGS/