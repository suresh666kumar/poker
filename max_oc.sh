
for i in {1..13}
do
    for j in {1..13}
    do
        if [ $i != $j ]
        then
            c1=$i
            c2=$j
            if [ $i == 1 ]
            then
                c1='A'
            fi
            if [ $i == 11 ]
            then
                c1='J'
            fi
            if [ $i == 12 ]
            then
                c1='Q'
            fi
            if [ $i == 13 ]
            then
                c1='K'
            fi

            if [ $j == 1 ]
            then
                c2='A'
            fi
            if [ $j == 11 ]
            then
                c2='J'
            fi
            if [ $j == 12 ]
            then
                c2='Q'
            fi
            if [ $j == 13 ]
            then
                c2='K'
            fi

            x=`../twocards.sh $c1 $c2 | wc -l`
            printf "%2d:\t$c1 & $c2\n" $x

        fi
    done
done
