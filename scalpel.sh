#!/bin/sh

cd data
a="$$$RANDOM$RANDOM$$"
b="$$$RANDOM$RANDOM$$"
sort -u list.txt > /tmp/$a
sort -u done.txt > /tmp/$b
diff /tmp/$a /tmp/$b | egrep '^< ' | cut -c3- > list.txt
rm done.txt
