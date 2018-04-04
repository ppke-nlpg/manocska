#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

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
false_prev_good = {'felesel', 'felvételizik', 'kiabál', 'mellékel', 'szembesül', 'túlórázik', 'fölényeskedik',
                   'alázatoskodik', 'televíziózik', 'feliratoz'
                   }

"""
with hyphen funny ik need to replaced
replace funny ik
"""
funny_ik_replacements = {'ad--veszik': 'ad--vesz', 'lát--hallik': 'lát-hall', 'tel--múl': 'telik--múlik',
                         'törik--zúz': 'tör--zúz', 'el|abbahagy': 'abba|hagy', 'el|kitábláz': 'ki|tábláz',
                         'földet|megdolgoz': 'meg|dolgoz', 'ki|abbahagy': 'abba|hagy', 'ki|felülmúl': 'felül|múl',
                         'ki|kiaggat': 'kiaggat', 'ki|odacsíp': 'oda|csíp', 'külön|megesz': 'meg|esz',
                         'külön|kidolgoz': 'ki|dolgoz', 'külön|közreműködik': 'közre|működik',
                         'külön|nyilvántart': 'nyilván|tart', 'meg|alábújik': 'alá|bújik', 'meg|áthálóz': 'át|hálóz',
                         'meg|cserbenhagy': 'cserben|hagy', 'meg|elvetemül': 'el|vetemül',
                         'meg|felkantároz': 'fel|kantároz', 'meg|felvirágoz': 'fel|virágoz',
                         'meg|karbantart': 'karban|tart', 'meg|kipislant': 'ki|pislant',
                         'meg|kitakarózik': 'ki|takarózik', 'meg|közrejátszik': 'közre|játszik',
                         'meg|lehull': 'le|hull', 'meg|megdolgoz': 'meg|dolgoz', 'meg|összedolgoz': 'össze|dolgoz',
                         'oda|bejárogat': 'be|járogat', 'rá|visszasüt': 'vissza|süt',
                         'teli|megcsömörlik': 'meg|csömörlik', 'újra|végigpásztáz': 'végig|pásztáz',
                         'utána|abbahagy': 'abba|hagy', 'utána|áttáncol': 'át|táncol',
                         'utána|beledolgoz': 'bele|dolgoz', 'utána|berigliz': 'be|rigliz', 'utána|megesz': 'meg|esz',
                         'utána|összesajtol': 'össze|sajtol', 'felhízlal{ORTH:substandard}': 'fel|hízlal'
                         }

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

good_verbs_humor_not_recognised3 = {'jelent|jelentet', 'békén|hagy', 'vet|vetet', 'bent|jár',
                                    'bicsakol', 'csökkent|csökkentet', 'döglik|dögöl', 'ébreszt|ébresztet',
                                    'edz|edzet', 'ejt|ejtet', 'fejt|fejtet', 'felejt|felejtet', 'hí|hív',
                                    'ment|mentet', 'vérezik|vérzik', 'veszt|vesztet', 'emlékezik|emlékszik',
                                    'ereszt|eresztet', 'érez|érzik', 'érint|érintet', 'ért|értet',
                                    'fejleszt|fejlesztet', 'fejt|fejtet', 'felejt|felejtet', 'hí|hív',
                                    'jelent|jelentet', 'kelt|keltet', 'ment|mentet', 'ért|értet',
                                    'feltételez', 'félt|féltet', 'vet|vetet', 'fest|festet', 'gerjeszt|gerjesztet',
                                    'habozik|habzik', 'hajlik|hajol', 'hangozik|hangzik',
                                    'hiányozik|hiányzik', 'hí|hív', 'illet|illik', 'int|intet', 'jelent|jelentet',
                                    'jól|esik', 'kell|kelletik', 'kelt|keltet', 'kétségbe|esik', 'ejt|ejtet',
                                    'fejleszt|fejlesztet', 'fejt|fejtet', 'felejt|felejtet', 'jelent|jelentet',
                                    'betegedik|betegszik', 'hajlik|hajol', 'int|intet',
                                    'törleszt|törlesztet', 'vet|vetet', 'ért|értet', 'hí|hív', 'lesz|van',
                                    'ment|mentet', 'teremt|teremtet', 'vet|vetet', 'melegedik|melegszik',
                                    'mellékel', 'ment|mentet', 'rogyaszt', 'rosszul|esik',
                                    'sejt|sejtet', 'sért|sértet', 'síkra|száll', 'szembesül', 'szerkeszt|szerkesztet',
                                    'talizik', 'tekint|tekintet', 'teremt|teremtet', 'terjeszt|terjesztet',
                                    'tetszet|tetszik', 'veszik|veszt', 'veszt|vesztet', 'vet|vetet', 'jön|jő',
                                    'bé|lát', 'bele|nyammog', 'el|nyammog', 'el|kunyizik', 'le|föst', 'le|pittyeszt',
                                    'le|tapizik', 'le|vetkez', 'meg|murdel', 'be|csődöl', 'meg|siketül',
                                    'össze|kunyizik', 'össze|pocsol', 'körül|nézgelődik', 'általánosul', 'anyagiasul',
                                    'barcog', 'böstörködik', 'cicózik', 'ciklizál', 'cöcög', 'cserkel', 'csevegdél',
                                    'csucsul', 'dogmatizál', 'dörömböz', 'egyéniesül', 'embolizál', 'érdel',
                                    'értékesül', 'fakadozik', 'fázlódik', 'fecser', 'fényesül', 'fogvatart', 'fől',
                                    'föst', 'furikol', 'gépiesül', 'gyömköd', 'hajkurászik', 'háramol', 'hastáncol',
                                    'hemolizál', 'hókuszpókuszol', 'horgonyzik', 'horpadozik', 'hőkezel', 'hörpent',
                                    'hőszigetel', 'ingerül', 'ivogat', 'kalamol', 'kandít', 'karmolászik', 'keringél',
                                    'keringet', 'kerreg', 'kolbászol', 'konkurrál', 'konszekrál', 'korhadozik', 'ködöl',
                                    'kövérszik', 'köznevesül', 'krisztianizál', 'kurtul', 'légiesül', 'lesekedik',
                                    'lifeg', 'loccsint', 'magasul', 'mosolyint', 'nézgelődik', 'nyammog', 'öklend',
                                    'ömöl', 'öregbül', 'pampog', 'paszíroz', 'pihizik', 'pikíroz', 'pogózik',
                                    'potencíroz', 'pöcsöl', 'prüsszen', 'pufferol', 'rágogat', 'reszakralizál', 'riog',
                                    'rohog', 'súlyosul', 'szakralizál', 'szakralizálódik', 'táncikál', 'tapizik',
                                    'tehermentesül', 'telik--múlik', 'toronylik', 'transzcendál', 'transzportál',
                                    'treffel', 'tutul', 'tüsszen', 'utóvizsgázik', 'útrakel', 'vakarászik', 'vemhesül',
                                    'vidámkodik', 'virgonckodik', 'pofon|csap', 'ellen|tart', 'ellen|támad',
                                    'elé|toppan', 'elé|áll', 'elé|borul', 'elé|citál'
                                    }


