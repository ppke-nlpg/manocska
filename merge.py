#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from collections import defaultdict, Counter

"""
Incorrect verbal article splitting:
Humor does not recognise the first part as verbal particle or the second part as a verb.
But recognise the whole entry as a verb.
"""
not_prev_verbs = {'alá|z', 'át|all', 'be|cserkel', 'be|folyásol', 'bé|kél', 'bé|küld', 'bé|lel', 'bele|s', 'bele|z',
                  'bent|ragad', 'cserben|hagy', 'elé|g', 'élen|jár', 'el|enyész', 'elé|r', 'elő|z', 'fel|el',
                  'földet|őriz', 'helyben|hagy', 'helyt|áll', 'helyt|őriz', 'helyt|rendez', 'jól|esik', 'jól|lakat',
                  'jól|lakik', 'jól|tart', 'jót|áll', 'karban|tart', 'kétségbe|esik', 'ki|fogásol', 'ki|horgász',
                  'ki|józanul', 'kinn|felejt', 'közben|jár', 'le|l', 'le|p', 'le|s', 'le|sz', 'meg|vagyon',
                  'nagyot|hall', 'odébb|áll', 'rá|g', 'rá|z', 'rendre|utasít', 'rosszul|esik', 'síkra|száll',
                  'szemre|hány', 'szemre|vételez', 'szörnyet|hal', 'tele|l', 'teli|k', 'után|állít', 'után|ízesít',
                  'után|nyom', 'után|rendel', 'után|tölt', 'útba|igazít'}

"""
With the second verbal article they are OK.
"""
double_prev_verbs = {'abba|bele|megy', 'abba|bele|nyugodik', 'abba|bele|törődik', 'át|el|jut', 'el|meg|említ',
                     'el|meg|jegyez', 'haza|el|megy', 'hozzá|oda|megy', 'ide|be|hoz', 'ide|be|ír', 'ide|be|jön',
                     'ide|be|lép', 'ide|be|néz', 'ide|be|tesz', 'ide|el|jön', 'ide|el|jut', 'ide|ki|jön', 'ki|meg|mond',
                     'meg|el|ad', 'meg|el|ér', 'meg|el|érik', 'meg|el|fogad', 'meg|el|megy', 'meg|el|mond',
                     'meg|el|olvas', 'meg|le|ír', 'meg|meg|jelenik', 'meg|meg|néz', 'meg|meg|tesz', 'meg|meg|van',
                     'oda|be|megy', 'oda|el|jut', 'oda|el|megy', 'oda|vissza|tér', 'rá|meg|van'}

"""
Occur splitted and not splitted but both wrong.
"""
wrong_verbs = {'megfájul', 'meg|fájul', 'elbúcsu', 'el|búcsu', 'behu', 'be|hu', 'meghó', 'meg|hó', 'kétségbeejt',
               'kétségbe|ejt'}

"""
Occur splitted and not splitted but only the NOT splitted is OK.
"""
not_prev_verbs2 = {'fel|esel', 'szembe|sül', 'észre|vételez', 'mellé|kel', 'ellen|őriz', 'ki|vitelez', 'jóvá|hagy',
                   'ellen|súlyoz', 'fel|ejt', 'ki|abál'}

