#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

import emmorphpy

emmorph = emmorphpy.EmMorphPy()

emmorph_cases = {'-Ul': '[Ess]', '-bA': '[Ill]', '-bAn': '[Ine]', '-bÓl': '[Ela]', '-hOz': '[All]', '-ig': '[Ter]',
                 '-kor': '[Temp]', '-ként': '[EssFor]', '-n': '[Supe]', '-nAk': '[Dat]', '-nÁl': '[Ade]',
                 '-rA': '[Subl]', '-rÓl': '[Del]', '-t': '[Acc]', '-tÓl': '[Abl]', '-vAl': '[Ins]', '-vÁ': '[Transl]',
                 '-ért': '[Cau]', '-stUl': '[_Com:stUl/Adv]'}
emmorph_cases_keys = tuple(emmorph_cases.keys())


def emmorphize(lemma, gramm_case=None):
    """
    Convert to emMorph-like notation...
    """
    if lemma is not None and lemma.endswith('-A'):
        lemma = lemma[0:-2] + '[Poss]'
    lemma = lemma.replace('-A=', '[Poss]=').replace('-A-', '[Poss]-')
    if lemma.endswith(emmorph_cases_keys):
        lemma, suff = lemma.rsplit('-', 1)
        lemma += emmorph_cases['-' + suff]
    elif gramm_case is not None and gramm_case.startswith('-'):
        lemma += emmorph_cases[gramm_case]
    if not lemma.endswith(']') and not lemma.startswith('=') and '=' not in lemma or lemma.endswith('[Poss]'):
        lemma += '[Nom]'  # Better than worse...
    lemma = lemma.replace('=', ' =').strip()  # Strip space if there is no noun before the PP...

    return lemma


