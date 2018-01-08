# Manócska – integrált igei vonzatkeret adatbázis

A _Manócska_ adatbázis összefogja és harmonizálja a szabadon elérhető magyar nyelvű igei vonzatkeret adatbázisokat és az igékről elérhető információkat, melyek a következők:

- [_Magyar igei szerkezetek (szótár)_. Sass Bálint et al.](ige_szotar/README.md)
- [28 millió szintaktikailag elemzett mondat és _500000 igei szerkezet (lista)_. Sass Bálint.](isz/README.md)
- [_Tádé_ – Igei vonzatkeret-gyakorisági lista. Kornai András et al.](tade/README.md)
- [_A magyar igei komplexumok vizsgálata_. Kalivoda Ágnes. (Mesterszakos szakdolgozat)](https://github.com/kagnes/hungarian_verbal_complex/)
- [_Infinitívuszi szerkezetek a magyarban_. Kalivoda Ágnes.](https://github.com/kagnes/infinitival_constructions)

Tartalmazza az összes ige-igekötő-vonzatkeret hármast a fenti erőforrásokból származó gyakoriságokkal.

# Az erőforrás szerkezete

### Az erőforrás a következő fájlokból áll:

- manocska.txt: ige és keret szerint rendezve
- manocska.sorted.txt: rang szerint rendezve (ez adatbázisonként a keret előfordulásának és az összes keret előfordulásának hányadosa)
- manocska.sorted.nolex.txt: rang szerint rendezve, a lexikálisan kötött argumentumot tartalmazó keretek __kihagyva__
- manocska.sorted.lex.txt: rang szerint rendezve, __csak__ a lexikálisan kötött argumentumot tartalmazó keretek
- manocska.log.txt: információk az összevonásról


### manocska.txt, manocska.sorted.txt, manocska.sorted.nolex.txt, manocska.sorted.lex.txt:

- Minden mező Tab-bal van elválasztva
- Első mező: az ige (igekötő |-al van elválasztva)
- Második mező: az argumentumok szóközzel elválasztva
    - az esetek [Humor kódban](http://www.morphologic.hu/downloads/publications/na/2006_mszny_jobbhumor_na-pt.pdf) vannak megadva (a [PSe3] minden személyű birtokost egységesen jelöl)
    - INF_ prefixummal az infinitív argumentumok
    - = jellel prefixálva a névutók
    - @ jelzi, ha nincs argumentum
    - A lexikálisan kötött elemek szótöve és az eset illetve névutó közvetlenül kapcsolódik
- Harmadik mező: a keret frekvenciája a _Magyar igei szerkezetek (szótár)_ alapján
- Negyedik mező: a keret frekvenciája a _500000 igei szerkezet (lista)_ alapján
- Ötödik mező: a keret frekvenciája a _Tádé_ alapján
- Hatodik mező: az (igekötős)ige frekvenciája _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ alapján (nem igekötős igékre None, minden keretre azonos)
- Hedetik mező az infinitívuszos ige az infinitívusz igekötőjével összekapcsolt frekvenciája _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ alapján (nem igekötős infinitívuszra és nem infinitívuszos igére None, minden keretre azonos)
- Nyolcadik mező az infinitívuszos ige igekötőjének és az infinitívusznak az összekapcsolt frekvenciája _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ alapján (nem igekötős igére és nem infinitívuszos igére None, minden keretre azonos)
- Kilencedik mező az infinitívuszos ige igekötős infintívuszának frekvenciája _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ alapján (nem igekötős infinitívuszra és nem infinitívuszos igére None, minden keretre azonos)
- Tizetdik mező a "rang": sum (adatbázisonként a keret előfordulásának és az összes keret előfordulásának hányadosa)


### merge.log.txt:

- Az igék száma az egyes adatbázisokban
- Aztán az egyes igékhez a közös keretek száma (ahol volt ilyen):
    - Mezőelválasztó: soremelés karakter (\n), rekordelválasztó: dupla soremelés karakter (\n\n)
    - A keretek listái Python jelölésben vannak
    - Első mező az ige
    - Második mező a _Magyar igei szerkezetek (szótár)_ és a 500000 igei szerkezet című lista közös keretei az adott igéhez
    - Harmadik mező a _500000 igei szerkezet (lista)_ és a _Tádé_ közös keretei az adott igéhez
    - Negyedik mező a _Tádé_ és a _Magyar igei szerkezetek (szótár)_ közös keretei az adott igéhez
    - Ötödik mező az ige _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ szerinti frekvenciája

# Az erőforrás előállítása

A reprodukálhatóságot könnyítendő az alábbi parancsok segítségével a Manócska előállítható a többi erőforrás előfeldolgozott formátumainak felhasználásval. (git clone --recursive ...)
A git repozitórium __nem tartalmazza az eredeti erőforrásokat__ melyek szükségesek a reprodukcióhoz __azok licensze miatt__.

    time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k10,10nr -k1,2 | \
    tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
    cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt


# Licensz

Felhasználható oktatási, kutatási és magáncélra. Ez esetben __az összes, a _Manócska_ által felhasznált erőforrást hivatkozni kell__.
Továbbiakban a Manócska készítése során felhasznált erőforrások jogtulajdonosainak álláspontja a mértékadó.

Indig Balázs. _Manócska – integrált igei vonzatkeret adatbázis._ (2017) Elérhető: [https://github.com/ppke-nlpg/manocska](https://github.com/ppke-nlpg/manocska)

    @manual{manocska,
      author       = {Indig, Bal{\'a}zs},
      title        = {Man{\'o}cska -- integr{\'a}lt igeivonzatkeret-adatb{\'a}zis},
      year         = {2017},
      url = {https://github.com/ppke-nlpg/manocska}
    }

A többi erőforrás hivatkozásához szükséges bibliográfiai adatokat lásd a fenti linkeken.
