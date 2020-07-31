#!/usr/bin/env bash

# good functions

## FIXME:
## In OSX, 'readlink -f' option does not exist, hence
## we have our own readlink -f behavior here.
## Once OSX has the option, below function is good enough.
##
## readlink() {
##     return /bin/readlink -f "$1"
## }
##
readlink() {
    targetFile=$1

    cd "$(dirname $targetFile)" || return 1
    targetFile=$(basename $targetFile)

    # Iterate down a (possible) chain of symlinks
    while [ -L "$targetFile" ]
    do
        targetFile=$(env readlink $targetFile)
        cd "$(dirname $targetFile)" || return 1
        targetFile=$(basename $targetFile)
    done

    # Compute the canonicalized name by finding the physical path
    # for the directory we're in and appending the target file.
    physicalPath=`pwd -P`
    result=$physicalPath/$targetFile
    echo $result
}
