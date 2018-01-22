# VFrame szótár
A _Manócska_ adatbázist használja a _VFrame_ vonzatkeret-egyértelműsítő eljárás, amely arra szolgál, hogy az ige lehetséges vonzatkereteinek számát csökkentse az igéhez tartozó igekötő és/vagy infinitívuszi vonzat segítségével. A *vframe_dict_generator.py* script három kimenetet generál a _Manócskából_, ezek:

- a szótárnak egy "emberi szemmel" könnyebben olvasható verziója (*vframe_to_read*)
- a _VFrame_ keresőeljárás bemenete (*vframe_to_eval*)
- az _AnaGramma_ elemző bemenete (*vframe_dict.py*)

További információ a _VFrame_ git repozitóriumban érthető el: [https://github.com/ppke-nlpg/vframe](https://github.com/ppke-nlpg/vframe) 

# Licensz
Felhasználható oktatási, kutatási és magáncélra. A _VFrame_ a következő bibliográfiai bejegyzések valamelyikével hivatkozható:

Vadász Noémi, Kalivoda Ágnes, Indig Balázs. _Egy egységesített magyar igei vonzatkerettár építése és felhasználása._ XIV. Magyar Számítógépes Nyelvészeti Konferencia (MSZNY 2018). 3--15. Szeged. 2018.

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

Indig, Balázs and Vadász, Noémi. _Windows in Human Parsing -- How Far can a Preverb Go?_ Tenth International Conference on Natural Language Processing (HrTAL2016), Dubrovnik, Croatia, September 29--30, 2016.

    @conference {indig_vadasz_2016b,
        title = {Windows in Human Parsing {\textendash} How Far can a Preverb Go?},
        booktitle = {Tenth International Conference on Natural Language Processing (HrTAL2016) 2016, Dubrovnik, Croatia, September 29-30, 2016, Proceedings},
        year = {2016},
        note = {to appear},
        publisher = {Springer},
        organization = {Springer},
        address = {Cham},
        keywords = {indba, vadno},
        author = {Indig, Bal{\'a}zs and Vad{\'a}sz, No{\'e}mi},
        editor = {Tadi{\'c}, Marko and Bekavac, Bo{\.z}o}
    }
