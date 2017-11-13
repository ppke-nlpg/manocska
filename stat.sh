echo -n "all frames: "
cat manocska.txt | wc -l
echo -n "all INF frames: "
cat manocska.txt  | grep "INF" -c
echo -n "INF frames (in ONE resource): "
cat manocska.txt | grep "INF" | cut -d$'\t' -f5,7 | egrep $'0\t|\t0' -c
echo -n "INF frames (in TWO resource): "
cat manocska.txt | grep "INF" | cut -d$'\t' -f5,7 | egrep -v $'0\t|\t0' -c
echo -n "all NON-INF frames: "
cat manocska.txt | grep -v "INF" -c
echo -n "NON-INF frames (in ONE resources): "
cat manocska.txt | grep -v "INF" | cut -d$'\t' -f3,4,5,6 | egrep $'^(0\t0\t0\t[1-9][0-9]*|0\t0\t[1-9][0-9]*\tNone|0\t[1-9][0-9]*\t0\tNone|[1-9][0-9]*\t0\t0\tNone)$' -c
echo -n "NON-INF frames (in TWO resources): "
cat manocska.txt | grep -v "INF" | cut -d$'\t' -f3,4,5,6 | egrep -v $'^(0\t0\t0\t[1-9][0-9]*|0\t0\t[1-9][0-9]*\tNone|0\t[1-9][0-9]*\t0\tNone|[1-9][0-9]*\t0\t0\tNone)$' |\
 egrep -v $'^[1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*$' | egrep -v $'^([1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*\tNone|[1-9][0-9]*\t[1-9][0-9]*\t0\t[1-9][0-9]*|[1-9][0-9]*\t0\t[1-9][0-9]*\t[1-9][0-9]*|0\t[1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*)$' -c
echo -n "NON-INF frames (in THREE resources): "
cat manocska.txt | grep -v "INF" | cut -d$'\t' -f3,4,5,6 |  egrep $'^([1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*\tNone|[1-9][0-9]*\t[1-9][0-9]*\t0\t[1-9][0-9]*|[1-9][0-9]*\t0\t[1-9][0-9]*\t[1-9][0-9]*|0\t[1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*)$' -c
echo -n "NON-INF frames (in FOUR resources): "
cat manocska.txt | grep -v "INF" | cut -d$'\t' -f3,4,5,6 |  egrep $'^[1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*\t[1-9][0-9]*$' -c