"""
Prev and verb do not go together
and
strange combinations
delete
"""
# TODO: further research (delete)
not_prev_verbs_TODO_FR = {'jól|esik', 'jól|lakat', 'jól|lakik', 'jól|tart', 'jót|áll', 'rosszul|esik', 'után|állít',
                          'után|ízesít', 'után|nyom', 'után|rendel', 'után|tölt', 'abba|fejez',
                          'együtt|hat'
                          }

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
Humor not recognised these verb forms (without preverb) -> delete
mostly: stemming error and bad preverb
"""
bad_forms = {'8|?NOUN[ACT]', 'abba|null', 'agyon|dóg', 'agyon|éh', 'alább|null', 'alá|null', 'alul|dozíro',
             'alul|finanszíro', 'át|áramol', 'át|baik', 'át|buborék', 'át|cserké', 'át|értelem', 'át|estet', 'át|gyűrű',
             'át|hagyomány', 'át|kereszt', 'át|kristály', 'át|masszíro', 'át|név', 'át|null', 'át|pár', 'át|skála',
             'át|só', 'át|struktúra', 'át|szám', 'át|szellő', 'át|tanulmány', 'át|tev', 'át|transzportál', 'át|ütem',
             'át|varázs', 'át|ve', 'be|áldo', 'be|ár', 'be|áramol', 'be|beton', 'be|birkóik', 'be|épit', 'be|erdősül',
             'be|fertő', 'be|gyűrű', 'be|hivat', 'be|injekció', 'be|jegy', 'be|-kapcs', 'be|kasszíro',
             'bele|bíztat{ORTH:substandard}', 'bele|dugdo', 'bele|fegyelem', 'bele|hím', 'bele|interioriza',
             'bele|maga', 'bele|mo', 'bele|null', 'belé|null', 'bele|passzíro', 'bele|tag', 'bele|vé', 'be|melír',
             'benn|null', 'be|null', 'be|öntö', 'be|padló', 'be|ráma', 'be|rögzik', 'be|szög', 'be|tag', 'bé|töl',
             'be|üzem', 'be|vacok', 'be|vagdo', 'be|ve', 'be|vite', 'egybe|mo', 'egybe|null', 'egyet|prüsszen',
             'egyet|tüsszen', 'el|átok', 'el|baik', 'el|bí', 'el|bizonytalaní', 'el|dózer', 'el|-elszemle', 'el|-elter',
             'el|fátyolo', 'el|fertő', 'el|határ', 'el|hó', 'el|imádkoik', 'el|k', 'el|kötö', 'el|különb', 'el|mátka',
             'el|méreg', 'el|nedvesül', 'el|null', 'elő|fesel', 'elő|finanszíro', 'elő|kiváncsiskodik', 'elő|kotoráik',
             'el|ömöl', 'elő|null', 'elő|políro', 'előre|ho', 'előre|null', 'elő|ve', 'el|postá', 'el|romol',
             'el|szégyenel', 'el|szén', 'el|tájék', 'el|tömegesül', 'el|tüsszen', 'el|varázs', 'fel|dolog', 'fel|épit',
             'fel|-felidé', 'fel|fesel', 'fel|iik', 'fel|kariká', 'fel|köl', 'fel|méreg', 'fel|normál', 'fel|null',
             'félre|értelme', 'félre|null', 'félre|olva', 'félre|rugdo', 'félre|tájék', 'fel|szoro', 'fenn|null',
             'föl|áldo', 'föl|derí', 'föl|dolog', 'föl|épí', 'föl|fű', 'föl|ho', 'föl|hú', 'föl|ingerül', 'föl|kariká',
             'föl|lármáik', 'föl|melenge', 'föl|null', 'föl|olva', 'föl|poggyász', 'föl|rá', 'föl|repí',
             'föl|szerelkeik', 'föl|tárcsáik', 'föl|tornász', 'föl|trancsíro', 'fönn|null', 'hátra|dűt', 'haza|null',
             'haza|segí', 'hozzá|formá', 'hozzá|null', 'ide|null', 'ki|aluik', 'ki|bíztat{ORTH:substandard}',
             'ki|csumá', 'ki|dekáik', 'ki|dolog', 'ki|fugá', 'ki|levegő', 'ki|lista', 'ki|manőver', 'ki|mazsolá',
             'ki|méreg', 'ki|null', 'ki|postá', 'ki|raj', 'ki|rajzo', 'ki|rugdo', 'ki|seregel', 'ki|sugár', 'ki|számlá',
             'ki|szipká', 'ki|szomj', 'ki|terjeszte', 'ki|tornász', 'ki|ülepí', 'ki|vadáik', 'ki|ve', 'ki|vetkez',
             'ki|villany', 'ki|zsinór', 'kölcsön|null', 'körbe|hordo', 'körbe|mo', 'körbe|úik', 'körbe|ve',
             'körül|fecskende', 'körül|koszorú', 'körül|nyaldo', 'közbe|null', 'le|aszfalt', 'le|béklyó', 'le|dózer',
             'le|fogdo', 'le|fólia', 'le|formá', 'le|fű', 'le|gyanta', 'le|hajó', 'le|horgász', 'le|kérde', 'le|köpdö',
             'le|műszaki', 'le|null', 'le|nulla', 'le|nullá', 'le|nyilatkoik', 'le|passzíro', 'le|selejt', 'le|tehe',
             'le|ű', 'le|vagdo', 'le|zsűri', 'meg|baik', 'meg|béke', 'meg|bí', 'meg|bot', 'meg|böfi', 'meg|csókolga',
             'meg|dicsô', 'meg|ezer', 'meg|félegázüzemanyagotkülönb', 'meg|finanszíro', 'meg|fogalm', 'meg|fogalom',
             'meg|fonnya', 'meg|formá', 'meg|g-g-gúny', 'meg|hajkurászik', 'meg|halá', 'meg|három', 'meg|határ',
             'meg|hét', 'meg|hinta', 'meg|hivat', 'meg|hu', 'meg|húsz', 'meg|injekció', 'meg|ismét', 'meg|jutalom',
             'meg|kédőjel', 'meg|-kérdőjel', 'meg|kordul', 'meg|korona', 'meg|köll', 'meg|kölönb', 'meg|különbö',
             'meg|méreg', 'meg|minta', 'meg|normál', 'meg|null', 'meg|nyolc', 'meg|ostor', 'meg|önb', 'meg|öt',
             'meg|pálya', 'meg|pár', 'meg|rágalom', 'meg|roham', 'meg|rongálo', 'meg|roskadoik', 'meg|rugdo',
             'meg|szellő', 'meg|szondá', 'meg|tehe', 'meg|torna', 'meg|tornász', 'meg|tripla', 'meg|turné', 'meg|út',
             'meg|változtatta-vált', 'meg|ve', 'meg|verseny', 'meg|vonalká', 'nagyot|kordul', 'neki|vetkez', 'oda|ho',
             'oda|kötö', 'oda|null', 'oda|varázs', 'össze|horgász', 'össze|játik', 'össze|koma', 'össze|null',
             'össze|políro', 'össze|satíro', 'össze|sí', 'össze|ve', 'össze|-visszakusza', 'rá|ébre', 'rá|er',
             'rá|fénykép', 'rá|hagyomány', 'rá|horgász', 'rá|költöik', 'rá|null', 'rá|szerv', 'reá|null', 'szembe|null',
             'szerte|hajkurászik', 'szerte|kerge', 'szerte|null', 'szét|baik', 'szét|bombá', 'szét|null', 'szét|pukka',
             'szét|rá', 'szét|rugdo', 'szét|szortíro', 'szét|trancsíro', 'tovább|fű', 'tovább|hordo', 'tovább|null',
             'tovább|számlá', 'túl|null', 'túl|paráik', 'újjá|rend', 'újjá|szerv', 'újra|értelem', 'újra|értelme',
             'újra|fertő', 'újra|fogalom', 'újra|formá', 'újra|játik', 'újra|lista', 'újra|null', 'újra|o', 'újra|olva',
             'újra|pálya', 'újra|rend', 'újra|szám', 'újra|szerv', 'utána|disszipa', 'utána|hú', 'után|hú',
             'utól|{ORTH:substandard}ér', 'végig|aluik', 'végig|birkóik', 'végig|hazudoik', 'végig|kere', 'végig|null',
             'végig|szó', 'vissza|null', 'vissza|postá', 'vissza|rend', 'vissza|rugdo', 'vissza|számla',
             'vissza|számlá', 'vissza|tag', 'vissza|varázs', 'vissza|ve', 'viszont|null', 'y|?NOUN[ACT]',
             'z|?NOUN[ACT]', 'ide|seregel', 'elő|seregel', 'fel|seregel', 'szét|seregel', 'össze|seregel', 'be|seregel',
             'le|horgonyzik', 'meg|bicsakol', 'meg|bűzöl', 'meg|édesül', 'meg|egyenesül', 'meg|nedvesül', 'meg|romol',
             'meg|szennyesül', 'meg|vidámul', 'oda|seregel', 'át|fesel', 'föl|fesel', 'hátra|bicsakol', 'ide|áramol',
             'ki|áramol', 'ki|fesel', 'ki|ficamul', 'ki|loccsint', 'ki|öklend', 'ki|ömöl', 'ki|paszíroz',
             'fel|hízlal{ORTH:substandard}'
             }


bad_forms2 = {'10', '12.er', '12.várak', '1492-rebefej', '3.megvált', 'abeab', 'acidifika', 'affilia', 'aggrega',
              'aholfoglalk', 'aklimatiza', 'akol', 'aktíva', 'aktiviliza', 'állnak-szemle', 'anarchiza',
              'antropomorfiza', 'anyakönyv', 'áramk', 'áramolik', 'aretta', 'assszimila', 'aszondja', 'aszongya',
              'aszszimila', 'áterend', 'aterm', 'átpaszíroz', 'átszin', 'átteleporta', 'bafej', 'bajol', 'bakapcs',
              'banaliza', 'befely', 'bekap-cs', 'belémkód', 'benedikál', 'beteleporta', 'bib', 'bili', 'bontódnak-bog',
              'böfi', '-böjt', 'centra', 'csapágy', 'csicska', 'dagonya', 'dajer', 'defragmenta', 'dekonspira',
              'dekonstrua', 'delabializa', 'démoniza', 'depolimeriza', 'depolitiza', 'deregisztra', 'deszakraliza',
              'dezantropomorfiza', 'diagonál', 'diferencia', 'dimeriza', 'diszperga', 'diverzifika', 'dűt',
              'egymásrahang', 'ék', '-él', 'elbucsu', 'eldisszipa', 'elektroniza', 'életrek', 'elkommercializa',
              'ellenpont', 'ellentétel', 'elővétel', 'elül-tájék', 'emlek', 'epila', 'épit', 'er', 'érdek',
              'érdekel-foglalk', 'érlelődik-deforma', 'erroda', 'érzék', 'érzé-k', 'érzékeli-érzék', 'estet',
              'eszencia', 'etartó', 'európaiza', 'eutrofiza', 'excardina', 'exkala', 'expressza', 'fantomiza',
              'feudaliza', 'fogalk', 'foglakozik', 'foglal-k', 'foglalkoztatott&ndash;foglalk', 'fogllak', 'folgalalk',
              'folkloriza', 'fölkászma', 'fragamenta', 'fu', 'fúziona', 'fü', 'ga', 'gargaliza', 'hamísít', 'három',
              'helyh', 'hidraliza', 'hízlal{ORTH:substandard}', 'hó', 'homogeniza', 'hozzámkapcs', 'hu', 'ígaz',
              'i.izem', 'infantiliza', 'infla', 'inicializa', 'inkorpora', 'intenzifika', 'interioriza', 'ite',
              'k', 'ka', '-kapcs', 'kap-cs', '-kész', 'készletrevétel', 'kiegyen-l', 'kihu', 'kimelír',
              'kiváncsiskodik', 'klassziciza', 'koca', 'koeduka', 'kompletta', 'koncelebrál', 'koncenra', 'koncetra',
              'konformiza', 'konkrétiza', 'konnota', 'konstitua', 'kormány', 'korrodea', 'korszerű', 'könnyá',
              'köréje-rend', 'körvonal', 'kriminaliza', 'kristály', 'lareduka', 'lehet.szemle', '-lemorzs', 'lúdbor',
              'ly', 'marina', 'másfél', 'mcdonaldiza', 'medikaliza', '-megalap', 'megdup-lá',
              'meghízlal{ORTH:substandard}', 'meghúszszor', 'megk', 'megkér-dőjel', 'megkérdő-jel', '-megkülönb',
              'megtizenháromszor', 'mégvált', 'megváltozásahú', 'mélyül-hú', 'menifeszta', 'mentaliza', 'mérsék',
              'metaforiza', 'mevált', 'mineraliza', 'mitiza', 'nagyontag', 'napa', 'naplégkörben-megszikrá', 'natk',
              '&ndash;kirajz', 'nevekedik', 'ny', 'nyű{ORTH:substandard}', 'objektiva', 'objektiviza', 'odahu',
              'osztály', 'önfoglalk', 'örvény', 'összehu', 'öszszekapcs', 'passziva', 'passziviza', 'passzva',
              'penetra', 'perk', 'pigmenta', 'pillanatfű', 'plakát', 'plasztika', 'pluraliza', 'poétiza',
              'problematiza', 'professzionaliza', 'projicia', 'pulveriza', 'rákosiza', 'recipia', 'regera', 'regiszta',
              'repona', 'restimula', 'riboszómákkapcs', 'ritualiza', 'sétakocsiká', 'sí', 'sokáig.e', 'struktúra',
              'sürgölődök-forg', 'szakvélemény', 'szegrega', 'szellô', 'szeme', 'szemiotiza', 'szenyny', 'szer', 'szin',
              'szinter', 'szita', 'szóra-k', 'szörnyűködik', 'szuperpona', 'szúrka', 'szükésg', 't', 'táják', 'tajek',
              'tájek', 'tajék', '-tájék', 'tájé-k', 'tájlk', 'tálék', 'támít', 'tanus', 'tartósul', 'tematiza',
              'termaliza', 'tevékeny', 'transzloka', 'tűkr', 'tükrö', 'tűrtö', 'üzelm', 'vagyon', 'vállt', 'van.-kapcs',
              'varázs', 'vát', 'védjegy', 'végighu', 'végleg', 'verbúva', 'versenget', 'viosszatükr', 'virtualiza',
              'visszahu', 'viszatasz', 'vizualiza', 'wált', '-zúg', 'zsűrí', 'ballagdál', 'be|j', 'békén|él',
              'bé|takar', 'el|ite', 'elő|bányáik', 'elő|csíra', 'elő|hám', 'elő|varázs', 'föl|idé', 'haza|szánkó',
              'ki|-él', 'ki|sellő', 'ki|sér', 'kölcsön|áll', 'kölcsön|ér', 'kölcsön|tanul', 'kölcsön|vállal', 'le|ve',
              'meg|átok', 'össze|g', 'pofon|csattan', 'rá|ma', 'számba|kér', 'után|él', 'be|megszűkül', 'megváltó'
              }


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
                           'rendre|próbál', 'számba|sikerül', 'be|intubál', 'egyet|vidámkodik', 'le|kandít',
                           'ki|dörömböz', 'ki|leffen', 'után|szárad'
                           }

funny_prev_drop_prev = {'abba|dob', 'abba|esik', 'abba|eszik', 'abba|kerül', 'abba|könyököl', 'abba|megy', 'abba|pisil',
                        'abba|tartozik', 'abba|téved', 'abba|varázsol', 'abba|visz', 'arrébb|mozdít', 'arrébb|taszít',
                        'arrébb|tol', 'arrébb|ül', 'bé|borít', 'bé|csal', 'bé|csen', 'bé|dug', 'bé|enged', 'bé|fal',
                        'bé|fed', 'bé|főz', 'bé|fut', 'bé|gyűrűz', 'bé|hall', 'bé|hantol', 'bé|hoz', 'bé|ír',
                        'bé|jelentkezik', 'bé|jön', 'békén|alszik', 'békén|arat', 'békén|boldogul', 'békén|hajt',
                        'békén|hallgat', 'békén|hordoz', 'békén|hömpölyög', 'békén|pihen', 'békén|tehet', 'békén|tűr',
                        'bé|köt', 'bé|következik', 'bé|lep', 'bé|lép', 'beljebb|megy', 'bé|megy', 'bé|mutat', 'bé|néz',
                        'benne|felejt', 'benne|foglal', 'benne|foglaltatik', 'benne|hagy', 'benne|marad', 'benne|ragad',
                        'benne|ragyog', 'benne|rejlik', 'benne|reked', 'bent|ég', 'bent|foglaltatik', 'bent|marad',
                        'bent|szakad', 'bé|nyel', 'bé|pótol', 'bé|ragyog', 'bé|repül', 'bé|szárnyal', 'bé|szegez',
                        'bé|takarít', 'bé|tanít', 'bé|telepít', 'bé|tesz', 'bé|tol', 'bé|tölt', 'bé|vesz', 'bé|vet',
                        'bé|vezet', 'bé|visz', 'egyet|ad', 'egyet|ajándékoz', 'egyet|ajánl', 'egyet|állít',
                        'egyet|ásít', 'egyet|bánt', 'egyet|becsül', 'egyet|bénázik', 'egyet|biciklizik',
                        'egyet|biggyeszt', 'egyet|billent', 'egyet|bizonyít', 'egyet|bólint', 'egyet|botlik',
                        'egyet|bődül', 'egyet|böffen', 'egyet|böfög', 'egyet|bőg', 'egyet|bök', 'egyet|bukik',
                        'egyet|búsul', 'egyet|büfög', 'egyet|cigizik', 'egyet|csap', 'egyet|csatol', 'egyet|csavar',
                        'egyet|csavarint', 'egyet|csavarog', 'egyet|csettint', 'egyet|cseveg', 'egyet|csigáz',
                        'egyet|csikordul', 'egyet|csilingel', 'egyet|csinál', 'egyet|csíp', 'egyet|csipog',
                        'egyet|csippent', 'egyet|csobban', 'egyet|csóvál', 'egyet|csörren', 'egyet|dalol',
                        'egyet|danol', 'egyet|deklarál', 'egyet|delegál', 'egyet|dob', 'egyet|dobban', 'egyet|dobbant',
                        'egyet|döccen', 'egyet|dördül', 'egyet|dug', 'egyet|durran', 'egyet|durrant', 'egyet|él',
                        'egyet|emel', 'egyet|emelkedik', 'egyet|énekel', 'egyet|érdekel', 'egyet|érez', 'egyet|érint',
                        'egyet|értékesít', 'egyet|érzeleg', 'egyet|eszik', 'egyet|fárad', 'egyet|fél', 'egyet|feled',
                        'egyet|fingik', 'egyet|fintorog', 'egyet|fizet', 'egyet|fogad', 'egyet|foglalkoztat',
                        'egyet|fogyaszt', 'egyet|fordít', 'egyet|fordul', 'egyet|forog', 'egyet|forral', 'egyet|fotóz',
                        'egyet|főz', 'egyet|fúj', 'egyet|fut', 'egyet|futkározik', 'egyet|fürdik', 'egyet|füttyent',
                        'egyet|gondolkodik', 'egyet|gurul', 'egyet|gyárt', 'egyet|gyújt', 'egyet|gyűjt', 'egyet|habzik',
                        'egyet|hagy', 'egyet|hall', 'egyet|hallgat', 'egyet|harap', 'egyet|hatástalanít',
                        'egyet|háziasít', 'egyet|hiányol', 'egyet|hisz', 'egyet|hív', 'egyet|hoz', 'egyet|hördül',
                        'egyet|hörpint', 'egyet|hüppög', 'egyet|idéz', 'egyet|int', 'egyet|ír', 'egyet|irányít',
                        'egyet|ismer', 'egyet|ismertet', 'egyet|ismételget', 'egyet|iszik', 'egyet|ítél',
                        'egyet|játszik', 'egyet|javasol', 'egyet|jelenik', 'egyet|jelez', 'egyet|jellemez',
                        'egyet|juttat', 'egyet|kakil', 'egyet|kanyarodik', 'egyet|kap', 'egyet|károg',
                        'egyet|káromkodik', 'egyet|kattan', 'egyet|kényszerít', 'egyet|képvisel', 'egyet|kérd',
                        'egyet|kérdez', 'egyet|keres', 'egyet|kerül', 'egyet|készít', 'egyet|kiált',
                        'egyet|kondul', 'egyet|koppan', 'egyet|koppant', 'egyet|korlátoz', 'egyet|korog',
                        'egyet|kortyint', 'egyet|kortyol', 'egyet|köhent', 'egyet|kölcsönöz', 'egyet|köp',
                        'egyet|kreál', 'egyet|kukorékol', 'egyet|kuncog', 'egyet|kurjant', 'egyet|küld',
                        'egyet|lapátol', 'egyet|lapoz', 'egyet|lebbent', 'egyet|legyint', 'egyet|lehel',
                        'egyet|lélegezik', 'egyet|loccsan', 'egyet|lop', 'egyet|lovagol', 'egyet|lő', 'egyet|lök',
                        'egyet|lyukaszt', 'egyet|marad', 'egyet|megesz', 'egyet|megy', 'egyet|ment', 'egyet|mennydörög',
                        'egyet|minősít', 'egyet|mordul', 'egyet|mosolyog', 'egyet|mozdul', 'egyet|mozog', 'egyet|mulat',
                        'egyet|mutat', 'egyet|nevesít', 'egyet|nevet', 'egyet|néz', 'egyet|növel', 'egyet|nyal',
                        'egyet|nyekereg', 'egyet|nyerít', 'egyet|nyikkan', 'egyet|nyög', 'egyet|nyújt',
                        'egyet|nyújtózik', 'egyet|nyújtózkodik', 'egyet|olvas', 'egyet|ordít', 'egyet|őriz',
                        'egyet|parádézik', 'egyet|parancsol', 'egyet|pattan', 'egyet|pihen', 'egyet|pipil',
                        'egyet|pislákol', 'egyet|pislog', 'egyet|pótol', 'egyet|próbál', 'egyet|próbálkozik',
                        'egyet|prüszköl', 'egyet|rajzol', 'egyet|rándít', 'egyet|rándul', 'egyet|ránt', 'egyet|rebben',
                        'egyet|reccsen', 'egyet|remél', 'egyet|rendel', 'egyet|részesít', 'egyet|ringat',
                        'egyet|robban', 'egyet|röpköd', 'egyet|rúg', 'egyet|sajnál', 'egyet|sebez', 'egyet|sétál',
                        'egyet|sikolt', 'egyet|simít', 'egyet|sípol', 'egyet|sír', 'egyet|sorsol', 'egyet|suhint',
                        'egyet|szakajt', 'egyet|szakít', 'egyet|szalutál', 'egyet|szellent', 'egyet|szerez',
                        'egyet|szervez', 'egyet|szipákol', 'egyet|szipog', 'egyet|szippant', 'egyet|szól',
                        'egyet|szundikál', 'egyet|szundít', 'egyet|szundizik', 'egyet|szusszan', 'egyet|támogat',
                        'egyet|tanít', 'egyet|tapsol', 'egyet|tárgyal', 'egyet|tárol', 'egyet|tartalmaz',
                        'egyet|tartozik', 'egyet|taszít', 'egyet|teázik', 'egyet|tehet', 'egyet|teker',
                        'egyet|telefonál', 'egyet|telepít', 'egyet|teljesít', 'egyet|tér', 'egyet|tervez',
                        'egyet|tesz', 'egyet|téved', 'egyet|tojik', 'egyet|tol', 'egyet|toppant', 'egyet|tölt',
                        'egyet|töröl', 'egyet|törül', 'egyet|túrázik', 'egyet|tűz', 'egyet|ugat', 'egyet|ugrik',
                        'egyet|úszik', 'egyet|utál', 'egyet|utaz', 'egyet|üt', 'egyet|üvölt', 'egyet|vág',
                        'egyet|vakar', 'egyet|vakaródzik', 'egyet|vakkant', 'egyet|vállal', 'egyet|vált', 'egyet|vár',
                        'egyet|vásárol', 'egyet|ver', 'egyet|veszélyeztet', 'egyet|vijjog', 'egyet|villan',
                        'egyet|vizsgál', 'egyet|vonul', 'egyet|zökken', 'egyet|zöttyen', 'egyet|zuhan', 'egyet|zümmög',
                        'egyet|zsörtöl', 'együtt|alakít', 'együtt|alkalmaz', 'együtt|alkot', 'együtt|álmodik',
                        'együtt|alszik', 'együtt|bálozik', 'együtt|barangol', 'együtt|beszél', 'együtt|bíz',
                        'együtt|bővít', 'együtt|bulizik', 'együtt|dicsér', 'együtt|dolgoztat', 'együtt|dönt',
                        'együtt|drukkol', 'együtt|ebédel', 'együtt|edz', 'együtt|élvez', 'együtt|emleget',
                        'együtt|emlékezik', 'együtt|említ', 'együtt|énekel', 'együtt|épít', 'együtt|érkezik',
                        'együtt|értékel', 'együtt|érvényesül', 'együtt|eszik', 'együtt|farsangol', 'együtt|folytat',
                        'együtt|formál', 'együtt|forog', 'együtt|fúj', 'együtt|fut', 'együtt|gondol',
                        'együtt|gondolkodik', 'együtt|gondolkozik', 'együtt|gyakorol', 'együtt|gyúr', 'együtt|hajt',
                        'együtt|hallgat', 'együtt|használ', 'együtt|hirdet', 'együtt|hív', 'együtt|hord',
                        'együtt|imádkozik', 'együtt|indul', 'együtt|ír', 'együtt|irt', 'együtt|javít', 'együtt|kacag',
                        'együtt|kér', 'együtt|keres', 'együtt|kiált', 'együtt|kínál', 'együtt|kóstolgat', 'együtt|költ',
                        'együtt|köszönt', 'együtt|követ', 'együtt|követel', 'együtt|közvetít', 'együtt|küzd',
                        'együtt|lakik', 'együtt|lakomázik', 'együtt|lapozgat', 'együtt|lát', 'együtt|látogat',
                        'együtt|lobog', 'együtt|lóg', 'együtt|marad', 'együtt|megy', 'együtt|mond', 'együtt|mozog',
                        'együtt|munkálkodik', 'együtt|mutatkozik', 'együtt|nevel', 'együtt|néz', 'együtt|nézeget',
                        'együtt|olvas', 'együtt|ölt', 'együtt|öregbít', 'együtt|őriz', 'együtt|örül', 'együtt|párol',
                        'együtt|pihen', 'együtt|rendez', 'együtt|sajnál', 'együtt|segít', 'együtt|simogat',
                        'együtt|sír', 'együtt|skandál', 'együtt|sugároz', 'együtt|szállít', 'együtt|számol',
                        'együtt|szárnyal', 'együtt|szaval', 'együtt|szavaz', 'együtt|szenved', 'együtt|szerepel',
                        'együtt|szív', 'együtt|szolgál', 'együtt|szorgoskodik', 'együtt|tanácskozik', 'együtt|táncol',
                        'együtt|tanul', 'együtt|tanulmányoz', 'együtt|tárol', 'együtt|tart', 'együtt|teljesít',
                        'együtt|termeszt', 'együtt|tesz', 'együtt|tevékenykedik', 'együtt|történik', 'együtt|treníroz',
                        'együtt|utaz', 'együtt|üdül', 'együtt|üdvözöl', 'együtt|ügyel', 'együtt|ül', 'együtt|ünnepel',
                        'együtt|választ', 'együtt|vállal', 'együtt|vár', 'együtt|várakozik', 'együtt|véd',
                        'együtt|végez', 'együtt|versenyez', 'együtt|vezényel', 'együtt|visz', 'együtt|zeng', 'elé|ad',
                        'elé|állít', 'elé|bukkan', 'elé|épül', 'elé|ereszkedik', 'elé|fárad', 'elé|fut', 'elé|hagy',
                        'elé|hív', 'elé|idéz', 'elé|jön', 'elé|kanyarog', 'elé|kerül', 'elé|készít', 'elé|köt',
                        'elé|lép', 'elé|megy', 'elé|mozdít', 'elé|nyújt', 'elé|pattan', 'elé|penderül', 'elé|rak',
                        'elé|rohan', 'elé|segít', 'elé|siet', 'elé|szalad', 'elé|szólít', 'elé|szökken', 'elé|szül',
                        'elé|tár', 'elé|tart', 'elé|tárul', 'elé|telepedik', 'elé|terjed', 'elé|terjeszt', 'elé|tesz',
                        'elé|tol', 'elé|tornyosul', 'elé|tűnik', 'elé|ugrik', 'elé|vár', 'elé|vet', 'elé|vetít',
                        'elé|vezet', 'elé|zuhan', 'ellen|debütál', 'ellen|indít', 'ellen|indul', 'ellen|intéz',
                        'ellen|lát', 'ellen|mond', 'ellen|nyújt', 'ellent|áll', 'ellen|tesz', 'ellent|hoz',
                        'ellent|szegül', 'ellent|vet', 'ellen|vág', 'ellen|véd', 'észre|alapoz', 'észre|hallgat',
                        'észre|hivatkozik', 'észre|jön', 'észre|panaszkodik', 'észre|siklik', 'észre|szül',
                        'észre|vall', 'észre|veszt', 'észre|vet', 'észre|vét', 'földet|ad', 'földet|adományoz',
                        'földet|ajándékoz', 'földet|ajánl', 'földet|ás', 'földet|áztat', 'földet|bérel',
                        'földet|birtokol', 'földet|borít', 'földet|dob', 'földet|dobál', 'földet|ég', 'földet|érint',
                        'földet|ért', 'földet|eszik', 'földet|exportál', 'földet|fal', 'földet|fertőtlenít',
                        'földet|fest', 'földet|foglal', 'földet|forgat', 'földet|gereblyéz', 'földet|gyarmatosít',
                        'földet|hagyományoz', 'földet|hajt', 'földet|harap', 'földet|hasznosít', 'földet|haszonbérel',
                        'földet|helyettesít', 'földet|helyez', 'földet|hint', 'földet|hord', 'földet|hoz', 'földet|húz',
                        'földet|igényel', 'földet|ígér', 'földet|jár', 'földet|jelent', 'földet|juttat',
                        'földet|kémlel', 'földet|kér', 'földet|keres', 'földet|készít', 'földet|kínál', 'földet|kiokád',
                        'földet|követel', 'földet|küld', 'földet|lapátol', 'földet|lát', 'földet|megy',
                        'földet|művel', 'földet|néz', 'földet|nyom', 'földet|oltalmaz', 'földet|oszt', 'földet|öntöz',
                        'földet|örököl', 'földet|pusztít', 'földet|rak', 'földet|reccsen', 'földet|rögzít',
                        'földet|seper', 'földet|söpör', 'földet|súrol', 'földet|szállít', 'földet|számít',
                        'földet|szerez', 'földet|szór', 'földet|szórat', 'földet|szurkol', 'földet|takar',
                        'földet|tanulmányoz', 'földet|tapos', 'földet|tart', 'földet|tehet', 'földet|tekint',
                        'földet|teremt', 'földet|terít', 'földet|tesz', 'földet|tölt', 'földet|tömörít', 'földet|tör',
                        'földet|trágyáz', 'földet|túr', 'földet|üdít', 'földet|ültet', 'földet|vált',
                        'földet|változtat', 'földet|varázsol', 'földet|vásárol', 'földet|verdes', 'földet|vesz',
                        'földet|veszt', 'földet|vet', 'fölé|csap', 'fölé|emel', 'fölé|hajol', 'fölé|helyez',
                        'fölé|rendel', 'fölé|virít', 'följebb|áll', 'följebb|árul', 'följebb|beszél', 'följebb|csap',
                        'följebb|csúszik', 'följebb|emel', 'följebb|emelkedik', 'följebb|húz', 'följebb|húzódik',
                        'följebb|húzódzkodik', 'följebb|jár', 'följebb|jön', 'följebb|jut', 'följebb|kapaszkodik',
                        'följebb|keres', 'följebb|kerül', 'följebb|kúszik', 'följebb|lakik', 'följebb|lép',
                        'följebb|mászik', 'följebb|megy', 'följebb|mozdul', 'följebb|mozog', 'följebb|néz',
                        'följebb|nyúl', 'följebb|ránt', 'följebb|reppen', 'följebb|száguldozik', 'följebb|szeg',
                        'följebb|szökik', 'följebb|tol', 'följebb|tornyosodik', 'följebb|vág', 'följebb|visz',
                        'följebb|vitet', 'helyben|ad', 'helyben|adódik', 'helyben|ajándékoz', 'helyben|alkot',
                        'helyben|áll', 'helyben|árul', 'helyben|árusít', 'helyben|azonosít', 'helyben|bízik',
                        'helyben|bizonyul', 'helyben|bocsát', 'helyben|csatlakozik', 'helyben|dolgozik',
                        'helyben|ebédel', 'helyben|él', 'helyben|élvez', 'helyben|épít', 'helyben|érez',
                        'helyben|éreztet', 'helyben|érkezik', 'helyben|értékel', 'helyben|értékesít', 'helyben|értesül',
                        'helyben|érvényesül', 'helyben|fejleszt', 'helyben|fényez', 'helyben|fizet',
                        'helyben|fogad', 'helyben|foglal', 'helyben|foglalkoztat', 'helyben|fogyaszt',
                        'helyben|folyik', 'helyben|folytat', 'helyben|forog', 'helyben|főz', 'helyben|futtat',
                        'helyben|füstöl', 'helyben|gazdálkodik', 'helyben|gondoskodik', 'helyben|gyárt',
                        'helyben|halad', 'helyben|hallik', 'helyben|hasznosul', 'helyben|hivatkozik',
                        'helyben|indítványoz', 'helyben|indul', 'helyben|intéz', 'helyben|ír', 'helyben|ítélkezik',
                        'helyben|jár', 'helyben|jelez', 'helyben|jogosít', 'helyben|kap', 'helyben|kedveskedik',
                        'helyben|keletkezik', 'helyben|kényszerít', 'helyben|képződik', 'helyben|kér', 'helyben|keres',
                        'helyben|kerül', 'helyben|készít', 'helyben|készül', 'helyben|kezdeményez', 'helyben|kezel',
                        'helyben|kísér', 'helyben|komposztál', 'helyben|köszön', 'helyben|köt', 'helyben|következik',
                        'helyben|kritizál', 'helyben|lát', 'helyben|marasztal', 'helyben|működik', 'helyben|működtet',
                        'helyben|növekszik', 'helyben|növel', 'helyben|nyaral', 'helyben|nyílik', 'helyben|nyújt',
                        'helyben|okoz', 'helyben|olvas', 'helyben|omol', 'helyben|oszt', 'helyben|ölt',
                        'helyben|raboskodik', 'helyben|részesít', 'helyben|részesül', 'helyben|segít',
                        'helyben|sugároz', 'helyben|süt', 'helyben|szab', 'helyben|szabályoz', 'helyben|számol',
                        'helyben|székel', 'helyben|szerepel', 'helyben|szervez', 'helyben|szolgáltat', 'helyben|sző',
                        'helyben|szörnyethal', 'helyben|szúr', 'helyben|születik', 'helyben|tájékoztat',
                        'helyben|tanul', 'helyben|tapasztal', 'helyben|tart', 'helyben|tartalmaz', 'helyben|teremt',
                        'helyben|tesz', 'helyben|tesztel', 'helyben|tevékenykedik', 'helyben|történik',
                        'helyben|üzemel', 'helyben|választ', 'helyben|válik', 'helyben|vállal', 'helyben|vár',
                        'helyben|vásárol', 'helyben|végez', 'helyben|vesz', 'helyben|vezet', 'helyben|vigyáz',
                        'helyben|vizsgál', 'helyben|vizsgázik', 'helyben|vonul', 'helyben|zajlik', 'helyt|ás',
                        'helyt|biztosít', 'helyt|helyettesít', 'helyt|időzik', 'helyt|készül', 'helyt|kezdeményez',
                        'helyt|köszön', 'helyt|köt', 'helyt|kötelez', 'helyt|magyarázkodik', 'helyt|marad',
                        'helyt|működik', 'helyt|nyílik', 'helyt|nyom', 'helyt|szerepel', 'helyt|szervez',
                        'helyt|szorít', 'helyt|születik', 'helyt|történik', 'helyt|válhatik', 'helyt|vizsgál',
                        'hoppon|marad', 'itt|felejt', 'itt|felejtkezik', 'itt|hagy', 'itt|jár', 'itt|marad',
                        'itt|ragad', 'jól|áll', 'jól|fejlik', 'jól|ismer', 'jól|jellemez', 'jól|passzol',
                        'jól|reprezentál', 'jól|sikerül', 'jól|táplál', 'jót|ad', 'jót|alakít', 'jót|állít',
                        'jót|álmodik', 'jót|beszélget', 'jót|bulizik', 'jót|cselekedik', 'jót|cselekszik',
                        'jót|csinál', 'jót|derül', 'jót|eredményez', 'jót|eszik', 'jót|eszközöl', 'jót|hall',
                        'jót|hoz', 'jót|improvizál', 'jót|iszik', 'jót|jelent', 'jót|jelez', 'jót|jósol',
                        'jót|jövendöl', 'jót|kap', 'jót|kereskedik', 'jót|köszön', 'jót|lát', 'jót|láttat',
                        'jót|mesél', 'jót|mulat', 'jót|mutat', 'jót|nevet', 'jót|olvas', 'jót|remél', 'jót|röhög',
                        'jót|sejtet', 'jót|sugall', 'jót|szül', 'jót|tanul', 'jót|tart', 'jót|tartogat', 'jót|tehet',
                        'jót|teremt', 'jót|uzsonnál', 'jót|vár', 'jót|végez', 'jót|vél', 'jót|veszít', 'jóvá|válik',
                        'karban|alakul', 'karban|beszél', 'karban|jelent', 'karban|sopánkodik', 'karban|szól',
                        'karban|üvölt', 'karban|vartyog', 'kelletik|kell', 'keresztül|feldolgoz', 'késztet|készt',
                        'kétségbe|áll', 'kétségbe|ejt', 'kétségbe|fordít', 'kétségbe|formál', 'kétségbe|hirdet',
                        'kétségbe|jelent', 'kétségbe|lát', 'kétségbe|menekül', 'kétségbe|néz', 'kétségbe|roskad',
                        'kétségbe|segít', 'kétségbe|tapogatózik', 'kétségbe|taszít', 'kétségbe|tesz',
                        'kétségbe|történik', 'kétségbe|vezet', 'kétségbe|vonódik', 'kinn|áll', 'kinn|árul',
                        'kinn|csinál', 'kinn|dalol', 'kinn|esik', 'kinn|fél', 'kinn|hagy', 'kinn|marad', 'kinn|poshad',
                        'kinn|rendez', 'kinn|susog', 'kinn|süt', 'kinn|tartózkodik', 'kinn|tölt', 'kinn|vár',
                        'kinn|zörög', 'kint|eszik', 'kint|feled', 'kint|felejt', 'kint|marad', 'kint|ragad',
                        'kint|reked', 'kölcsön|ballag', 'kölcsön|bérel', 'kölcsön|biztosít', 'kölcsön|bont',
                        'kölcsön|csökken', 'kölcsön|csökkent', 'kölcsön|emel', 'kölcsön|forog', 'kölcsön|használ',
                        'kölcsön|hat', 'kölcsön|helyettesít', 'kölcsön|játszik', 'kölcsön|javasol', 'kölcsön|jön',
                        'kölcsön|kerül', 'kölcsön|közlekedik', 'kölcsön|menekül', 'kölcsön|minősül', 'kölcsön|nyújt',
                        'kölcsön|önöz', 'kölcsön|segít', 'kölcsön|szolgál', 'kölcsön|találkozik', 'kölcsön|támogat',
                        'kölcsön|tartalmaz', 'kölcsön|történik', 'kölcsön|válik', 'kölcsön|változik', 'kölcsön|von',
                        'közben|csörög', 'közben|jön', 'közzé|ad', 'közzé|állít', 'közzé|befolyásol', 'közzé|emel',
                        'közzé|esik', 'közzé|eszik', 'közzé|helyettesít', 'közzé|illik', 'közzé|javasol', 'közzé|kerül',
                        'közzé|kínálkozik', 'közzé|számít', 'közzé|tartozik', 'közzé|tétetik', 'közzé|történik',
                        'közzé|vár', 'közzé|végez', 'létre|ad', 'létre|építtet', 'létre|gyúl', 'létre|hajt',
                        'létre|használ', 'létre|irányul', 'létre|jelent', 'létre|kárhoztat', 'létre|kelt',
                        'létre|nyer', 'létre|rögzít', 'létre|szerepel', 'létre|szervez', 'létre|szólít', 'létre|tart',
                        'létre|teremt', 'létre|vesz', 'létre|zár', 'mögé|tesz', 'nagyot|ad', 'nagyot|alakít',
                        'nagyot|álmodik', 'nagyot|alszik', 'nagyot|arat', 'nagyot|ásít', 'nagyot|bakizik',
                        'nagyot|bámul', 'nagyot|beszélget', 'nagyot|biciklizik', 'nagyot|bizonyít', 'nagyot|bokszol',
                        'nagyot|bólint', 'nagyot|botlik', 'nagyot|böfög', 'nagyot|bukik', 'nagyot|bulizik',
                        'nagyot|civilizálódik', 'nagyot|csap', 'nagyot|csattan', 'nagyot|csendül', 'nagyot|csinál',
                        'nagyot|csíp', 'nagyot|csobban', 'nagyot|csorbít', 'nagyot|csönget', 'nagyot|csúszik',
                        'nagyot|dob', 'nagyot|dobbant', 'nagyot|döndül', 'nagyot|dördül', 'nagyot|dörög',
                        'nagyot|dörren', 'nagyot|dug', 'nagyot|durrant', 'nagyot|ébred', 'nagyot|élvez', 'nagyot|emel',
                        'nagyot|emelkedik', 'nagyot|erősödik', 'nagyot|esik', 'nagyot|eszik', 'nagyot|fejlik',
                        'nagyot|fejlődik', 'nagyot|fékez', 'nagyot|fészkelődik', 'nagyot|firkál', 'nagyot|focizik',
                        'nagyot|fohászkodik', 'nagyot|folytat', 'nagyot|fordít', 'nagyot|fúj', 'nagyot|fut',
                        'nagyot|füttyent', 'nagyot|gágog', 'nagyot|gondol', 'nagyot|gondolkozik', 'nagyot|gyalogol',
                        'nagyot|hajt', 'nagyot|halad', 'nagyot|hálálkodik', 'nagyot|hallgat', 'nagyot|hanyatlik',
                        'nagyot|harap', 'nagyot|hazudik', 'nagyot|hibáz', 'nagyot|hibázik', 'nagyot|horkan',
                        'nagyot|hördül', 'nagyot|húz', 'nagyot|indul', 'nagyot|invesztál', 'nagyot|iszik', 'nagyot|jár',
                        'nagyot|játszik', 'nagyot|javít', 'nagyot|javul', 'nagyot|jelképez', 'nagyot|kanyarodik',
                        'nagyot|káromkodik', 'nagyot|kaszál', 'nagyot|kavar', 'nagyot|kiált', 'nagyot|kockáztat',
                        'nagyot|koppan', 'nagyot|kortyol', 'nagyot|köp', 'nagyot|köszön', 'nagyot|kurjant',
                        'nagyot|lebben', 'nagyot|legyint', 'nagyot|lélegezik', 'nagyot|lélegzik', 'nagyot|lendít',
                        'nagyot|lendül', 'nagyot|lép', 'nagyot|lobban', 'nagyot|loccsan', 'nagyot|lök', 'nagyot|markol',
                        'nagyot|megy', 'nagyot|mennydörög', 'nagyot|merészel', 'nagyot|mond', 'nagyot|mordul',
                        'nagyot|mosolyog', 'nagyot|mozdít', 'nagyot|mulat', 'nagyot|nevel', 'nagyot|nő',
                        'nagyot|nyekken', 'nagyot|nyerít', 'nagyot|nyög', 'nagyot|nyújt', 'nagyot|nyújtózik',
                        'nagyot|nyújtózkodik', 'nagyot|ordít', 'nagyot|pattan', 'nagyot|percen', 'nagyot|pillant',
                        'nagyot|ránt', 'nagyot|reccsen', 'nagyot|reggelizik', 'nagyot|repül', 'nagyot|rikkant',
                        'nagyot|rikolt', 'nagyot|robban', 'nagyot|robbant', 'nagyot|romlik', 'nagyot|röhög',
                        'nagyot|röppen', 'nagyot|rúg', 'nagyot|sebez', 'nagyot|sétál', 'nagyot|sikolt',
                        'nagyot|szellent', 'nagyot|szippant', 'nagyot|szisszen', 'nagyot|szív', 'nagyot|szól',
                        'nagyot|szusszan', 'nagyot|szusszant', 'nagyot|tart', 'nagyot|taszít', 'nagyot|távozik',
                        'nagyot|teljesít', 'nagyot|teremt', 'nagyot|tesz', 'nagyot|toccsan', 'nagyot|tüsszent',
                        'nagyot|ugrik', 'nagyot|úszik', 'nagyot|üt', 'nagyot|üvölt', 'nagyot|vág', 'nagyot|válaszol',
                        'nagyot|vált', 'nagyot|változtat', 'nagyot|vénül', 'nagyot|verődik', 'nagyot|veszt',
                        'nagyot|villan', 'nagyot|visít', 'nagyot|vív', 'nagyot|zökken', 'nagyot|zsebel',
                        'nyilván|beszélget', 'nyilván|gondol', 'nyilván|kerül', 'nyilván|követ', 'nyilván|lát',
                        'nyilván|munkál', 'nyilván|tartozik', 'odébb|fut', 'odébb|húz', 'odébb|tol', 'odébb|vonul',
                        'ott|alszik', 'ott|cselekedik', 'ott|érez', 'ott|eszik', 'ott|fekszik', 'ott|fogad',
                        'ott|forog', 'ott|hall', 'ott|hord', 'ott|ismer', 'ott|játszik', 'ott|jellemez', 'ott|kap',
                        'ott|keres', 'ott|kísér', 'ott|köszönt', 'ott|lakik', 'ott|lát', 'ott|munkál', 'ott|ont',
                        'ott|őriz', 'ott|pusztul', 'ott|ragad', 'ott|rejtezik', 'ott|rendez', 'ott|szerepel',
                        'ott|tart', 'ott|tölt', 'ott|választ', 'ott|vár', 'ott|végez', 'óva|billen', 'óva|tekereg',
                        'óva|ügyel', 'összébb|húz', 'összébb|simul', 'összébb|szorul', 'pofon|érkezik', 'pofon|jár',
                        'pofon|segít', 'pofon|térít', 'pofon|üt', 'pórul|találkozik', 'rendre|ad', 'rendre|cselekedik',
                        'rendre|dolgozik', 'rendre|int', 'rendre|jelöl', 'rendre|kap', 'rendre|kényszerít',
                        'rendre|kerül', 'rendre|mérséklődik', 'rendre|mondogat', 'rendre|okoz', 'rendre|szerez',
                        'rendre|tagozódik', 'rendre|tanít', 'rendre|tart', 'rendre|tartalmaz', 'rendre|törekszik',
                        'rendre|vonatkozik', 'síkra|emel', 'síkra|épít', 'síkra|ér', 'síkra|folytatódik',
                        'síkra|helyez', 'síkra|helyeződik', 'síkra|kerül', 'síkra|lép', 'síkra|redukál', 'síkra|terel',
                        'síkra|terelődik', 'síkra|üdvözöl', 'szabadjára|ereszt', 'szabadjára|hagy', 'szabadjára|indít',
                        'szabadjára|keres', 'szabadlábra|bocsát', 'szabadlábra|dönt', 'szabadlábra|ítél',
                        'szabadlábra|kér', 'szabadlábra|kerül', 'szabadlábra|vár', 'szabadlábra|visel', 'számba|ad',
                        'számba|alkalmaz', 'számba|áll', 'számba|csoportosít', 'számba|csorog', 'számba|csúszik',
                        'számba|derül', 'számba|dob', 'számba|dönt', 'számba|folyik', 'számba|fröccsen',
                        'számba|gondol', 'számba|helyez', 'számba|indít', 'számba|jön', 'számba|jut', 'számba|kerül',
                        'számba|költözik', 'számba|küld', 'számba|lóg', 'számba|olvas', 'számba|publikál',
                        'számba|sürget', 'számba|szolgál', 'számba|találkozik', 'számba|tart', 'számba|tartozik',
                        'számba|teremt', 'számba|tesz', 'számba|vezet', 'széjjelebb|húz', 'széjjelebb|húzódik',
                        'széjjelebb|nyílik', 'széjjelebb|nyit', 'széjjelebb|nyitódik', 'széjjelebb|tár', 'szemben|áll',
                        'szemre|használ', 'szemre|helyez', 'szemre|jellemez', 'szemre|kerül', 'szemre|köt',
                        'szemre|követ', 'szemre|különbözik', 'szemre|látszik', 'szemre|vall', 'szemre|változik',
                        'szemre|vásárol', 'szemre|vesz', 'szemügyre|bizonyul', 'szemügyre|fűz', 'szemügyre|ismer',
                        'szemügyre|jön', 'szemügyre|kezdődik', 'szemügyre|következik', 'szemügyre|lát',
                        'szemügyre|méltányol', 'szemügyre|nyújt', 'szemügyre|vet', 'szörnyet|csinál', 'szörnyet|hall',
                        'szörnyet|követ', 'szörnyet|nevez', 'szörnyet|szül', 'szörnyet|tapasztal', 'tekintet|tekint',
                        'tetszik|tetszet', 'torkig|ér', 'torkig|undorodik', 'torkig|úszik', 'tudomásul|biztosít',
                        'tudomásul|dönt', 'tudomásul|ér', 'tudomásul|értesít', 'tudomásul|fejleszt',
                        'tudomásul|folytat', 'tudomásul|helyez', 'tudomásul|hív', 'tudomásul|igazol',
                        'tudomásul|javasol', 'tudomásul|jelentkezik', 'tudomásul|jut', 'tudomásul|kér',
                        'tudomásul|készít', 'tudomásul|kínál', 'tudomásul|köszön', 'tudomásul|megy',
                        'tudomásul|módosul', 'tudomásul|óv', 'tudomásul|szolgál', 'tudomásul|tesz',
                        'tudomásul|történik', 'tudomásul|utal', 'tudomásul|válik', 'tudomásul|vár', 'tudomásul|vétet',
                        'tudtul|ad', 'után|fut', 'után|jár', 'után|keresgél', 'után|közöl', 'után|von',
                        'útba|csatlakozik', 'útba|ejtet', 'útba|ér', 'útba|esik', 'útba|fordul', 'útba|fut',
                        'útba|indít', 'útba|indul', 'útba|nyit', 'útba|tagol', 'útba|torkollik', 'útba|vezet',
                        'véget|ér', 'zokon|esik', 'zöldágra|jut', 'együtt|hál',
                        'észhez|tér', 'észhez|térít', 'észre|tér', 'észre|térít', 'zöldágra|vergődik', 'észhez|kap'
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
      'oda|utazik', 'vissza|kocog', 'el|kurvul', 'le|hugyoz', 'meg|örvendeztetet', 'össze|fos', 'össze-össze|néz',
      'abba|hagyat', 'agyon|dolgoztat', 'agyon|fagy', 'agyon|zsúfol', 'alá|értékel', 'alá|folyik', 'alá|hull',
      'alá|nyal', 'alá|pincéz', 'által|cikázik', 'által|jár', 'által|lát', 'alul|exponál', 'át|álmodik', 'át|csomagol',
      'át|feszít', 'át|fűlik', 'át|háramlik', 'át|hevít', 'át|hull', 'át|hurcolkodik', 'át|hurkol', 'át|hűt',
      'át|kopogtat', 'át|lábol', 'át|lapol', 'át|mázol', 'át|nyilallik', 'át|nyomódik', 'át|ömlik', 'át|örököl',
      'át|szorít', 'át|üzen', 'át|varr', 'be|avatódik', 'be-be|csap', 'be-be|néz', 'be|bifláz', 'be|bolondít',
      'be|bonyolódik', 'be|boronál', 'be|boroz', 'be|bőrösödik', 'be|citál', 'be|cumiz', 'be|csajoz', 'be|csavarog',
      'be|csepegtet', 'be|cserepez', 'be|cserkel', 'be|csiccsent', 'be|csődít', 'be|csuk', 'be|csűr', 'be|daciz',
      'be|erdősödik', 'be|füstöl', 'be|füvesít', 'be|gazol', 'be|gyűlik', 'be|hat', 'be|hintőporoz', 'be|hízelgi',
      'be|illatoz', 'be|irányít', 'be|járogat', 'be|kalandoz', 'be|kanyarít', 'be|kávézik', 'be|kormányoz', 'be|koszol',
      'bele|avat', 'be|lebódul', 'bele|csempész', 'bele|fordít', 'bele|fülled', 'bele|hallatszik', 'be|lejt',
      'bele|kábul', 'bele|kékül', 'bele|lop', 'bele|mered', 'be|lépet', 'bele|pistul', 'bele|sajog', 'bele|tud',
      'bele|ugrat', 'bele|vasal', 'bele|vegyít', 'bele|vénül', 'bele|zabál', 'bele|zökken', 'be|masíroz', 'be|mászkál',
      'be|paliz', 'be|párol', 'be|pillézik', 'be|porosodik', 'be|pucol', 'be|rosál', 'be|rukkol', 'be|sajtol',
      'be|seggel', 'be|sereglik', 'be|slisszol', 'be|suttyan', 'be|süvölt', 'be|szalonnázik', 'be|szekundázik',
      'be|szemtelenkedik', 'be|szeszel', 'be|szuszakol', 'be|terelget', 'be|tokozódik', 'be|tömődik', 'be|tüzel',
      'be|ügyeskedik', 'be|vérez', 'be|vetődik', 'be|zápul', 'be|zúg', 'be|zsindelyez', 'egybe|áll', 'egybe|sereglik',
      'el|ácsorog', 'el|adódik', 'el|álldogál', 'el|álmodozik', 'el|aprít', 'el|árvereztet', 'el|aszik', 'el|bajlódik',
      'el|barmol', 'el|bizonytalankodik', 'el|bokrosodik', 'el|bürokratizálódik', 'el|csemegézik', 'el|csenevészedik',
      'el|csinál', 'el|csörömpöl', 'el|csörtet', 'el-el|akad', 'el-el|gyönyörködik', 'el|erőtlenít', 'el|érzékenyedik',
      'el|esteledik', 'el|fakad', 'el|feslik', 'el|fuserál', 'el|galoppoz', 'el|gennyesedik', 'el|gépiesít', 'el|hasít',
      'el|hegedül', 'el|hidegít', 'el|irtózik', 'el|iszaposodik', 'el|iszogat', 'el|jegesedik', 'el|kapál',
      'el|karikázik', 'el|kártyáz', 'el|kérdez', 'el|keskenyül', 'el|komorít', 'el|konspirál', 'el|korcsosodik',
      'el|korhaszt', 'el|labdázgat', 'el|lángol', 'el|lankaszt', 'el|laposít', 'el|lötyög', 'el|mállaszt', 'el|mellőz',
      'el|mocsarasodik', 'el|nadrágol', 'el|németesedik', 'el|néptelenít', 'el|nevel', 'el|nyúz', 'el|oxál',
      'elő|hívódik', 'elő|parancsol', 'előre|áll', 'előre|csapódik', 'előre|csuklik', 'előre|hullik', 'előre|mászik',
      'előre|szól', 'elő|számol', 'elő|tódul', 'elő|totyog', 'el|perel', 'el|pilled', 'el|piszmog', 'el|prédál',
      'el|rakodik', 'el|reppen', 'el|rikkantja', 'elwrombol', 'el|rútít', 'el|sápaszt', 'el|savanyodik',
      'el|sekélyesít', 'el|sinkófál', 'el|számítja', 'el|szánt', 'el|szemtelenedik', 'el|szenesít', 'el|színtelenedik',
      'el|szótlanodik', 'el|tájol', 'el|tájolódik', 'el|terebélyesedik', 'el|tetvesedik', 'el|totyog', 'el|tördel',
      'el|tréfál', 'el|tréfálkozik', 'el|ugat', 'el|undorít', 'el|undorodik', 'el|ülhet', 'el|vakar', 'el|vámol',
      'el|városiasodik', 'el|végzi', 'el|vénül', 'el|vihog', 'el|virul', 'el|zsidósodik', 'fel|borzad',
      'fel|bosszankodik', 'fel|bukfencezik', 'fel|burjánzik', 'fel|csókol', 'fel|csuklik', 'fel|dühösít',
      'fel|émelyedik', 'fel|esz', 'fel|fagy', 'fel-fel|néz', 'fel-fel|nyög', 'fel-fel|villant', 'fel|gallyaz',
      'fel|gombolyít', 'fel|gyürkőzik', 'fel|hajózik', 'fel|hat', 'fel|hízik', 'fel|idegesedik', 'fel|iszapolódik',
      'fel|kantároz', 'fel|kérdez', 'fel|köttet', 'fel|kurbliz', 'fel|lármáz', 'fel|látogat', 'fel|málház',
      'fel|mérgesedik', 'fel|mérgesít', 'fel|metél', 'fel|minősít', 'felwöltő', 'fel|puffaszt', 'félre|nyom',
      'félre|tétet', 'fel|ruházkodik', 'fel|sivít', 'fel|stuccol', 'fel|száguld', 'fel|szálkásodik', 'fel|szarvaz',
      'fel|szivárog', 'fel|tárcsáz', 'fel|taszít', 'fel|telefonál', 'fel|telepedik', 'fel|türemlik', 'felül|üt',
      'fel|zavarodik', 'fel|zörget', 'hátra|dug', 'hátra|kacsint', 'hátra|kiált', 'hátra|siklik', 'hátra|taszít',
      'hátra|vonul', 'haza|kéredzkedik', 'haza|néz', 'haza|telepít', 'hozzá|biggyeszt', 'hozzá|támaszt', 'ide|érzik',
      'ide|hallik', 'ide|húz', 'ide|készít', 'ide|zár', 'jót|áll', 'keresztül|erőszakol', 'keresztül|rág',
      'ki|állíttat', 'ki|apaszt', 'ki|ázik', 'ki|bánik', 'ki|bombáz', 'ki|böffent', 'ki|bökkent', 'ki|böngész',
      'ki|csapong', 'ki|cserepesedik', 'ki|csesz', 'ki|csődül', 'ki|csurran', 'ki|csüng', 'ki|dülled', 'ki|érzik',
      'ki|faszol', 'ki|fen', 'ki|ficamít', 'ki|forog', 'ki|glancol', 'ki|gombolódik', 'ki|hajszol', 'ki|hasogat',
      'ki|hesseget', 'ki|híresztel', 'ki|hizlal', 'ki|ikszel', 'ki|józanul', 'ki|kászolódik', 'ki-ki|hagy', 'ki-ki|néz',
      'ki|kosaraz', 'ki|köttet', 'ki|lélegez', 'ki|manikűröz', 'ki|marjul', 'ki|maszkíroz', 'ki|mosakodik',
      'ki|nyiffant', 'ki|okád', 'ki|öklendez', 'ki|őröl', 'ki|pállik', 'ki|panaszkodja', 'ki|paríroz', 'ki|paterol',
      'ki|pattogzik', 'ki|pödör', 'ki|purgál', 'ki|puskáz', 'ki|reggeledik', 'ki|reteszel', 'ki|sebesedik',
      'ki|sebesít', 'ki|seprűz', 'ki|sóz', 'ki|spekulál', 'ki|szalaszt', 'ki|szőkül', 'ki|tapsol', 'ki|tekinget',
      'ki|tisztáz', 'ki|türemlik', 'ki|udvarol', 'ki|vásik', 'ki|verődik', 'ki|vicsorít', 'ki|villamosozik',
      'ki|virágoz', 'ki|virrad', 'ki|zeng', 'körbe|szaglász', 'körül|cirógat', 'körül|falaz', 'körül|forog',
      'körül|hajóz', 'körül|hízeleg', 'körül|lovagol', 'körül|párnáz', 'körül|röhög', 'körül|szaglász', 'körül|utazik',
      'le|alkonyodik', 'le|babázik', 'le|barnít', 'le|basz', 'le|biggyed', 'le|cihelődik', 'le|csavarodik',
      'le|cseppen', 'le|csihad', 'le|csinál', 'le|csuklik', 'le|dörgöl', 'le|énekel', 'le|foglalóz', 'le|függönyöz',
      'le|gallyaz', 'le|hamuz', 'le|hengerez', 'le|horgad', 'le|hörpint', 'le|hurcolkodik', 'le|káderez', 'le|kantároz',
      'le|lappad', 'le|lécel', 'le|lépked', 'le|levelez', 'le|malacozik', 'le|meózik', 'le|metél', 'le|mutat',
      'le|nézet', 'le|okád', 'le|óvakodik', 'le|öblöget', 'le|padlózik', 'le|pisál', 'le|piszkol', 'le|pókhálóz',
      'le|poroz', 'le|puskáz', 'le|rókáz', 'le|sárgul', 'le|slattyog', 'le|sompolyog', 'le|sorvad', 'le|suny',
      'le|súrol', 'le|szabadul', 'le|szamaraz', 'le|számítol', 'le|szánkázik', 'le|szegődtet', 'le|szel',
      'le|szerszámoz', 'le|talál', 'le|tántorog', 'le|tart', 'le|tessékel', 'le|tottyan', 'le|tűr', 'le|ugraszt',
      'le|ugrat', 'le|zöttyen', 'meg|acélosodik', 'meg|acéloz', 'meg|áhít', 'meg|bízat', 'meg|borjazik', 'meg|böjtöl',
      'meg|búbol', 'meg|butul', 'meg|büdösödik', 'meg|cukroz', 'meg|dögleszt', 'meg|élesedik', 'meg|emberedik',
      'meg|emberesedik', 'meg|érzik', 'meg|étet', 'meg|fájdít', 'meg|forrósodik', 'meg|fülled', 'meg|gondolkoztat',
      'meg|halkul', 'meg|halványodik', 'meg|hidegedik', 'meg|higgad', 'meg|hólyagosodik', 'meg|ifjít', 'meg|ifjodik',
      'meg|illatosodik', 'meg|iszonyodik', 'meg|ittasul', 'meg|jártat', 'meg|juházik', 'meg|kéret', 'meg|kérvényez',
      'meg|koccan', 'meg|koccant', 'meg|koplaltat', 'meg|koppant', 'meg|kótyagosodik', 'meg|könnyebbít', 'meg|könnyül',
      'meg|kukul', 'meg|leng', 'meg|lóbáz', 'meg|magyarosít', 'meg|makacsolja', 'meg|malacozik', 'meg|másul',
      'meg-meg|csúszik', 'meg-meg|rebben', 'meg-meg|szólal', 'meg-meg|újul', 'meg|mondogat', 'meg|mordul',
      'meg|nadrágol', 'meg|nyomorgat', 'meg|nyuvaszt', 'meg|okosít', 'meg|orvosol', 'meg|öklöz', 'meg|ölelget',
      'meg|öregít', 'meg|őszít', 'meg|pirkad', 'meg|pokrócoz', 'meg|részegszik', 'meg|sápad', 'meg|sodorint',
      'meg|százszoroz', 'meg|szegik', 'meg|szenesedik', 'meg|szitál', 'meg|tágul', 'meg|talpal', 'meg|tetvesedik',
      'meg|traktál', 'meg|ugrat', 'meg|ültet', 'meg|vállasodik', 'meg|vedlik', 'meg|vélt', 'meg|vérez', 'meg|világosul',
      'meg|zördül', 'nagyot|hall', 'neki|durál', 'neki|fohászkodik', 'neki|vadul', 'neki|verődik', 'neki|vörösödik',
      'odább|áll', 'oda|csíp', 'oda|hallik', 'oda|kozmál', 'oda|lapul', 'oda|látszik', 'oda|óvakodik', 'oda|rúg',
      'oda|sompolyog', 'oda|sül', 'oda|teremt', 'oda|vizel', 'össze|bonyolódik', 'össze|bütyköl', 'össze|csapzik',
      'össze|csendül', 'össze|csomóz', 'össze|csoportosul', 'össze|éget', 'össze|fogódzik', 'össze|hajlik',
      'össze|hangzik', 'össze|hasogat', 'össze|igazít', 'össze|írat', 'össze|izzad', 'össze|karistol', 'össze|kel',
      'össze|költöztet', 'össze|lapít', 'össze|mar', 'össze|rabol', 'össze|rondít', 'össze|röffen', 'össze|sajtol',
      'össze|sároz', 'össze|tanul', 'össze|társul', 'össze|töpped', 'össze|vár', 'össze|vérez', 'rá|bízat',
      'rá|bizonyul', 'rá|cseppen', 'rá|dörrent', 'rá|dupláz', 'rá|feledkezik', 'rá|gázol', 'rá|hág', 'rá|hány',
      'rá|hull', 'rá|lök', 'rá|ölt', 'rá|roskad', 'rá|sandít', 'rá|szúr', 'rá|telefonál', 'rá|tipor', 'szemre|vételez',
      'szét|bontakozik', 'szét|csavar', 'szét|hurcol', 'szét|lök', 'tele|beszél', 'tele|ül', 'tova|hömpölyög',
      'tova|vonul', 'túl|csap', 'ujjá|szervez', 'végig|döng', 'végig|hasad', 'végig|hemperedik', 'végig|nyúlik',
      'végig|razziáz', 'végig|reped', 'végig|tántorog', 'vele|jár', 'vissza|csendül', 'vissza|döbben', 'vissza|dörmög',
      'vissza|ijed', 'vissza|indít', 'vissza|ítél', 'vissza|kocsikázik', 'vissza|kuporodik', 'vissza|lépdel',
      'vissza|lóg', 'vissza|lopódzik', 'vissza|masírozik', 'vissza|özönlik', 'vissza|rabol', 'vissza|slattyog',
      'vissza|szolgál', 'vissza|tántorodik', 'vissza|tetszik', 'vissza|torpan', 'vissza|tűz', 'vissza-vissza|csillan',
      'vissza-vissza|fordul', 'fel|virágoz', 'fel|virul', 'fel|vigyáz', 'együtt|áll'
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
                      'rozsdásod', 'tűn', 'felvételiz', 'túlóráz', 'bele|egyez'
                      }

"""
Occur not splitted but only the splitted is OK. And ik suffix is needed
unsplitted -> splitted+ik
"""

prev_and_ik_verbs = \
             {elem.replace('|', ''): (elem + 'ik') for elem in
              {'ki|es', 'rá|fáz', 'meg|esz'}}

del_prev_and_add_ik = {'végig|horgász'}


def is_verb_wrong(verb):
    return verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev \
                    or verb in wrong_verbs3 or verb in bad_forms or verb in bad_forms2


def fix_verb(verb_elem):
    if verb_elem in double_prev_verbs or verb_elem in not_rev_verbs_drop_prev or verb_elem in funny_prev_drop_prev or \
            ('|' in verb_elem and verb_elem.split('|', maxsplit=1)[1] in never_prev_verbs):
        verb_elem = verb_elem.split('|', maxsplit=1)[1]
    elif verb_elem in not_prev_verbs or verb_elem in not_prev_verbs2:  # Remove split
        verb_elem = verb_elem.replace('|', '')
    elif verb_elem in verb_add_ik_suffix:
        verb_elem += 'ik'
    elif verb_elem in del_prev_and_add_ik:
        verb_elem = verb_elem.split('|')[1] + 'ik'

    verb_elem = not_prev_verbs3.get(verb_elem, verb_elem)  # Put split
    verb_elem = funny_ik_replacements.get(verb_elem, verb_elem)  # Funny ik replacement
    verb_elem = prev_and_ik_verbs.get(verb_elem, verb_elem)  # ik+ verbal particle
    if '|' in verb_elem and verb_elem.split('|', maxsplit=1)[1] in light_verb_exception_verbs and\
            verb_elem not in light_verb_exception_verbs_w_prev:
        verb_elem = verb_elem.split('|', maxsplit=1)[1]

    # Should be the last filter
    if '--' in verb_elem:
        verb_elem = verb_elem.replace('--', '-')

    return verb_elem


# Not postpositional phrase -> delete
not_postp = {'adódóan', 'beálltával', 'bekövetkeztével', 'egyidőben', 'elmúltával', 'előrehaladtával', 'eltérően',
             'eredményeképpen', 'eredően', 'fakadóan', 'folyólag', 'függetlenül', 'függően', 'hála', 'illetően',
             'innen', 'ízben', 'köszönhetően', 'következőleg', 'követően', 'közeledtével', 'közöttii', 'lejártával',
             'leteltével', 'létrejöttével', 'megelőzően', 'megfelelően', 'túlmenően', 'unknown', 'végből', 'virradóan',
             'virradólag', 'vonatkozólag'}

# Not postpositional phrase -> case
postp_to_case = {'belőle': '[ELA]', 'inneni': '[NOM]', 'közelében': '[INE]', 'rajta': '[SUP]'}

# "Adjective postpositional phrase" -> case
postp_to_case2 = {'afölötti': '[NOM]', 'alatti': '[NOM]', 'alattiak': '[NOM]', 'alattiakat': '[ACC]',
                  'alattiakban': '[INE]', 'alattiaknak': '[DAT]', 'alattiaknál': '[ADE]', 'alattiakon': '[SUP]',
                  'alattijuktól': '[ABL]', 'alattinak': '[DAT]', 'alattira': '[SUB]', 'alattit': '[ACC]',
                  'alattival': '[INS]', 'alóli': '[NOM]', 'általi': '[NOM]', 'azelőtti': '[NOM]',
                  'azelőttihez': '[ALL]', 'azelőttire': '[SUB]', 'azelőttit': '[ACC]', 'belüli': '[NOM]',
                  'belülinek': '[DAT]', 'belülivel': '[INS]', 'elleni': '[NOM]', 'elleniek': '[NOM]',
                  'ellenieket': '[ACC]', 'ellenit': '[ACC]', 'ellenivel': '[INS]', 'előtti': '[NOM]',
                  'előttihez': '[ALL]', 'előttije': '[NOM]', 'előttinek': '[DAT]', 'előttinél': '[ADE]',
                  'előttire': '[SUB]', 'előttiség': '[NOM]', 'előttit': '[ACC]', 'előttitől': '[ABL]',
                  'előttivé': '[FAC]', 'előttivel': '[INS]', 'ezelőtti': '[NOM]', 'ezelőttiekénél': '[ADE]',
                  'ezelőttiekkel': '[INS]', 'ezelőttiektől': '[ABL]', 'ezelőttihez': '[ALL]', 'ezelőttinek': '[DAT]',
                  'ezelőttinél': '[ADE]', 'ezelőttire': '[SUB]', 'ezelőttit': '[ACC]', 'ezelőttitől': '[ABL]',
                  'ezelőttivel': '[INS]', 'feletti': '[NOM]', 'felettiek': '[NOM]', 'felettieket': '[ACC]',
                  'felettiekkel': '[INS]', 'felettieknek': '[DAT]', 'felettieknél': '[ADE]', 'felettiekről': '[DEL]',
                  'felettije': '[NOM]', 'felettinek': '[DAT]', 'felettire': '[SUB]', 'felettit': '[ACC]',
                  'felettivel': '[INS]', 'felőli': '[NOM]', 'felüli': '[NOM]', 'felüliek': '[NOM]',
                  'felüliekkel': '[INS]', 'felülieknek': '[DAT]', 'felülieknél': '[ADE]', 'felüliekre': '[SUB]',
                  'felülit': '[ACC]', 'fölötti': '[NOM]', 'fölöttiek': '[NOM]', 'fölöttieket': '[ACC]',
                  'fölöttiekkel': '[INS]', 'fölöttieknél': '[ADE]', 'fölöttiekre': '[SUB]', 'fölöttire': '[SUB]',
                  'fölüliek': '[NOM]', 'helyetti': '[NOM]', 'Iránt': '[-]', 'iránti': '[NOM]', 'képesti': '[NOM]',
                  'keresztüli': '[NOM]', 'kívüli': '[NOM]', 'kívüliek': '[NOM]', 'kívülieket': '[ACC]',
                  'kívüliekkel': '[INS]', 'kívüliként': '[FOR]', 'kívülisége': '[NOM]', 'kívüliségére': '[SUB]',
                  'kívülivé': '[FAC]', 'kívülivel': '[INS]', 'körüli': '[NOM]', 'körüliek': '[NOM]',
                  'körüliekkel': '[INS]', 'körüliektől': '[ABL]', 'körülire': '[SUB]', 'körüliről': '[DEL]',
                  'körülit': '[ACC]', 'közbeni': '[NOM]', 'közelről': '[-]', 'közötti': '[NOM]', 'közöttiek': '[NOM]',
                  'közöttiekből': '[ELA]', 'közöttieké': '[NOM]', 'közöttieket': '[ACC]', 'közöttieknek': '[DAT]',
                  'közöttieknél': '[ADE]', 'közöttiekre': '[SUB]', 'közöttin': '[SUP]', 'közöttinek': '[DAT]',
                  'közöttinél': '[ADE]', 'közöttire': '[SUB]', 'közti': '[NOM]', 'köztiek': '[NOM]', 'közüli': '[NOM]',
                  'melletti': '[NOM]', 'miatti': '[NOM]', 'mögötti': '[NOM]', 'nélküli': '[NOM]', 'nélkülibe': '[ILL]',
                  'nélküliből': '[ELA]', 'nélküliek': '[NOM]', 'nélkülieké': '[NOM]', 'nélkülieknél': '[ADE]',
                  'nélküliekre': '[SUB]', 'nélkülinek': '[DAT]', 'nélkülit': '[ACC]', 'nélkülivé': '[FAC]',
                  'számára': '[DAT]', 'számodra': '[DAT]', 'számomra': '[DAT]', 'számunkra': '[DAT]',
                  'szembeni': '[NOM]', 'szemközti': '[NOM]', 'szerinti': '[NOM]', 'szerintiek': '[NOM]',
                  'szerintiekkel': '[INS]', 'szerintiektől': '[ABL]', 'szerintinek': '[DAT]', 'szerintire': '[SUB]',
                  'szerintiről': '[DEL]', 'szerintit': '[ACC]', 'szerintitől': '[ABL]', 'szerintivé': '[FAC]',
                  'szerintivel': '[INS]', 'túli': '[NOM]', 'túliak': '[NOM]', 'túliaké': '[NOM]', 'túliakig': '[TER]',
                  'túliakkal': '[INS]', 'túliaknak': '[DAT]', 'utáni': '[NOM]', 'utániak': '[NOM]',
                  'utániakat': '[ACC]', 'utánira': '[SUB]'}

# Correct postpositional phrase -> delete reflexiveness
postp_to_postp = {'afelett': 'felett', 'amellett': 'mellett', 'anélkül': 'nélkül', 'aszerint': 'szerint',
                  'efelé': 'felé', 'efelett': 'felett', 'efölött': 'fölött', 'ehelyett': 'helyett',
                  'ekörül': 'körül', 'eközben': 'közben', 'emellé': 'mellé', 'emiatt': 'miatt', 'emögött': 'mögött',
                  'ezelőtt': 'előtt', 'eziránt': 'iránt'}


def correct_postp(frame):
    new_frame = []
    for arg in frame:
        if '=' in arg:
            prefix, postp = arg.split('=',  maxsplit=1)
            if postp in not_postp:
                continue  # Drop bad arg
            postp = postp_to_case.get(postp, postp)
            postp = postp_to_case2.get(postp, postp)
            postp = postp_to_postp.get(postp, postp)
            arg = '='.join((prefix, postp))
        new_frame.append(arg)
    return new_frame
