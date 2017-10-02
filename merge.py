#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from collections import defaultdict, Counter

"""
These verbs never occur with verbal particle.
All occurence with verbal particle should be corrected to the sole verb.
dekete verbal particle
"""
never_prev_verbs = {'akar', 'kell', 'óhajt', 'szabad', 'szándékozik'}

"""
Ezek az igék csak a listában szereplő igekötőkkel mennek együtt minden más rossz.
midnen más igekötő igekötőtlenné teendő
ez a file: light_verb_exceptions.txt
"""
light_verb_exception_verbs = {'bír', 'fog', 'kezd', 'kíván', 'mer', 'szeret', 'szokik', 'talál', 'tetszik',
                              'tud', 'van', 'lesz', 'lehet', 'nincs', 'sincs'}

with open('light_verbs/light_verb_exceptions.txt', encoding='UTF-8') as lve:
    light_verb_exception_verbs_w_prev = {line.replace('+', '|') for line in lve.readlines()}

# TODO: ezt mergelni: jo_inf_lista.txt
"""
Először merge aztán "manócskajavítás"
Az összes perjelest kiválogatni.
"""

"""
Incorrect verbal particle splitting
and
Occur splitted and not splitted but only the NOT splitted is OK.
splitted -> unsplitted
"""
not_prev_verbs = {'alá|z', 'át|all', 'bele|s', 'bele|z', 'elé|g', 'elé|r', 'elő|z', 'fel|el',
                  'le|l', 'le|p', 'le|s', 'le|sz', 'rá|g', 'rá|z', 'tele|l', 'teli|k', }

not_prev_verbs2 = {'fel|esel', 'szembe|sül', 'észre|vételez', 'mellé|kel', 'ellen|őriz', 'ki|vitelez',
                   'ellen|súlyoz', 'fel|ejt', 'ki|abál', 'ki|fogásol', 'be|folyásol', 'szemre|hány', 'szemre|vételez',
                   'nagyot|hall', 'bé|küld', 'bé|lel', 'be|cserkel', 'bé|kél', 'ki|józanul'}

"""
Good verbs, that have false verbal particle analysis
SHOULD NOT BE splitted!
noop
"""
false_prev_good = {'felesel', 'felvételizik', 'kiabál', 'mellékel', 'szembesül', 'túlórázik'}

"""
with hyphen funny ik need to replaced
replace funny ik
"""
funny_ik_replacements = {'ad--veszik': 'ad--vesz', 'lát--hallik': 'lát-hall', 'tel--múl': 'telik--múlik',
                         'törik--zúz': 'tör--zúz'}

"""
good verbs, that Humor has not recognised.
We do not do anything with them. Mostly due to the hyphen (--) and strange verbal particle
noop
"""
good_verbs_humor_not_recognised = {'ad--kap', 'ad--vesz', 'csetlik--botlik', 'csűr--csavar', 'él--hal',
                                   'eszik--iszik', 'hány--vet', 'hoz--visz', 'húz--halaszt', 'ír--olvas',
                                   'jár--kel', 'jön--megy', 'lát--hall', 'lót--fut', 'recseg--ropog',
                                   'sürög--forog', 'süt--főz', 'térül--fordul', 'tesz--vesz', 'tör--zúz', 'üt--ver'}

good_verbs_humor_not_recognised2 = {'bent|ragad', 'cserben|hagy', 'élen|jár', 'el|enyész', 'helyben|hagy', 'helyt|áll',
                                    'karban|tart', 'kétségbe|esik',
                                    'közben|jár', 'kinn|felejt', 'meg|vagyon', 'odébb|áll',
                                    'rendre|utasít', 'síkra|száll', 'szörnyet|hal',
                                    'útba|igazít', 'ki|horgász', 'kétségbe|von', 'pofon|vág', 'számba|vesz',
                                    'számon|kér', 'számon|tart', 'útba|ejt',
                                    'békén|hagy', 'elé|vesz', 'földet|ér', 'helyt|ad', 'dupla_ik|hagy', 'meg|hány--vet',
                                    'pórul|jár', 'zokon|vesz',
                                    'hatályosul'
                                    }

