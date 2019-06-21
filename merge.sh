rm resources.pckl.gz
time (python3 merge.py --TSV 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k9,9nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
time (python3 merge.py --XML --read-pickle | pigz -c > manocska.xml.gz)
time (python3 merge.py --gen-patterns --read-pickle)
