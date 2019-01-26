# Manócska – an integrated verb frame database

_Manócska_ contains all Hungarian verb frame databases, these are as follows:

- [_Hungarian verbal structures (dictionary)_. Bálint Sass et al.](ige_szotar/README.en.md)
- [28 million syntactically parsed sentences and _500000 verbal structures (list)_. Bálint Sass.](isz/README.en.md)
- [_Tádé_ – A frequency list of verb frames. András Kornai et al.](tade/README.en.md)
- [_PrevLex_ – A revised table of particle verbs in Hungarian. Ágnes Kalivoda.](https://github.com/kagnes/prevlex/)
- [_Infinitival constructions in Hungarian_. Ágnes Kalivoda.](https://github.com/kagnes/infinitival_constructions)
- [_The verb frame database of the hungarian-english variant of MetaMorpho_. Gábor Prószéky et al.](MetaMorphoHuEn/README.en.md)

It contains 'verb – verbal particle – argument frame' triplets with their frequencies in the above mentioned resources.

# The structure of the resource

### It consists of the following files:

- manocska.txt: the _Manócska_ database in TSV format (with rows ordered by verb and argument frame)
- manocska.sorted.txt: ordered by rank (this value is computed by dividing the actual frame frequency and the summarized frame frequency for each resource, and finally by summarizing the divisions' results)
- manocska.sorted.nolex.txt: ordered by rank, __without__ frames having a lexically bound argument
- manocska.sorted.lex.txt: ordered by rank, __only__ frames having a lexically bound argument
- manocska.log.txt: information about the merging process and some statistics
- manocska.xml.gz: the _Manócska_ database in XML format

### manocska.txt, manocska.sorted.txt, manocska.sorted.nolex.txt, manocska.sorted.lex.txt:

- every field is separated by Tab
- 1st field: the verb lemma (the verbal particle is separated by pipe, |)
- 2nd field: arguments, separated by space
    - the cases are represented with [_emMorph_-like tags](https://e-magyar.hu/hu/textmodules/emmorph_codelist) ([Poss] stands for every person and number in possessive, 'e' means singular, 't' means plural)
    - the INF_ prefix stands for the infinitival argument
    - = is placed before the postpositions
    - @ means that the verb does not have any arguments
    - ??? can be seen in cases when we don't have any information about the argument frame
    - in case of lexically bound arguments, the word stem is concatenated with the case and/or the postposition
- 3rd field: the frequency of the argument frame, based on the _Hungarian verbal structures (dictionary)_
- 4th field: the frequency of the argument frame, based on the _500000 verbal structures (list)_
- 5th field: the frequency of the argument frame, based on _Tádé_
- 6th field: the frequency of the argument frame (of the particle verbs only), based on _PrevLex_ (in the case of verbs without particle, this field gets a None value)
- 7th field: the frequency of the argument frame by verbs having infinitival arguments, based on _Ágnes Kalivoda's collection_ (Infinitival constructions in Hungarian; in case of verbs without infinitival argument, this field gets a None value)
- 8th field:  the frequency of the argument frame, based on _MetaMorpho_
- 9th field: the rank value

# Creating the resource

In order to facilitate reproducibility, _Manócska_ can be created with the following commands, using the preprocessed formats of the other resources (git clone --recursive ...).
The git repository __does not contain__ the original resources needed for reproduction, __due to their licences__.

    time (python3 merge.py --TSV 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k9,9nr -k1,2 | \
    tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
    cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt

# Licence

_Manócska_ can be used for education, research and private projects. Please refer to __every resource__ used by _Manócska_ according to their authors original request. In every other case, you should keep yourself to the licences set by the resources' creators.

To cite _Manócska_ use one of the following bibliographic entries:

Ágnes Kalivoda, Noémi Vadász, Balázs Indig. _Manócska: A Unified Verb Frame Database for Hungarian._ Proceedings of the 21st International Conference on Text, Speech and Dialogue (TSD 2018). 135--143. Brno 2018.

	@inproceedings{nlp:tsd18conf/pp124-132,
		title={{\textsc  {Manócska}: A Unified Verb Frame Database for Hungarian}},
		booktitle={{Proceedings of the 21st International Conference on Text, Speech and Dialogue---TSD 2018, Brno, Czech Republic}},
		series = {Lecture Notes in Artificial Intelligence},
		volume = 11107,
		year = 2018,
		editor = {Petr Sojka and Ale{\v s} Hor{\'a}k and Ivan Kope{\v c}ek and Karel Pala},
		month = Sep,
		day = {11--14},
		author={{\'A}gnes Kalivoda and No{\'e}mi Vad{\'a}sz and Bal{\'a}zs Indig},
		pages={135--143},
		doi={https://doi.org/10.1007/978-3-030-00794-2_14},
		publisher = {Springer-Verlag},
		isbn =  {978-3-030-00794-2},
	}

Vadász Noémi, Kalivoda Ágnes, Indig Balázs. _Egy egységesített magyar igei vonzatkerettár építése és felhasználása_ XIV. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2018). 3--15. Szeged. 2018.

    @inproceedings{vadasz_kalivoda_indig_2018a,
        title = {Egy egys{\'e}ges{\'i}tett magyar igei vonzatkerett{\'a}r {\'e}p{\'i}t{\'e}se {\'e}s felhaszn{\'a}l{\'a}sa},
        booktitle = {XIV. Magyar Sz{\'a}m{\'i}t{\'o}g{\'e}pes Nyelv{\'e}szeti Konferencia (MSZNY 2018)},
        year = {2018},
        pages = {3{\textendash}15},
        publisher={Szegedi Tudom{\'a}nyegyetem Informatikai Tansz{\'e}kcsoport},
        organization = {Szegedi Tudom{\'a}nyegyetem Informatikai Int{\'e}zet},
        address = {Szeged},
        author = {Vad{\'a}sz, No{\'e}mi and Kalivoda, {\'A}gnes and Indig, Bal{\'a}zs},
        editor = {Vincze, Veronika}
    }

The bibliographical data needed for citing the other resources can be found on the links presented at the top of this page.