good_verbs_humor_not_recognised3 = {'jelent|jelentet', 'jön|jő', 'békén|hagy', 'vet|vetet', 'bent|jár',
                                    'bicsakol', 'csökkent|csökkentet', 'döglik|dögöl', 'ébreszt|ébresztet',
                                    'edz|edzet', 'ejt|ejtet', 'fejt|fejtet', 'felejt|felejtet', 'hí|hív', 'jön|jő',
                                    'ment|mentet', 'vérezik|vérzik', 'veszt|vesztet', 'emlékezik|emlékszik',
                                    'ereszt|eresztet', 'érez|érzik', 'érint|érintet', 'ért|értet',
                                    'fejleszt|fejlesztet', 'fejt|fejtet', 'felejt|felejtet', 'hí|hív',
                                    'jelent|jelentet', 'jön|jő', 'kelt|keltet', 'ment|mentet', 'ért|értet',
                                    'feltételez', 'félt|féltet', 'vet|vetet', 'fest|festet', 'gerjeszt|gerjesztet',
                                    'habozik|habzik', 'hajlik|hajol', 'hangozik|hangzik', 'jön|jő',
                                    'hiányozik|hiányzik', 'hí|hív', 'illet|illik', 'int|intet', 'jelent|jelentet',
                                    'jól|esik', 'jön|jő', 'kell|kelletik', 'kelt|keltet', 'kétségbe|esik', 'ejt|ejtet',
                                    'fejleszt|fejlesztet', 'fejt|fejtet', 'felejt|felejtet', 'jelent|jelentet',
                                    'jön|jő', 'betegedik|betegszik', 'hajlik|hajol', 'int|intet', 'jön|jő',
                                    'törleszt|törlesztet', 'vet|vetet', 'ért|értet', 'hí|hív', 'lesz|van',
                                    'ment|mentet', 'teremt|teremtet', 'vet|vetet', 'melegedik|melegszik',
                                    'mellékel', 'ment|mentet', 'jön|jő', 'jön|jő', 'rogyaszt', 'rosszul|esik',
                                    'sejt|sejtet', 'sért|sértet', 'síkra|száll', 'szembesül', 'szerkeszt|szerkesztet',
                                    'talizik', 'tekint|tekintet', 'teremt|teremtet', 'terjeszt|terjesztet',
                                    'tetszet|tetszik', 'veszik|veszt', 'veszt|vesztet', 'vet|vetet', 'jön|jő',
                                    'bé|lát'
                                    }


"""
Prev and verb do not go together
and
strange combinations
delete
"""
# TODO: further research (delete)
not_prev_verbs_TODO_FR = {'jól|esik', 'jól|lakat', 'jól|lakik', 'jól|tart', 'jót|áll', 'rosszul|esik', 'után|állít',
                          'után|ízesít', 'után|nyom', 'után|rendel', 'után|tölt'}

# TODO: Research written together of separately?
verb_bad_prev = {'-be|jár', 'bé|késik',  'egyet|ér', 'el|fogul', 'helyt|van', 'jól|érez', 'kétségbe|rohan',
                 'kétségbe|van', 'kölcsön|lehet', 'kölcsön|szól', 'közzé|tetszik', 'létre|szenderedik',
                 'szörnyet|uszít', 'számba|megy', 'pofon|érkezik'
                 'abba|kerül', 'abba|van', 'egyet|alszik', 'egyet|említ', 'egyet|gondol', 'egyet|húz', 'egyet|jelent',
                 'egyet|kér', 'egyet|lát', 'egyet|lép', 'egyet|mond', 'egyet|nyel', 'egyet|nyom', 'egyet|sóhajt',
                 'egyet|szeret', 'egyet|talál', 'egyet|tud', 'egyet|választ', 'egyet|vesz', 'együtt|csinál',
                 'együtt|dolgozik', 'együtt|él', 'együtt|érez', 'együtt|jár', 'együtt|játszik',
                 'együtt|rögzít', 'együtt|szerkeszt', 'együtt|tölt', 'együtt|van', 'földet|kap', 'helyben|biztosít',
                 'helyben|használ', 'helyben|marad', 'helyben|van', 'helyt|kap', 'jót|akar', 'jót|ígér', 'jót|ír',
                 'jót|kíván', 'jót|mond', 'jót|tesz', 'nagyot|alkot', 'nagyot|csalódik', 'nagyot|dobban',
                 'nagyot|fordul', 'nagyot|kacag', 'nagyot|nevet', 'nagyot|néz', 'nagyot|nyel', 'nagyot|sóhajt',
                 'nagyot|téved', 'nagyot|változik', 'szabadjára|enged',
                 'szabadlábra|helyez', 'szemügyre|vesz',
                 'torkig|van', 'tudomásul|vesz',
                 'óva|int', 'együtt|dolgoz', 'közre|játsz'}

