#### [Click here for English readme!](https://github.com/ppke-nlpg/manocska/blob/master/README.en.md)

# Manócska – integrált igei vonzatkeret adatbázis

A _Manócska_ adatbázis összefogja és harmonizálja a magyar nyelvű igei vonzatkeret adatbázisokat és az igékről elérhető információkat, melyek a következők:

- [_Magyar igei szerkezetek (szótár)_. Sass Bálint et al.](ige_szotar/README.md)
- [28 millió szintaktikailag elemzett mondat és _500000 igei szerkezet (lista)_. Sass Bálint.](isz/README.md)
- [_Tádé_ – Igei vonzatkeret-gyakorisági lista. Kornai András et al.](tade/README.md)
- [_A magyar igei komplexumok vizsgálata_. Kalivoda Ágnes. (Mesterszakos szakdolgozat)](https://github.com/kagnes/hungarian_verbal_complex/)
- [_Infinitívuszi szerkezetek a magyarban_. Kalivoda Ágnes.](https://github.com/kagnes/infinitival_constructions)
- [_A MetaMorpho igei vonzatkeret adatbázisa_. Prószéky Gábor et al.](MetaMorphoHuEn/README.md)

Tartalmazza az összes ige-igekötő-vonzatkeret hármast a fenti erőforrásokból származó gyakoriságokkal.

# Az erőforrás szerkezete

### Az erőforrás a következő fájlokból áll:

- manocska.txt: a _Manócska_ adatbázis TSV formátumban (a sorok ige és keret szerint rendezve)
- manocska.sorted.txt: rang szerint rendezve (ez adatbázisonként a keret előfordulásának és az összes keret előfordulásának hányadosa)
- manocska.sorted.nolex.txt: rang szerint rendezve, a lexikálisan kötött argumentumot tartalmazó keretek __kihagyva__
- manocska.sorted.lex.txt: rang szerint rendezve, __csak__ a lexikálisan kötött argumentumot tartalmazó keretek
- manocska.log.txt: információk az összevonásról és néhány statisztika
- manocska.xml.gz: a _Manócska_ adatbázis XML formátumban

### manocska.txt, manocska.sorted.txt, manocska.sorted.nolex.txt, manocska.sorted.lex.txt:

- Minden mező Tab-bal van elválasztva
- Első mező: az ige (igekötő |-al van elválasztva)
- Második mező: az argumentumok szóközzel elválasztva
    - az esetek [Humor kódban](http://www.morphologic.hu/downloads/publications/na/2006_mszny_jobbhumor_na-pt.pdf) vannak megadva (a [PSe3] minden személyű birtokost egységesen jelöl)
    - INF_ prefixummal az infinitív argumentumok
    - = jellel prefixálva a névutók
    - @ jelzi, ha nincs argumentum
    - ??? olyan esetekben szerepel, amikor nincs információnk a vonzatkeretről
    - a lexikálisan kötött elemek szótöve és az eset illetve névutó közvetlenül kapcsolódik
- Harmadik mező: a keret frekvenciája a _Magyar igei szerkezetek (szótár)_ alapján
- Negyedik mező: a keret frekvenciája a _500000 igei szerkezet (lista)_ alapján
- Ötödik mező: a keret frekvenciája a _Tádé_ alapján
- Hatodik mező: az (igekötős)ige frekvenciája _Kalivoda Ágnes Infinitívuszi szerkezetek a magyarban_ vizsgálata alapján (nem igekötős igékre None, minden keretre azonos)
- Hetedik mező: az infinitívuszi vonzattal rendelkező igék frekvenciája _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ alapján (infinitívuszi vonzattal nem rendelkező igékre None, minden keretre azonos)
- Nyolcadik mező: a keret frekvenciája a _MetaMorpho_ alapján
- Kilencedik mező: a rang

# Az erőforrás előállítása

A reprodukálhatóságot könnyítendő a _Manócska_ előállítható a többi erőforrás előfeldolgozott formátumainak felhasználásával, az alábbi parancsok segítségével (git clone --recursive ...).
A git repozitórium __nem tartalmazza az eredeti erőforrásokat__, melyek szükségesek a reprodukcióhoz, __azok licensze miatt__.

    time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k10,10nr -k1,2 | \
    tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
    cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt


# Licensz

Felhasználható oktatási, kutatási és magáncélra. Ez esetben __a _Manócska_ által felhasznált összes erőforrást hivatkozni kell__.
Továbbiakban a Manócska készítése során felhasznált erőforrások jogtulajdonosainak álláspontja a mértékadó.

A _Manócska_ a következő bibliográfiai bejegyzések egyikével hivatkozható:

Indig Balázs, Vadász Noémi, Kalivoda Ágnes . _Manócska – integrált igei vonzatkeret adatbázis._ (2017) Elérhető: [https://github.com/ppke-nlpg/manocska](https://github.com/ppke-nlpg/manocska)

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

A többi erőforrás hivatkozásához szükséges bibliográfiai adatokat lásd a fenti linkeken.

