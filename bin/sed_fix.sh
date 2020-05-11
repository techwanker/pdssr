for f in *.py; 
do     
    sed -i "s/util/pdsutil/" $f 
done
