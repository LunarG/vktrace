#!/bin/bash
# Note: For this script to run successfully:
#    cube must be in PATH.
#    SCREEENSHOT_LAYER_PATH should be set to directory containing the screenshot layer
#set -x
if [ -t 1 ] ; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    NC=''
fi

printf "$GREEN[ RUN      ]$NC $0\n"

python3 vktracereplay.py ${PWD}/../vktrace/vktrace ${PWD}/../vktrace ${PWD}/../vktrace/vkreplay

if [ $? -eq 0 ] ; then
	printf "$GREEN[  PASSED  ]$NC ${PGM}\n"
else
	printf "$RED[  FAILED  ]$NC Trace/replay tests failed.\n"
	printf "$RED[  FAILED  ]$NC ${PGM}\n"
	printf "TEST FAILED\n"
	exit 1
fi

exit 0