otherverbs = {'abbabeleegyez': 'abba|bele|egyez',
              'abbabelemegy': 'abba|bele|megy',
              'abbabelenyugodik': 'abba|bele|nyugodik',
              'abbabeletörődik': 'abba|bele|törődik',
              'abbakerül': 'abba|kerül',
              'abbavan': 'abba|van',
              'ad--kap': 'ad--kap',
              'ad--vesz': 'ad--vesz',
              'ad--veszik': 'ad--veszik',
              'alat': 'alat',
              'álmodoz': 'álmodoz',
              'áramol': 'áramol',
              'asztat': 'asztat',
              'áteljut': 'át|el|jut',
              'beköltöz': 'be|költöz',
              'beletel': 'bele|tel',
              'beletet': 'bele|tet',
              'besűrűsöd': 'be|sűrűsöd',
              'betel': 'be|tel',
              'bíztat': 'bíztat',
              'csetlik--botlik': 'csetlik--botlik',
              'csúsz': 'csúsz',
              'csűr--csavar': 'csűr--csavar',
              'egybegyűl': 'egybe|gyűl',
              'együttdolgoz': 'együtt|dolgoz',
              'együttdolgozik': 'együtt|dolgozik',
              'együttél': 'együtt|él',
              'együttérez': 'együtt|érez',
              'együttjár': 'együtt|jár',
              'együttjátszik': 'együtt|játszik',
              'együtttölt': 'együtt|tölt',
              'együttvan': 'együtt|van',
              'elbizonytalanod': 'el|bizonytalanod',
              'elégedet': 'elégedet',
              'elértéktelened': 'el|értéktelened',
              'eles': 'el|es',
              'elévesz': 'elé|vesz',
              'elfogul': 'el|fogul',
              'él--hal': 'él--hal',
              'elhíz': 'el|híz',
              'eljátsz': 'el|játsz',
              'eljutat': 'el|jutat',
              'elkötelezet': 'el|kötelezet',
              'elmegemlít': 'el|meg|említ',
              'elmegjegyez': 'el|meg|jegyez',
              'elmúl': 'el|múl',
              'eltel': 'el|tel',
              'eltűn': 'el|tűn',
              'elvál': 'el|vál',
              'eszik--iszik': 'eszik--iszik',
              'fek': 'fek',
              'felerősöd': 'fel|erősöd',
              'felgyűl': 'fel|gyűl',
              'feltornász': 'fel|tornász',
              'feltűn': 'fel|tűn',
              'felzárkóz': 'fel|zárkóz',
              'fölerősöd': 'föl|erősöd',
              'fölülmúl': 'fölül|múl',
              'füröd': 'füröd',
              'fürödik': 'fürödik',
              'gyarapod': 'gyarapod',
              'gyűl': 'gyűl',
              'hány--vet': 'hány--vet',
              'hazaelmegy': 'haza|el|megy',
              'hazud': 'hazud',
              'hibádz': 'hibádz',
              'hírhed': 'hírhed',
              'hivat': 'hivat',
              'híz': 'híz',
              'hoz--visz': 'hoz--visz',
              'hozzáodamegy': 'hozzá|oda|megy',
              'hozzászok': 'hozzá|szok',
              'húz--halaszt': 'húz--halaszt',
              'idebehoz': 'ide|be|hoz',
              'idebeír': 'ide|be|ír',
              'idebejön': 'ide|be|jön',
              'idebelép': 'ide|be|lép',
              'idebenéz': 'ide|be|néz',
              'idebetesz': 'ide|be|tesz',
              'ideeljön': 'ide|el|jön',
              'ideeljut': 'ide|el|jut',
              'ideirogat': 'ide|irogat',
              'idekijön': 'ide|ki|jön',
              'irogat': 'irogat',
              'ír--olvas': 'ír--olvas',
              'jár--kel': 'jár--kel',
              'jár--kelt': 'jár--kelt',
              'játsz': 'játsz',
              'jön--megy': 'jön--megy',
              'jutat': 'jutat',
              'kétel': 'kétel',
              'kimegmond': 'ki|meg|mond',
              'kimúl': 'ki|múl',
              'kitel': 'ki|tel',
              'kiteljesed': 'ki|teljesed',
              'korlatoz': 'korlatoz',
              'költöz': 'költöz',
              'kötelezet': 'kötelezet',
              'közrejátsz': 'közre|játsz',
              'közzétetszik': 'közzé|tetszik',
              'kultúrál': 'kultúrál',
              'kuporg': 'kuporg',
              'különböz': 'különböz',
              'lát--hall': 'lát--hall',
              'lát--hallik': 'lát--hallik',
              'lefek': 'le|fek',
              'leporolik': 'le|porolik',
              'letel': 'le|tel',
              'leteleped': 'le|teleped',
              'letet': 'le|tet',
              'lót--fut': 'lót--fut',
              'megállapod': 'meg|állapod',
              'megbeszel': 'meg|beszel',
              'megbizonyosod': 'meg|bizonyosod',
              'megbuk': 'meg|buk',
              'megelad': 'meg|el|ad',
              'megeléged': 'meg|eléged',
              'megelér': 'meg|el|ér',
              'megelérik': 'meg|el|érik',
              'megelfogad': 'meg|el|fogad',
              'megelmegy': 'meg|el|megy',
              'megelmond': 'meg|el|mond',
              'megelolvas': 'meg|el|olvas',
              'megerősöd': 'meg|erősöd',
              'meges': 'meg|es',
              'megfürödik': 'meg|fürödik',
              'meghány--vet': 'meg|hány--vet',
              'meghibásod': 'meg|hibásod',
              'meghíz': 'meg|híz',
              'megjelen': 'meg|jelen',
              'megleír': 'meg|le|ír',
              'megmegjelenik': 'meg|meg|jelenik',
              'megmegnéz': 'meg|meg|néz',
              'megmegtesz': 'meg|meg|tesz',
              'megmegvan': 'meg|meg|van',
              'megnyíl': 'meg|nyíl',
              'megnyugod': 'meg|nyugod',
              'megsűrűsöd': 'meg|sűrűsöd',
              'megszok': 'meg|szok',
              'megszűn': 'meg|szűn',
              'megtel': 'meg|tel',
              'megúsz': 'meg|úsz',
              'megvál': 'meg|vál',
              'megváltoz': 'meg|változ',
              'meggyűl': 'meg|gyűl',
              'mérkőz': 'mérkőz',
              'nyug': 'nyug',
              'nyugod': 'nyugod',
              'odabemegy': 'oda|be|megy',
              'odaeljut': 'oda|el|jut',
              'odaelmegy': 'oda|el|megy',
              'odavisszatér': 'oda|vissza|tér',
              'oszolik': 'oszolik',
              'osztoz': 'osztoz',
              'összegyűl': 'össze|gyűl',
              'összesűrűsöd': 'össze|sűrűsöd',
              'rámegvan': 'rá|meg|van',
              'recseg--ropog': 'recseg--ropog',
              'romol': 'romol',
              'sürög--forog': 'sürög--forog',
              'sűrűsöd': 'sűrűsöd',
              'süt--főz': 'süt--főz',
              'számontart': 'számon|tart',
              'származ': 'származ',
              'születet': 'születet',
              'tartoz': 'tartoz',
              'tel': 'tel',
              'telik--múl': 'telik--múl',
              'tel--múl': 'tel--múl',
              'térül--fordul': 'térül--fordul',
              'tesz--vesz': 'tesz--vesz',
              'tetsz': 'tetsz',
              'törik--zúz': 'törik--zúz',
              'tör--zúz': 'tör--zúz',
              'üt--ver': 'üt--ver',
              'vál': 'vál',
              'változ': 'változ',
              'van--van': 'van--van',
              'veszélyeztetet': 'veszélyeztetet',
              'visszaelindul': 'vissza|elindul',
              'visszaes': 'vissza|es',
              'visszaköltöz': 'vissza|költöz'
              }


