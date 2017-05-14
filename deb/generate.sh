#!/bin/bash

# This scripts generates a deb file from the rpm file
# It assumes the default project structure and require no arguments

PKGS=pkgs
RPMPKGS=../rpm/pkgs

# Generate deb

alien --scripts --keep-version $RPMPKGS/*
if [ $? -ne 0 ]; then
    echo "deb generation failed!"
fi

# Copy newly created deb

if [ ! -d $PKGS ]; then
    mkdir $PKGS
fi

mv *.deb $PKGS/