"""
Occur splitted and not splitted but only the splitted is OK.
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
      'el|zabrál', 'hátra|lök', 'le|reped', 'meg|gémberedik', 'le|fittyed', 'fel|tarisznyál', 'el|gázosít',
      'alább|hagy', 'meg|hegyez', 'fel|dolgoz', 'le|nyomtat', 'ki|fehérlik', 'le|szegényedik',
      'le|maradozik', 'át|fűt', 'le|tűz', 'elő|énekel', 'ki|lábol', 'ki|rázódik', 'el|gördít', 'el|hibáz',
      'át|húzat', 'meg|botoz', 'át|kap', 'be|árnyékoz', 'meg|kettőződik', 'bele|sóhajt', 'helyre|zökken',
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
      'be|rezel', 'bele|csavar', 'meg|esz', 'haza|szólít', 'át|pofoz', 'ki|kísérletez', 'hozzá|kap',
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
      'fel|takar', 'meg|csörget', 'elő|buggyan', 'át|tűz', 'össze|habar', 'el|boronál'}}

"""
wrong verbs: stemming error
"""
wrong_verbs2 = {'ad--veszik', 'ajánlat', 'al', 'alat', 'alázat', 'áldozat', 'alud', 'asztat', 'bí', 'bíztat',
                'bíztat{ORTH:substandard}', 'bűzöl', 'cselekedet', 'dolgozat', 'elégedet', 'élvezet', 'emlékezet',
                'es', 'fedezet', 'fejezet', 'fek', 'füröd', 'fürödik', 'gyalázat', 'gyülekezet', 'hálózat', 'határozat',
                'hírhed', 'hivat', 'idézet', 'igyekezet', 'irogat', 'jár--kelt', 'jutat', 'kereset', 'kétel',
                'kockázat', 'korlatoz', 'köll', 'környezet', 'kötelezet', 'kötet', 'közalkalmaz', 'kultúrál', 'kuporg',
                'lát--hallik', 'letet', 'magyarázat', 'normál', 'nyilatkozat', 'nyug', 'nyugod', 'oszolik',
                'pályázat', 'romol', 'sarkallik', 'seregel', 'sorozat', 'szavazat', 'szégyenel', 'szeretet',
                'szervezet', 'szövetkezet', 'születet', 'táblázat', 'tagozat', 'tel--múl', 'tervezet', 'törik--zúz',
                'ugor', 'vadászat', 'változat', 'van--van', 'végetér', 'veszélyeztetet', 'vigyázat', 'fokozat',
                'elhangozik', 'szembenáll'}

"""
good verbs, that Humor has not recognised.
We do not do anything with them. Mostly due to the hyphen (--)
"""
good_verbs_humor_not_recognised = {'hatályosul', 'ad--kap', 'ad--vesz', 'csetlik--botlik', 'csűr--csavar', 'él--hal',
                                   'eszik--iszik', 'hány--vet', 'hoz--visz', 'húz--halaszt', 'ír--olvas',
                                   'jár--kel', 'jön--megy', 'lát--hall', 'lót--fut', 'recseg--ropog',
                                   'sürög--forog', 'süt--főz', 'térül--fordul', 'tesz--vesz', 'tör--zúz', 'üt--ver'}

"""
these verbs should have an ik suffix
"""
verbs_need_ik = {'egyez', 'osztoz', 'álmod', 'álmodoz', 'áramol', 'csúsz', 'erősöd', 'foglakoz', 'folyamod', 'gazdagod',
                 'gyarapod', 'gyűl', 'hazud', 'hibádz', 'híz', 'horgász', 'játsz', 'kés', 'kies', 'költöz', 'közeled',
                 'különböz', 'létez', 'mérkőz', 'nyíl', 'önállósod', 'rejtőz', 'részesed', 'rozsdásod', 'sűrűsöd',
                 'származ', 'szörföz', 'tapogatóz', 'tartoz', 'távoz', 'tel', 'telik--múl', 'tetsz', 'tornász', 'tűn',
                 'vál', 'változ', 'vitáz', 'vizsgáz', 'felvételiz'}

"""
Occur not splitted but only the splitted is OK.
"""
prev_verbs = \
             {elem.replace('|', ''): elem for elem in
              {'be|gyűrűzik', 'be|végeztetik', 'cserben|hagy', 'élen|jár', 'el|vetemül', 'helyben|hagy', 'helyt|áll',
               'jól|esik', 'jól|lakik', 'jóvá|hagy',  'közben|jár', 'meg|hibban', 'odébb|áll', 'rá|fáz',
               'rendre|utasít', 'rosszul|esik', 'síkra|száll'}}

"""
Good verbs, that have false verbal article analysis
"""
false_prev_good = {'felesel', 'felvételizik', 'karbantart', 'kétségbeesik', 'kiabál', 'mellékel', 'szembesül',
                   'szemrevételez', 'szörnyethal', 'túlórázik', 'útbaigazít'}

"""
Good verbs, that have false verbal article analysis but need ik suffix
"""
false_prev_need_ik = {'elenyész', 'elhaláloz', 'túlóráz'}

"""
Occur not splitted but only the splitted is OK. And ik suffix is needed
"""
prev_and_ik_verbs = \
             {elem.replace('|', ''): (elem + 'ik') for elem in
              {'el|búcsúz', 'meg|éhez', 'meg|fáz', 'meg|reggeliz', 'meg|szomjaz', 'meg|vacsoráz',
               'rá|fáz', 'be|gubóz', 'el|időz', 'el|puskáz', 'el|szipkáz', 'fel|tornáz', 'le|fasisztáz', 'ki|mazsoláz'}}

"""
Stemming error with strange verbal article
"""
prev_and_verb_not_goes_toghether_bad = {'át|aluik', 'bele|tet', 'ide|irogat', 'ki|listá', 'le|fek', 'le|kép',
                                        'le|porolik', 'meg|beszel', 'meg|különb', 'meg|négy', 'meg|nyugod',
                                        'utána|végrehajt', 'vissza|elindul', 'el|kötelezet', 'meg|fürödik'}

"""
Prev and verb not goes together (delete)
"""
verb_bad_prev = {'-be|jár', 'bé|késik',  'egyet|ér', 'el|fogul', 'helyt|van',  'jól|érez', 'kétségbe|rohan',
                 'kétségbe|van', 'kétségbe|von', 'kölcsön|lehet', 'kölcsön|szól', 'közzé|tetszik', 'létre|szenderedik',
                 'szörnyet|uszít', 'számba|megy', 'pofon|érkezik'
                 'abba|kerül', 'abba|van', 'egyet|alszik', 'egyet|említ', 'egyet|gondol', 'egyet|húz', 'egyet|jelent',
                 'egyet|kér', 'egyet|lát', 'egyet|lép', 'egyet|mond', 'egyet|nyel', 'egyet|nyom', 'egyet|sóhajt',
                 'egyet|szeret', 'egyet|talál', 'egyet|tud', 'egyet|választ', 'egyet|vesz', 'együtt|csinál',
                 'együtt|dolgozik', 'együtt|él', 'együtt|érez', 'együtt|jár', 'együtt|játszik',
                 'együtt|rögzít', 'együtt|szerkeszt', 'együtt|tölt', 'együtt|van', 'földet|kap', 'helyben|biztosít',
                 'helyben|használ', 'helyben|marad', 'helyben|van', 'helyt|kap', 'jót|akar', 'jót|ígér', 'jót|ír',
                 'jót|kíván', 'jót|mond', 'jót|tesz', 'nagyot|alkot', 'nagyot|csalódik', 'nagyot|dobban',
                 'nagyot|fordul', 'nagyot|kacag', 'nagyot|nevet', 'nagyot|néz', 'nagyot|nyel', 'nagyot|sóhajt',
                 'nagyot|téved', 'nagyot|változik', 'pofon|vág', 'szabadjára|enged',
                 'szabadlábra|helyez', 'számba|vesz', 'számon|kér', 'számon|tart', 'szemügyre|vesz',
                 'torkig|van', 'tudomásul|vesz', 'útba|ejt', 'békén|hagy', 'elé|vesz', 'el|jutat', 'földet|ér',
                 'helyt|ad', 'itt|hagy', 'meg|hány--vet', 'óva|int', 'pórul|jár', 'zokon|vesz',
                 'együtt|dolgoz', 'közre|játsz'}  # TODO: Research written together of separately?

"""
add ik suffix
"""
verb_add_ik_suffix = {'át|forrósod', 'be|költöz', 'bele|tel', 'be|sűrűsöd', 'be|tel', 'egybe|gyűl', 'el|adósod',
                      'el|bizonytalanod', 'el|értéktelened', 'el|es', 'el|híz', 'el|játsz', 'el|távoz', 'el|tel',
                      'el|tűn', 'el|vál', 'fel|erősöd', 'fel|forrósod', 'fel|gyűl', 'fel|tornász', 'fel|tűn',
                      'fel|zárkóz', 'föl|erősöd', 'hozzá|szok', 'ki|tel', 'ki|teljesed', 'le|tel', 'le|teleped',
                      'le|vizsgáz', 'meg|állapod', 'meg|bizonyosod', 'meg|buk', 'meg|egyez', 'meg|eléged',
                      'meg|erősöd', 'meg|es', 'meg|gyűl', 'meg|hibásod', 'meg|híz', 'meg|jelen', 'meg|nyíl',
                      'meg|sűrűsöd', 'meg|szok', 'meg|szűn', 'meg|tel', 'meg|úsz', 'meg|vál', 'meg|változ',
                      'össze|gyűl', 'össze|sűrűsöd', 'vissza|es', 'vissza|költöz', 'bele|egyez', 'ki|egyez',
                      'hozzá|szok'}


def fix_verb(verb_elem):
    if verb_elem in double_prev_verbs:
        verb_elem = verb_elem.split('|', maxsplit=1)[1]
    elif verb_elem in not_prev_verbs or verb_elem in not_prev_verbs2:  # Remove split
        verb_elem = verb.replace('|', '')
    elif verb_elem in verbs_need_ik or verb_elem in false_prev_need_ik or verb_elem in verb_add_ik_suffix:
        verb_elem += 'ik'
    verb_elem = not_prev_verbs3.get(verb_elem, verb_elem)  # Put split
    verb_elem = prev_verbs.get(verb_elem, verb_elem)
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
        if verb in wrong_verbs or verb in wrong_verbs2 or verb in prev_and_verb_not_goes_toghether_bad or\
                verb in verb_bad_prev:
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
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in prev_and_verb_not_goes_toghether_bad or\
                    verb in verb_bad_prev:
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
        if verb in wrong_verbs or verb in wrong_verbs2 or verb in prev_and_verb_not_goes_toghether_bad or\
                verb in verb_bad_prev:
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
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in prev_and_verb_not_goes_toghether_bad or\
                    verb in verb_bad_prev:
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
        kagi_verbs['{0}|{1}'.format(ik, verb)] = freq
        kagi_sumfreq += freq

print('No. of Verbs (kagi_verbal_complex): ', len(kagi_verbs), file=sys.stderr)

all_ige = set(verb_dict_verbs.keys()) | set(isz_verbs.keys()) | set(tade_verbs.keys())
print('Igék száma (összesen): ', len(all_ige), file=sys.stderr)

for verb in sorted(all_ige):
    szotar_ige = tuple([keret[1] for keret in verb_dict_verbs[verb]])
    isz_ige = tuple([keret[1] for keret in isz_verbs[verb]])
    tade_ige = tuple([keret[1] for keret in tade_verbs[verb]])
    all_frame = set(szotar_ige) | set(isz_ige) | set(tade_ige)
    if len(szotar_ige) + len(isz_ige) + len(tade_ige) > len(all_frame):
        print(verb, list(sorted(set(szotar_ige) & set(isz_ige))), list(sorted(set(isz_ige) & set(tade_ige))),
              list(sorted(set(tade_ige) & set(szotar_ige))), kagi_verbs[verb], sep='\n', end='\n\n', file=sys.stderr)
    for act_frame in sorted(all_frame):
        szotar_freq = get_freq_w_ind_for_frame(verb_dict_verbs[verb], act_frame)[1]
        isz_freq = get_freq_w_ind_for_frame(isz_verbs[verb], act_frame)[1]
        tade_freq = get_freq_w_ind_for_frame(tade_verbs[verb], act_frame)[1]
        kagi_aggr_freq = 0
        kagi_freq_fin1_ik1 = kagi_freq_fin1_ik2 = kagi_freq_fin2_ik1 = kagi_freq_fin2_ik2 = None
        if '|' in verb:
            kagi_freq_fin1_ik1 = kagi_verbs[verb]
            kagi_aggr_freq += kagi_freq_fin1_ik1
            """
            if len(act_frame) > 0 and act_frame[0].startswith('INF_'):
                inf = act_frame[0][4:]  # strip 'INF_' prefix
                ige_ik, ige_wo_ik = verb.split('|', maxsplit=1)
                if '|' in inf:
                    # Own PreV
                    kagi_freq_fin2_ik2 = kagi_verbs[inf]
                    kagi_aggr_freq += kagi_freq_fin2_ik2
                    # Swap PreV
                    inf_ik, inf_wo_ik = inf.split('|', maxsplit=1)
                    kagi_freq_fin1_ik2 = kagi_verbs['{0}|{1}'.format(inf_ik, ige_wo_ik)]
                    kagi_aggr_freq += kagi_freq_fin1_ik2
                    kagi_freq_fin2_ik1 = kagi_verbs['{0}|{1}'.format(ige_ik, inf_wo_ik)]
                    kagi_aggr_freq += kagi_freq_fin2_ik1
                else:
                    kagi_freq_fin2_ik1 = kagi_verbs['{0}|{1}'.format(ige_ik, inf)]
                    kagi_aggr_freq += kagi_freq_fin2_ik1
            """
        else:
            """
            if len(act_frame) > 0 and act_frame[0].startswith('INF_'):
                inf = act_frame[0][4:]  # strip 'INF_' prefix
                if '|' in inf:
                    inf_ik, inf_wo_ik = inf.split('|', maxsplit=1)
                    kagi_freq_fin1_ik2 = kagi_verbs['{0}|{1}'.format(inf_ik, verb)]
                    kagi_aggr_freq += kagi_freq_fin1_ik2
            """
        if act_frame == ():
            act_frame = '@'
        else:
            act_frame = ' '.join(act_frame)
        rank = sum((szotar_freq / verb_dict_sumfreq, isz_freq / isz_sumfreq, tade_freq / tade_sumfreq,
                    kagi_aggr_freq / (4*kagi_sumfreq)))
        print(verb, act_frame, szotar_freq, isz_freq, tade_freq, kagi_freq_fin1_ik1,
              kagi_freq_fin1_ik2, kagi_freq_fin2_ik1, kagi_freq_fin2_ik2, '{0:1.20f}'.format(rank), sep='\t')

"""
time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k10,10nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
