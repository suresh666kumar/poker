FN=`ls poker_now_log_*.csv`

../..//analyse-poker.py $FN
echo

echo "Bottom 20% aka Garbage List"
../..//gc.py $FN 120 | sort
#../gc.py $FN | egrep -v "SB|BB" | sort
echo

echo "Pocket Pairs"
../..//pocket_pair.sh | sort
echo
