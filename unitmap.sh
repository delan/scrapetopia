#!/bin/bash
tmpdir=/tmp/lectopia
tmp=$tmpdir/$$

p1='http://dbs.ilectures.curtin.edu.au/lectopia/lectopia.lasso?ut='
p2='<td.+>([^<]+)</h2></div>'
p3='s!'"$p2"'!\1!'

mkdir -p $tmpdir

function lock {
	mkdir $tmp.lock 2> /dev/null
	while [ x"$?" != x"0" ] ; do
		sleep 0.1
		mkdir $tmp.lock 2> /dev/null
	done
}

function unlock {
	rmdir $tmp.lock
}

for i in {0..9999}; do
	(
	rm -f $tmp.$i
	curl -so $tmp.$i "$p1"$i
	if [ -e "$tmp.$i" ]; then
		lock
		printf 'unit\t%06d\t' $i
		egrep -o "$p2" "$tmp".$i | sed -r "$p3"
		unlock
	else
		printf 'nope\t%06d\n' $i
	fi
	rm -f $tmp.$i
	) &
	if (( $i % 64 == 0 )); then wait; fi
done
