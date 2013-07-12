#!/bin/sh
sort -u list.txt > /tmp/1.txt
sort -u done.txt > /tmp/2.txt
diff /tmp/1.txt /tmp/2.txt | egrep '^< ' | cut -c3- > newlist.txt