def emmorph_filter(anals) -> set:
    ret = set()
    for anal in anals:
        isverb = False
        isprev = False
        prevs = set()
        for i, elem in enumerate(anal.split('+')):
            if elem.strip() == '':
                continue
            add, tag = elem.split(']')[0].split('[')
            isverb |= tag.endswith('/V')  # Has both '[/V]' and '[/Prev]'
            # 'felül' can be 'felül':'[/Prev]' (BAD) and 'felül': {'fel':'[/Prev]' + 'ül':'[/V]'} (GOOD)
            isprev |= tag == '/Prev' or (tag == '/CmpdPfx' and i == 0)
            if tag == '/Prev' or (tag == '/CmpdPfx' and i == 0):  # save '[/Prev]'
                prevs.add(add)
        if isverb and isprev:  # Return good preverbs...
            ret = ret.union(prevs)
    if len(ret) > 1:  # Hack for be/bele vissza/vissza-vissza, fel/fel-fel and meg/meg-meg
        new_ret = max(ret, key=len)
        print('WARNING HACK: MULTIPLE PREVERB ({0})! CHOOSING THE LONGEST ONE ({1})!'.format(ret, new_ret),
              file=sys.stderr)
        ret = {new_ret}
    return ret


with open('igeiszerkezet-lista.txt', encoding='ISO8859-2') as f:
    for l in f:
        fields = l.strip().split()
        verb = fields[0]
        new_fields = []
        for field in fields[1:-1]:
            field = field.replace('---', '-')
            field = field.replace('--', '-')
            if field == '-':
                continue
            if '|' in field:  # Fun: the distributivity is not regular: cases are common, but Possessives are not...
                case = ''
                if field.endswith(emmorph_cases_keys):
                    case = '-' + field.rsplit('-', 1)[1]
                field = '|'.join(sorted(emmorphize(el, case) for el in set(field.split('|'))))
            else:
                field = emmorphize(field)
            new_fields.append(field)
        fields[1:-1] = new_fields
        if not verb.endswith('null'):
            emmorph_anal = emmorph.analyze(verb)
            prev = emmorph_filter(emmorph_anal)
            if len(prev) > 0:
                # Should be one preverb here...
                preverb = prev.pop()
                if verb.startswith('-'):
                    preverb = '-' + preverb  # Hack for '-bejár' # Maybe: ki-bejár be-bejár...
                # And verb should start with it...
                assert verb.startswith(preverb), 'Verb ({0}) not starts with preverb ({0})!'.format(verb, preverb)
                verb = verb[:len(preverb)] + '|' + verb[len(preverb):]
            elif len(emmorph_anal) == 0 and verb in otherverbs:  # Verbs not known by emMorph
                verb = otherverbs[verb]                              # Usually bad forms or special cases
            elif len(emmorph_anal) == 0:
                exit('Error {0}'.format(verb))
            else:
                # There is no preverb...
                pass
        elif verb.endswith('null'):  # |null, le|null, etc.
            assert len(verb) > 4, 'Is this ({0}) prev+null?'.format(verb)
            verb = verb[:-4] + '|' + verb[-4:]
        else:
            exit('Error2 {0}'.format(verb))
        fields[0] = verb
        if len(fields) > 1:
            print('\t'.join(fields))
        else:
            print(' ' + ''.join(fields))  # For the last line...