"""
With the second verbal particle they are OK.
delete verbal particle (first)
"""
double_prev_verbs = {'abba|bele|megy', 'abba|bele|nyugodik', 'abba|bele|törődik', 'át|el|jut', 'el|meg|említ',
                     'el|meg|jegyez', 'haza|el|megy', 'hozzá|oda|megy', 'ide|be|hoz', 'ide|be|ír', 'ide|be|jön',
                     'ide|be|lép', 'ide|be|néz', 'ide|be|tesz', 'ide|el|jön', 'ide|el|jut', 'ide|ki|jön', 'ki|meg|mond',
                     'meg|el|ad', 'meg|el|ér', 'meg|el|érik', 'meg|el|fogad', 'meg|el|megy', 'meg|el|mond',
                     'meg|el|olvas', 'meg|le|ír', 'meg|meg|jelenik', 'meg|meg|néz', 'meg|meg|tesz', 'meg|meg|van',
                     'oda|be|megy', 'oda|el|jut', 'oda|el|megy', 'oda|vissza|tér', 'rá|meg|van', 'abba|bele|egyez'}

not_rev_verbs_drop_prev = {'földet|őriz', 'helyt|őriz', 'helyt|rendez',
                           'egyet|enged', 'egyet|sikerül', 'egyet|tart', 'földet|hagy', 'földet|igyekezik',
                           'földet|sikerül', 'helyben|igyekezik', 'helyben|sikerül', 'helyben|tervez', 'jól|eszik',
                           'jól|öltözik', 'jót|hívat', 'kölcsön|sikerül', 'nagyot|segít', 'nagyot|sikerül',
                           'rendre|próbál', 'számba|sikerül'
                           }


"""
Occur splitted and not splitted but both wrong.
Stemming error with strange verbal particle
and
wrong verbs: stemming error
delete
"""
wrong_verbs = {'megfájul', 'meg|fájul', 'elbúcsu', 'el|búcsu', 'behu', 'be|hu', 'meghó', 'meg|hó',
               'át|aluik', 'bele|tet', 'ide|irogat', 'ki|listá', 'le|fek', 'le|kép',
               'le|porolik', 'meg|beszel', 'meg|különb', 'meg|négy', 'meg|nyugod',
               'utána|végrehajt', 'vissza|elindul', 'el|kötelezet', 'meg|fürödik', '(x-y)(y-z)(z-x)=x|y|?NOUN[ACT]'
               }

wrong_verbs2 = {'ajánlat', 'al', 'alat', 'alázat', 'áldozat', 'asztat', 'bí', 'elhangozik', 'füröd',
                'alud', 'es', 'nyugod', 'bíztat{ORTH:substandard}', 'cselekedet', 'dolgozat', 'elégedet', 'élvezet',
                'emlékezet', 'fedezet', 'fejezet', 'fek', 'gyalázat', 'gyülekezet', 'hálózat', 'határozat', 'fürödik',
                'bűzöl', 'hírhed', 'idézet', 'igyekezet', 'jár--kelt', 'jutat', 'kereset', 'kétel', 'hivat', 'irogat',
                'bíztat', 'kockázat', 'korlatoz', 'köll', 'környezet', 'kötelezet', 'kötet', 'közalkalmaz', 'kultúrál',
                'kuporg', 'letet', 'magyarázat', 'normál', 'nyilatkozat', 'nyug', 'oszolik',
                'pályázat', 'romol', 'sarkallik', 'seregel', 'sorozat', 'szavazat', 'szégyenel', 'szeretet',
                'szervezet', 'szövetkezet', 'születet', 'táblázat', 'tagozat', 'tervezet',
                'ugor', 'vadászat', 'változat', 'van--van', 'veszélyeztetet', 'vigyázat', 'fokozat', 'el|jutat'}

wrong_verbs3 = {'benézik', 'érdekképvis', 'észre|ve', 'fel|éte', 'hal|hallik', 'ihlet|ihlik', 'készt|késztet', 'lessz',
                'liz', 'lizik', 'ihlet|ihlik', 'méltó', 'méltö', 'nagyméltó', 'sokal', 'tellik', 'véghez', 'vérá',
                'viszszahú'}


