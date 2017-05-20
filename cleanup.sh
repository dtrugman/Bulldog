#!/bin/sh

# Cleans up midleware directories and files created by the pack script
# WARNING: Removes the binaries and packages as well!

rm -rf deb/pkgs
rm -rf rpm/pkgs
rm -rf bin/dist bin/build