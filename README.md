# Manócska – integrált igei vonzatkeret adatbázis

A _Manócska_ adatbázis összefogja és harmonizálja a szabadon elérhető magyarnyelvű igei vonzatkeret adatbázisokat és az igékről elérhető információkat melyek a következők:

- [_Magyar igei szerkezetek (szótár)_. Sass Bálint et al.](ige_szotar/README.md)
- [28 millió szintaktikailag elemzett mondat és _500000 igei szerkezet (lista)_. Sass Bálint.](isz/README.md)
- [_Tádé_ – Igei vonzatkeret-gyakorisági lista. Kornai András et al.](tade/README.md)
- [_A magyar igei komplexumok vizsgálata. Kalivoda Ágnes_. (Mesterszakos szakdolgozat)](https://github.com/kagnes/hungarian_verbal_complex/)

Tartalmazza az összes ige-igekötő-keret hármast a fenti erőforrásokból származó gyakoriságokkal.

# Az erőforrás szerkezete

### Az erőforrás a kövektező fájlokból áll:

- manocska.txt: ige és keret szerint rendezve
- manocska.sorted.txt: rang szerint rendezve
- manocska.sorted.nolex.txt: rang szerint rendezve, a lexikálisan kötött argumentumot tartalmazó keretek __kihagyva__
- manocska.sorted.lex.txt: rang szerint rendezve, __csak__ a lexikálisan kötött argumentumot tartalmazó keretek
- manocska.log.txt: információk az összevonásról


### manocska.txt, manocska.sorted.txt, manocska.sorted.nolex.txt, manocska.sorted.lex.txt:

- Midnen mező Tab-bal van elválasztva.
- Első mező az ige (igekötő |-al van elválasztva)
- Második mező az argumentumok szóközzel elválasztva
    - az esetek [Humor kódban](http://www.morphologic.hu/downloads/publications/na/2006_mszny_jobbhumor_na-pt.pdf) vannak megadva (a [PSe3] minden személyű birtokost egységesen jelöl)
    - INF_ prefixummal az infinitív argumentumok
    - = jellel prefixálva a névutók
    - @ jelzi ha nincs argumentum
    - A lexikálisan kötött elemek szótöve és az eset illetve névutó közvetlenül kapcsolódik
- Harmadik mező a keret frekvenciája a _Magyar igei szerkezetek (szótár)_ alapján
- Negyedik mező a keret frekvenciája a _500000 igei szerkezet (lista)_ alpján
- Ötödik mező a keret frekvenciája a _Tádé_ alapján
- Hatoik mező az (igekötős)ige frekvenciája _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ alapján (nem igekötős igékre nulla, minden keretre azonos)
- Hetedik mező a "rang": sum (adatbázisonként a keret előfordulásának és az összes keret előfordulásának hányadosa)


### merge.log.txt:

- Az igék száma az egyes adatbázisokban
- Aztán az egyes igékhez a közös keretek száma (ahol volt ilyen):
    - Mezőelválasztó Tab karakter
    - A keretek listái Python jelölésben vannak
    - Első mező az ige
    - Második mező a _Magyar igei szerkezetek (szótár)_ és a 500000 igei szerkezet című lista közös keretei az adott igéhez
    - Harmadik mező a _500000 igei szerkezet (lista)_ és a _Tádé_ közös keretei az adott igéhez
    - Negyedik mező a _Tádé_ és a _Magyar igei szerkezetek (szótár)_ közös keretei az adott igéhez
    - Ötödik mező az ige _Kalivoda Ágnes Magyar igei komplexum vizsgálatai_ szerinti frekvenciája

# Az erőforrás előállítása

A reprodukálhatóságot könnyítendő az alábbi parancsok segítségével a Manócska előállítható a többi erőforrás előfeldolgozott formátumainak felhasználásval. (git clone --recursive ...)

    time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k6,6g | \
    tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt)
    cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt


# Licensz

Felhasználható oktatási, kutatási és magáncélra. Ez esetben __az összes a _Manócska_ által felhasznált erőforrást hivatkozni kell__.
Továbbiakban a Manócska készítése során felhasznált erőforrások jogtulajdonosainak álláspontja a mértékadó.