"""
Occur splitted and not splitted but only the splitted is OK.
and
Occur not splitted but only the splitted is OK.
unsplitted -> splitted
"""
not_prev_verbs3 = \
    {elem.replace('|', ''): elem for elem in
     {'el|trafál', 'ki|támogat', 'meg|tapaszt', 'el|ügyetlenkedik', 'meg|sínyli', 'le|ölet', 'össze|vét',
     'közre|ad', 'el|biceg', 'le|puffant', 'végre|hajt', 'tovább|passzol', 'ki|folyat', 'át|böngész',
      'be|huppan', 'alá|néz', 'meg-meg|áll', 'haza|száll', 'be|csempész', 'le|cikiz', 'össze|fecseg',
      'ki|tetet', 'ketté|harap', 'rá|ró', 'fel|csenget', 'be|tetéz', 'el|hull', 'fölül|múl', 'be|boltoz',
      'fel|fakaszt', 'ki|rothad', 'be|fuccsol', 'oda|lát', 'bele|segít', 'el|tángál', 'össze|dolgoz',
      'meg|honosul', 'át|pattan', 'ide|tart', 'el|süpped', 'át|hangzik', 'be|harangoz', 'be|szüremlik',
      'le|firkant', 'ki|rittyent', 'össze|esket', 'össze|szedelődzködik', 'végre|hajtat', 'fel|rikkant',
      'le|csöndesít', 'ki|stafíroz', 'le|táboroz', 'ki|hímez', 'meg|keserül', 'be|tetőz', 'el|fészkelődik',
      'el|csesz', 'elő|kiált', 'végig|pásztáz', 'el|happol', 'vissza|nevet', 'le|ömlik', 'ki|hasad',
      'el|náspángol', 'be|gyűrűz', 'elő|csúszik', 'be|cikkelyez', 'le|ragyog', 'össze|veszít',
      'meg|mukkan', 'le|hasít', 'vissza-vissza|tér', 'le|kenyerez', 'be|spriccel', 'el|nyújtózkodik',
      'utána|bámul', 'ki|zúdul', 'meg|hordoz', 'el|dolgoz', 'ki|fürkész', 'közre|működik', 'meg|szoktat',
      'haza|kívánkozik', 'el|fűrészel', 'meg|tágít', 'ki|járat', 'meg|dolgoz', 'el|szóródik',
      'ki|pukkaszt', 'hátra|köt', 'be|baktat', 'el|mutat', 'észre|vesz', 'át|keresztelkedik',
      'le|származtat', 'ki|listáz', 'le|nyisszant', 'szét|kuszál', 'el|ég', 'el|csöndesül', 'fel|dobban',
      'el|bájol', 'el|zörög', 'meg|perdít', 'át|hívat', 'meg|biztat', 'utána|fut', 'abba|hagy', 'le|igáz',
      'meg|sántul', 'fel|indít', 'szét|tárul', 'le|őröl', 'fel|oson', 'meg|interpellál', 'le|horgaszt',
      'össze|ró', 'le|amputál', 'le|sikál', 'meg|hány', 'el|színtelenít', 'ki|fakaszt', 'körbe|rohan',
      'be|ágyazódik', 'ki|gurít', 'elő|támolyog', 'be|karikázik', 'meg|vonalaz', 'tele|köpköd',
      'hozzá|szegődik', 'meg|könnyez', 'be|vezettet', 'vissza|hull', 'át|mulat', 'meg|rezzent',
      'fel|lobogóz', 'vissza|köt', 'körül|sétál', 'szét|hajlik', 'be|sántikál', 'ki|terelget', 'szét|hull',
      'el|zabrál', 'hátra|lök', 'le|reped', 'le|fittyed', 'fel|tarisznyál', 'el|gázosít',
      'alább|hagy', 'meg|hegyez', 'fel|dolgoz', 'le|nyomtat', 'ki|fehérlik', 'le|szegényedik',
      'le|maradozik', 'át|fűt', 'le|tűz', 'elő|énekel', 'ki|lábol', 'ki|rázódik', 'el|gördít', 'el|hibáz',
      'át|húzat', 'meg|botoz', 'át|kap', 'meg|kettőződik', 'bele|sóhajt', 'helyre|zökken',
      'szét|száll', 'meg|karóz', 'össze|szegez', 'el|biggyeszt', 'bele|választ', 'el|mered', 'közre|hat',
      'meg|süketít', 'haza|takarodik', 'meg|bérmál', 'meg|csömörlik', 'meg|fakad', 'ki|irtat',
      'be|süllyeszt', 'körül|ér', 'le|plombál', 'közre|játszik', 'fel|nyerít', 'be|lázasodik', 'le|hajlít',
      'külön|ír', 'végig|araszol', 'egybe|keveredik', 'oda|von', 'vissza|nyújt', 'alá|ad', 'le|támolyog',
      'ki|tapaszt', 'közre|fog', 'át|zúg', 'vissza|lovagol', 'meg|hűt', 'ki|fejel', 'ki|figuráz',
      'ki|kupálódik', 'utol|ér', 'be|durrant', 'el|ígér', 'szét|csattan', 'el|hangoz', 'végig|hurcol',
      'el|lejt', 'le|forog', 'be|zeng', 'le|hívat', 'le|sittel', 'meg|háromszoroz', 'meg|vasal',
      'meg|kergül', 'össze|egyezik', 'fel|idéződik', 'meg|hasonlik', 'felül|bélyegez', 'be|ténfereg',
      'végig|esik', 'el|szigetelődik', 'meg|vész', 'oda|lépked', 'ki|szőkít', 'el|erőtlenedik',
      'ki|tábláz', 'közre|bocsát', 'meg|illetődik', 'fel|billent', 'ki|dolgoz', 'túl|hűt', 'vissza|tükröz',
      'végig|csörtet', 'fel|fárad', 'ki|villog', 'keresztül|jár', 'el|gyávul', 'át|főz', 'be|erdősít',
      'el|világít', 'bele|tép', 'meg|irtózik', 'rá|éhezik', 'végig|böngész', 'fel|tetszik', 'át|fénylik',
      'el|temettet', 'bele|kaszál', 'be|lélegez', 'meg|bolydít', 'le|kecmereg', 'meg|puffad', 'át|zúdul',
      'elő|olvas', 'el|ér', 'végig|zuhan', 'ki|csempész', 'be|savanyodik', 'fel|retten', 'el|repeszt',
      'fel|magasít', 'be|fellegzik', 'meg|ömlik', 'be|nyargal', 'el|lustít', 'meg|férfiasodik',
      'ki|rügyezik', 'vissza|battyog', 'körül|dong', 'be|torkollik', 'vissza|készül', 'meg|fogódzkodik',
      'bele|toccsan', 'le|sugárzik', 'meg|fullaszt', 'le|meztelenít', 'meg|döndül', 'körül|hord',
      'szét|hint', 'ki|kotródik', 'át|remeg', 'oda|sorol', 'ide|lök', 'meg|lobban', 'be|kvártélyoz',
      'bele|dolgoz', 'ki|nyiffan', 'le|zuhog', 'tovább|fut', 'át|táncol', 'fel|ijeszt', 'el|vakkant',
      'félre|nevel', 'össze|fogat', 'be|fröcsköl', 'ki|golyóz', 'túl|hevít', 'át|hasít', 'el|távolíttat',
      'ki|kopog', 'külön|áll', 'vissza|vigyorog', 'ki|csuk', 'le|kicsinyel', 'le|nyomódik', 'ki|gázol',
      'mellé|talál', 'be|tűr', 'fel|mázol', 'fel|esküszik', 'egybe|állít', 'meg|fingat', 'körül|jártat',
      'át|származik', 'meg|tízszerez', 'el|gondolkoztat', 'fel|baktat', 'össze|hunyorít',
      'vissza|csempész', 'túl|fizet', 'rá|pipál', 'ellen|jegyez', 'meg|őrződik', 'le|perdül', 'abba|marad',
      'be|rezel', 'bele|csavar', 'haza|szólít', 'át|pofoz', 'ki|kísérletez', 'hozzá|kap',
      'meg|vonul', 'össze|forrad', 'át|olvad', 'el|agyabugyál', 'ketté|fűrészel', 'le|halkul', 'túl|kiált',
      'el|vermel', 'számon|kér', 'le|bámul', 'át|csempész', 'le|ordít', 'hátra|fut', 'be|hurcolkodik',
      'meg|vizsgáltat', 'fel|dobog', 'fel|nyúlik', 'utána|lát', 'meg|nyomogat', 'össze|teremt',
      'végig|vonaglik', 'fel|szokik', 'felül|múl', 'be|les', 'be|hajóz', 'ki|nyomul', 'el|hurcolkodik',
      'végig|kopog', 'el|árvul', 'hátra|int', 'meg|oldoz', 'át|vasal', 'le|horgonyoz', 'el|rágódik',
      'mellé|lép', 'egybe|illeszt', 'le|fotóz', 'elő|szivárog', 'végig|viharzik', 'le|ellik',
      'le|részegít', 'fel|habzsol', 'be|horpaszt', 'rá|biccent', 'el|barikádoz', 'meg|népesül',
      'be|szállingózik', 'le|lógat', 'bele|bődül', 'meg|kövesedik', 'ki|mélyül', 'oda|vár', 'össze|sül',
      'meg|dupláz', 'fel|hangosodik', 'alá|kanyarít', 'ki|szédeleg', 'el|vérez', 'le|előlegez',
      'ki|öblösödik', 'el|dörren', 'be|kocog', 'össze|tölt', 'vissza|származtat', 'át|tart',
      'össze|halmozódik', 'ki|fűződik', 'meg|pályáz', 'meg|forraszt', 'össze|ront', 'össze|gázol',
      'elő|keveredik', 'keresztül|bújik', 'ki|zúdít', 'meg|elevenül', 'le|hull', 'be|kíván',
      'meg|csalatkozik', 'nyilván|tart', 'ki|hull', 'körbe|hord', 'le|szakadozik', 'el|vitorlázik',
      'fel|takar', 'meg|csörget', 'elő|buggyan', 'át|tűz', 'össze|habar', 'el|boronál', 'kétségbe|ejt',
      'jóvá|hagy', 'szemben|áll', 'véget|ér', 'szörnyet|hal', 'útba|igazít', 'karban|tart', 'kétségbe|esik',
      'be|gyűrűzik', 'be|végeztetik', 'cserben|hagy', 'élen|jár', 'el|vetemül', 'helyben|hagy', 'helyt|áll',
      'jól|esik', 'jól|lakik', 'jóvá|hagy', 'közben|jár', 'meg|hibban', 'odébb|áll', 'rendre|utasít', 'rosszul|esik',
      'síkra|száll',
      'el|időz', 'el|puskáz', 'el|enyész', 'ki|mazsoláz', 'el|búcsúz', 'meg|éhez', 'meg|fáz', 'meg|reggeliz',
      'meg|szomjaz', 'meg|vacsoráz', 'rá|fáz', 'be|gubóz', 'el|szipkáz', 'fel|tornáz', 'le|fasisztáz', 'el|haláloz',
      'be|árnyékoz', 'meg|gémberedik', 'ki|esik', 'át|ázik', 'be|biztosít', 'el|csorog', 'igénybe|vesz', 'le|főz',
      'oda|utazik', 'vissza|kocog'
      }
     }

