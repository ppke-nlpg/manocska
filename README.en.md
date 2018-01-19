# Manócska – an integrated verb frame database

_Manócska_ contains all open-source Hungarian verb frame databases, these are as follows:

- [_Hungarian verbal structures (dictionary)_. Bálint Sass et al.](ige_szotar/README.en.md)
- [28 million syntactically parsed sentences and _500000 verbal structures (list)_. Bálint Sass.](isz/README.en.md)
- [_Tádé_ – A frequency list of verb frames. András Kornai et al.](tade/README.en.md)
- [_A frequency list of verb frames_. Ágnes Kalivoda. (MA thesis)](https://github.com/kagnes/hungarian_verbal_complex/)
- [_Infinitival constructions in Hungarian_. Ágnes Kalivoda.](https://github.com/kagnes/infinitival_constructions)

It contains 'verb – verbal particle – argument frame' triplets with their frequencies in the above mentioned resources.

# The structure of the resource

### It consists of the following files:

- manocska.txt: ordered by verb and argument frame
- manocska.sorted.txt: ordered by rank (this value is computed by dividing the actual frame frequency and the summarized frame frequency for each resource, and finally by summarizing the divisions' results)
- manocska.sorted.nolex.txt: ordered by rank, __without__ frames having a lexically bound argument
- manocska.sorted.lex.txt: ordered by rank, __only__ frames having a lexically bound argument
- manocska.log.txt: information about the merging process


### manocska.txt, manocska.sorted.txt, manocska.sorted.nolex.txt, manocska.sorted.lex.txt:

- every field is separated by Tab
- 1st field: the verb lemma (the verbal particle is separated by pipe, |)
- 2nd field: arguments, separated by space
    - the cases are represented with [Humor tags](http://www.morphologic.hu/downloads/publications/na/2006_mszny_jobbhumor_na-pt.pdf) ([PSe3] stands for every person and number in possessive, 'e' means singular, 't' means plural)
    - the INF_ prefix stands for the infinitival argument
    - = is placed before the postpositions
    - @ means that the verb does not have any arguments
    - in case of lexically bound arguments, the word stem is concatenated with the case and/or the postposition
- 3rd field: the frequency of the argument frame, based on the _Hungarian verbal structures (dictionary)_
- 4th field: the frequency of the argument frame, based on the _500000 verbal structures (list)_
- 5th field: the frequency of the argument frame, based on _Tádé_
- 6th field: the frequency of the argument frame (of the particle verbs only), based on _Ágnes Kalivoda's MA thesis_ (in the case of verbs without particle, this field gets a None value)
- 7th field: the frequency of the argument frame by verbs having infinitival arguments, based on _Ágnes Kalivoda's collection_ (Infinitival constructions in Hungarian; in case of verbs without infinitival argument, this field gets a None value)
- 8th field: the rank value


### merge.log.txt:

- number of verbs in each resources
- after that, the common frames (meaning that two or more resources agree on the frame), by each verb:
    - Field separator: newline character (\n), Record separator: double newline (\n\n)
    - The lists of the frames are represented in Python-style
    - 1st field: the verb lemma
    - 2nd field: common frames coming from the _Hungarian verbal structures (dictionary)_ and the _500000 verbal structures (list)_, in case of the given verb
    - 3rd field: common frames coming from the _500000 verbal structures (list)_ and _Tádé_, in case of the given verb
    - 4th field: common frames coming from _Tádé_ and the _Hungarian verbal structures (dictionary)_, in case of the given verb
    - 5th field: the frequency of the verb, according to _Ágnes Kalivoda's MA thesis_

# Creating the resource

In order to facilitate reproducability, _Manócska_ can be created with the following commands, using the preprocessed formats of the other resources (git clone --recursive ...).
The git repository __does not contain__ the original resources needed for reproduction, __due to their licences__.

    time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k10,10nr -k1,2 | \
    tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
    cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt


# Licence

_Manócska_ can be used for education, research and private projects. Please refer to __every resource__ used by _Manócska_. In every other case, you should keep yourself to the licences set by the resources' creators.

To cite _Manócska_ use one of the following bibliographic entries:

Balázs Indig, Noémi Vadász, Ágnes Kalivoda. _Manócska – an integrated verb frame database._ (2017) Available at: [https://github.com/ppke-nlpg/manocska](https://github.com/ppke-nlpg/manocska)

    @manual{manocska,
      author       = {Indig, Bal{\'a}zs and Vad{\'a}sz, No{\'e}mi and Kalivoda, {\'A}gnes},
      title        = {Man{\'o}cska -- integr{\'a}lt igeivonzatkeret-adatb{\'a}zis},
      year         = {2017},
      url = {https://github.com/ppke-nlpg/manocska}
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

