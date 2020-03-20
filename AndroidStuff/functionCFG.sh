#!/bin/sh

if [ $# -ne 2 ]
then
  echo "Usage: $0 <apk> <function (regex)>"
  exit
fi

androguard decompile -o output-$2 -f png -i $1 --limit "^.*$2.*"