"""
these verbs should have an ik suffix
verb -> verb+ik
"""
verb_add_ik_suffix = {'be|költöz', 'bele|tel', 'be|sűrűsöd', 'egybe|gyűl',
                      'el|bizonytalanod', 'el|értéktelened', 'el|híz', 'el|távoz', 'be|tel', 'el|es', 'el|játsz',
                      'el|tel', 'el|tűn', 'el|vál', 'fel|erősöd', 'fel|gyűl', 'fel|tornász', 'fel|tűn',
                      'fel|zárkóz', 'föl|erősöd', 'hozzá|szok', 'ki|tel', 'ki|teljesed', 'le|tel', 'le|teleped',
                      'le|vizsgáz', 'meg|állapod', 'meg|bizonyosod', 'meg|buk', 'meg|egyez', 'meg|eléged',
                      'meg|erősöd', 'meg|es', 'meg|gyűl', 'meg|hibásod', 'meg|híz', 'meg|jelen', 'meg|nyíl',
                      'meg|sűrűsöd', 'meg|szok', 'meg|szűn', 'meg|tel', 'meg|úsz', 'meg|vál', 'meg|változ',
                      'össze|gyűl', 'össze|sűrűsöd', 'vissza|es', 'vissza|költöz', 'bele|egyez', 'ki|egyez',
                      'hozzá|szok',
                      'egyez', 'osztoz', 'csúsz', 'foglakoz',
                      'gyarapod', 'hazud', 'hibádz', 'híz', 'játsz', 'kés', 'költöz',
                      'különböz', 'létez', 'nyíl', 'sűrűsöd',
                      'származ', 'tapogatóz', 'tartoz', 'távoz', 'tel', 'telik--múl', 'tetsz', 'tornász',
                      'vál', 'változ', 'álmodoz', 'áramol', 'gyűl', 'mérkőz', 'rejtőz', 'szörföz', 'vitáz', 'vizsgáz',
                      'át|forrósod', 'el|adósod', 'fel|forrósod',
                      'horgász', 'álmod', 'erősöd', 'folyamod', 'gazdagod', 'közeled', 'önállósod', 'részesed',
                      'rozsdásod', 'tűn', 'felvételiz', 'túlóráz'
                      }

