#!/bin/bash
tmp=/tmp/lectopia-$$.tmp

p1='http://dbs.ilectures.curtin.edu.au/lectopia/lectopia.lasso?ut='
p2='<td.+>([^<]+)</h2></div>'
p3='s!'"$p2"'!\1!'

for i in {0..9999}; do
	rm -f "$tmp"
	curl -so "$tmp" "$p1"$i
	if [ -e "$tmp" ]; then
		printf '%s\t' $i
		egrep -o "$p2" "$tmp" | sed -r "$p3"
	fi
done

rm -f "$tmp"