"""
Occur not splitted but only the splitted is OK. And ik suffix is needed
unsplitted -> splitted+ik
"""

prev_and_ik_verbs = \
             {elem.replace('|', ''): (elem + 'ik') for elem in
              {'ki|es', 'rá|fáz', 'meg|esz'}}


def fix_verb(verb_elem):
    if verb_elem in double_prev_verbs or verb_elem in not_rev_verbs_drop_prev or \
            ('|' in verb_elem and verb_elem.split('|', maxsplit=1)[1] in never_prev_verbs):
        verb_elem = verb_elem.split('|', maxsplit=1)[1]
    elif verb_elem in not_prev_verbs or verb_elem in not_prev_verbs2:  # Remove split
        verb_elem = verb.replace('|', '')
    elif verb_elem in verb_add_ik_suffix:
        verb_elem += 'ik'
    verb_elem = not_prev_verbs3.get(verb_elem, verb_elem)  # Put split
    verb_elem = funny_ik_replacements.get(verb_elem, verb_elem)  # Funny ik replacement
    verb_elem = prev_and_ik_verbs.get(verb_elem, verb_elem)  # ik+ verbal particle
    if '|' in verb_elem and verb_elem.split('|', maxsplit=1)[1] in light_verb_exception_verbs and\
            verb_elem not in light_verb_exception_verbs_w_prev:
        verb_elem = verb_elem.split('|', maxsplit=1)[1]

    return verb_elem


def get_freq_w_ind_for_frame(frames, frame):
    for i, (freqency, curr_frame) in enumerate(frames):
        if curr_frame == frame:
            return i, freqency
    else:
        return -1, 0


def smart_append(verbs_dict, verb_elem, freqency, frame):
    if verb_elem in verbs_dict:
        frame_ind, frame_freq = get_freq_w_ind_for_frame(verbs_dict[verb_elem], frame)
        if frame_ind >= 0:
            verbs_dict[verb_elem][frame_ind][0] = frame_freq + freqency
            return
    verbs_dict[verb_elem].append([freqency, frame])


verb_dict_verbs = defaultdict(list)
verb_dict_sumfreq = 0
with open('ige_szotar/szotar.kimenet.txt', encoding='UTF-8') as verb_dict:
    for entry in verb_dict:
        entry = entry.strip().split('\t')
        if len(entry) == 3:
            verb, freq, example = entry
            arguments = []
        elif len(entry) >= 4:
            verb, *arguments, freq, example = entry
        else:
            break
        freq = int(freq)
        if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev or\
                verb in wrong_verbs3:
            continue
        verb = fix_verb(verb)
        arguments = [i.replace(' =', '=') for i in arguments]  # Because at the end args will be separated by spaces
        smart_append(verb_dict_verbs, verb, freq, tuple(sorted(arguments)))
        verb_dict_sumfreq += freq

print('No. of Verbs (ige_szotar): ', len(verb_dict_verbs), file=sys.stderr)


isz_verbs = defaultdict(list)
isz_sumfreq = 0
with open('isz/igeiszerkezet-lista.kimenet.txt', encoding='UTF-8') as isz:
    for entry in isz:
        if not entry.startswith((' 0', 'Igeskicc')):
            entry = entry.strip().split('\t')
            if len(entry) == 2:
                verb, freq = entry
                arguments = []
            elif len(entry) >= 3:
                verb, *arguments, freq = entry
            else:
                break
            freq = int(freq)
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or\
                    verb in verb_bad_prev or verb in wrong_verbs3:
                continue
            verb = fix_verb(verb)
            arguments = [i.replace(' =', '=') for i in arguments]  # Because at the end args will be separated by spaces
            smart_append(isz_verbs, verb, freq, tuple(sorted(arguments)))
            isz_sumfreq += freq

print('No. of Verbs (isz): ', len(isz_verbs), file=sys.stderr)

tade_verbs = defaultdict(list)
tade_sumfreq = 0
with open('tade/tade.kimenet.tsv', encoding='UTF-8') as tade:
    for entry in tade:
        entry = entry.strip().split('\t')
        if len(entry) == 5:
            verb, arguments, freq, igegyak, arany = entry
            if arguments[0] == '@':
                arguments = ''
        else:
            break
        arguments = tuple(arguments.split())
        freq = int(freq)
        if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev or\
                verb in wrong_verbs3:
            continue
        verb = fix_verb(verb)
        # Fix double argumetns: Uniq
        set_vonzatok = set(arguments)
        if len(arguments) > len(set_vonzatok):
            arguments = tuple(set_vonzatok)
        if ' ' in verb:
            if verb.startswith('"'):
                print('Dropped: {0}'.format(verb), file=sys.stderr)
                continue
            verb, inf = verb.split()
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or\
                    verb in verb_bad_prev or verb in wrong_verbs3:
                continue
            verb = fix_verb(verb)
            # Do not append INF's frame to the non-INF occurence's frame.
            # It could contain argument of the FIN verb too!
            # TODO: Research a solution later...
            # smart_append(tade_verbs, inf, freq, tuple(sorted(arguments)))  # Here stuff can be non uniq...
            # tade_sumfreq += freq
            # arguments = ['INF_' + inf]
            arguments = ['INF']
        smart_append(tade_verbs, verb, freq, tuple(sorted(arguments)))  # Here stuff can be non uniq...
        tade_sumfreq += freq

print('No. of Verbs (Tadé): ', len(tade_verbs), file=sys.stderr)

kagi_verbs = Counter()
kagi_sumfreq = 0
with open('kagi_verbal_complex/freqPrevFin.txt', encoding='UTF-8') as kagi:
    for entry in kagi:
        entry = entry.strip().split(' ')
        if len(entry) == 2:
            freq, verb_w_ik = entry
        else:
            break
        ik, verb = verb_w_ik.split('+')
        freq = int(freq)
        if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev or\
                verb in wrong_verbs3:
            continue
        verb = fix_verb(verb)
        kagi_verbs['{0}|{1}'.format(ik, verb)] = freq
        kagi_sumfreq += freq

print('No. of Verbs (kagi_verbal_complex): ', len(kagi_verbs), file=sys.stderr)


# TODO: document
inflist_verbs = defaultdict(list)
inflist_sumfreq = 0
with open('infinitival_constructions/FinInf.txt', encoding='UTF-8') as inflist:
    for entry in inflist:
        entry = entry.strip().split(' ')
        if len(entry) == 2:
            freq, verb_w_ik = entry
            if '+' in verb_w_ik:
                ik, verb = verb_w_ik.split('+')
                verb = '{0}|{1}'.format(ik, verb)
            else:
                freq, verb = entry
        else:
            break
        freq = int(freq)
        arguments = ['INF']
        smart_append(inflist_verbs, verb, freq, tuple(sorted(arguments)))
        inflist_sumfreq += freq

print('No. of Verbs (inflist): ', len(inflist_verbs), file=sys.stderr)


all_ige = set(verb_dict_verbs.keys()) | set(isz_verbs.keys()) | set(tade_verbs.keys()) | set(inflist_verbs.keys())
print('Igék száma (összesen): ', len(all_ige), file=sys.stderr)

for verb in sorted(all_ige):
    szotar_frames = tuple([frame[1] for frame in verb_dict_verbs[verb]])
    isz_frames = tuple([frame[1] for frame in isz_verbs[verb]])
    tade_frames = tuple([frame[1] for frame in tade_verbs[verb]])
    inflist_frames = tuple([frame[1] for frame in inflist_verbs[verb]])
    all_frame = set(szotar_frames) | set(isz_frames) | set(tade_frames) | set(inflist_frames)
    if len(szotar_frames) + len(isz_frames) + len(tade_frames) + len(inflist_frames) > len(all_frame):
        print(verb, list(sorted(set(szotar_frames) & set(isz_frames))),
              list(sorted(set(isz_frames) & set(tade_frames))),
              list(sorted(set(tade_frames) & set(szotar_frames))),
              list(sorted(set(tade_frames) & set(inflist_frames))),  # TODO: document
              kagi_verbs[verb], sep='\n', end='\n\n', file=sys.stderr)
    for act_frame in sorted(all_frame):
        szotar_freq = get_freq_w_ind_for_frame(verb_dict_verbs[verb], act_frame)[1]
        isz_freq = get_freq_w_ind_for_frame(isz_verbs[verb], act_frame)[1]
        tade_freq = get_freq_w_ind_for_frame(tade_verbs[verb], act_frame)[1]
        kagi_freq = None
        kagi_freq_rank = 0
        if '|' in verb:
            kagi_freq = kagi_verbs.get(verb, 0)
            kagi_freq_rank = kagi_freq / kagi_sumfreq

        inflist_freq = None
        inflist_freq_rank = 0
        if len(act_frame) > 0 and act_frame[0] == 'INF':
            inflist_freq = inflist_verbs.get(verb)
            if len(inflist_freq) == 0:
                inflist_freq = 0
            else:
                inflist_freq = inflist_freq[0][0]  # Freq for act frame
            inflist_freq_rank = inflist_freq / inflist_sumfreq
        if act_frame == ():
            act_frame = '@'
        else:
            act_frame = ' '.join(act_frame)
        rank = sum((szotar_freq / verb_dict_sumfreq, isz_freq / isz_sumfreq, tade_freq / tade_sumfreq,
                    kagi_freq_rank, inflist_freq_rank))
        print(verb, act_frame, szotar_freq, isz_freq, tade_freq, kagi_freq, inflist_freq,
              '{0:1.20f}'.format(rank), sep='\t')

"""
time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k10,10nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
