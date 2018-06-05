#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys
import gzip
import copy
import pickle

from itertools import combinations
from collections import defaultdict, Counter
from concurrent.futures import ProcessPoolExecutor, wait

from utils.correction_tables import is_verb_wrong, fix_verb, correct_postp
from MetaMorphoHuEn.mmo_to_dict import process_mmo


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


def verb_dict_process():
    found_wrong_verbs = set()
    found_verbs = defaultdict(list)
    sumfreq = 0
    with open('ige_szotar/szotar.kimenet.txt', encoding='UTF-8') as verb_dict:
        for entry in verb_dict:
            entry = entry.strip().split('\t')
            if len(entry) < 3 and entry != ['']:
                exit('verb_dict_error: {0}'.format(entry))
            elif entry == ['']:
                break

            # No alternative forms among the verbs just among the lexical arguments
            if len(entry) < 3:
                verb, freq, example = entry
                arguments = []
            else:  # len(entry) >= 4
                verb, *arguments, freq, example = entry

            freq = int(freq)
            if is_verb_wrong(verb):
                found_wrong_verbs.add(verb)
                continue
            verb_new = fix_verb(verb)
            if verb_new != verb:
                found_wrong_verbs.add(verb)
            verb = verb_new
            arguments = [i.replace(' =', '=') for i in arguments]  # Because at the end args will be separated by spaces
            arguments = correct_postp(arguments)
            smart_append(found_verbs, verb, freq, tuple(sorted(arguments)))
            sumfreq += freq
    return sumfreq, found_wrong_verbs, found_verbs


def isz_process():
    found_wrong_verbs = set()
    found_verbs = defaultdict(list)
    sumfreq = 0
    with open('isz/igeiszerkezet-lista.kimenet.txt', encoding='UTF-8') as isz:
        for entry in isz:
            if not entry.startswith((' 0', 'Igeskicc')):
                entry = entry.strip().split('\t')
                if len(entry) < 2:
                    exit('isz_error: {0}'.format(entry))

                # No alternative forms among the verbs just among the lexical arguments
                if len(entry) == 2:
                    verb, freq = entry
                    arguments = []
                else:  # len(entry) >= 3
                    verb, *arguments, freq = entry

                freq = int(freq)
                if is_verb_wrong(verb):
                    found_wrong_verbs.add(verb)
                    continue
                verb_new = fix_verb(verb)
                if verb_new != verb:
                    found_wrong_verbs.add(verb)
                verb = verb_new
                # Because at the end args will be separated by spaces
                arguments = [i.replace(' =', '=') for i in arguments]
                arguments = correct_postp(arguments)
                smart_append(found_verbs, verb, freq, tuple(sorted(arguments)))
                sumfreq += freq
    return sumfreq, found_wrong_verbs, found_verbs


def tade_process():
    found_wrong_verbs = set()
    found_verbs = defaultdict(list)
    sumfreq = 0
    with open('tade/tade.kimenet.tsv', encoding='UTF-8') as tade:
        for entry in tade:
            entry = entry.strip().split('\t')
            if len(entry) != 5:
                exit('tade_error: {0}'.format(entry))

            # No alternative forms denoted by | as preverbs are denoted by |
            verb, arguments, freq, verbfreq, arany = entry
            if arguments[0] == '@':
                arguments = ''

            arguments = tuple(arguments.split())
            freq = int(freq)
            if is_verb_wrong(verb):
                found_wrong_verbs.add(verb)
                continue
            verb_new = fix_verb(verb)
            if verb_new != verb:
                found_wrong_verbs.add(verb)
            verb = verb_new

            # Fix double argumetns: Uniq
            set_vonzatok = set(arguments)
            if len(arguments) > len(set_vonzatok):
                arguments = tuple(set_vonzatok)
            if ' ' in verb:
                if verb.startswith('"'):
                    print('Dropped: {0}'.format(verb), file=sys.stderr)
                    continue
                verb, inf = verb.split()
                if is_verb_wrong(verb):
                    found_wrong_verbs.add(verb)
                    continue
                verb_new = fix_verb(verb)
                if verb_new != verb:
                    found_wrong_verbs.add(verb)
                verb = verb_new
                # Do not append INF's frame to the non-INF occurence's frame.
                # It could contain argument of the FIN verb too!
                # TODO: Research a solution later...
                # smart_append(found_verbs, inf, freq, tuple(sorted(arguments)))  # Here stuff can be non uniq...
                # sumfreq += freq
                # arguments = ['INF_' + inf]
                arguments = ['INF']
            arguments = correct_postp(arguments)
            smart_append(found_verbs, verb, freq, tuple(sorted(arguments)))  # Here stuff can be non uniq...

            sumfreq += freq
    return sumfreq, found_wrong_verbs, found_verbs


def kagi_verbs_process():
    found_wrong_verbs = set()
    found_verbs = Counter()
    sumfreq = 0
    with open('kagi_verbal_complex/freqPrevFin.txt', encoding='UTF-8') as kagi:
        for entry in kagi:
            entry = entry.strip().split(' ')

            if len(entry) != 2:
                exit('kagi_verbs_error: {0}'.format(entry))

            freq, verb_w_ik = entry
            prev, verb = verb_w_ik.split('+')
            freq = int(freq)

            for v in verb.split('|'):
                verb = '{0}|{1}'.format(prev, v)
                if is_verb_wrong(verb):
                    found_wrong_verbs.add(verb)
                    continue
                verb_new = fix_verb(verb)
                if verb_new != verb:
                    found_wrong_verbs.add(verb)
                verb = verb_new
                found_verbs[verb] = freq
                sumfreq += freq
    return sumfreq, found_wrong_verbs, found_verbs


def kagi_inflist_process():
    # TODO: document
    found_wrong_verbs = set()
    found_verbs = defaultdict(list)
    sumfreq = 0
    with open('infinitival_constructions/FinInf.txt', encoding='UTF-8') as inflist:
        for entry in inflist:
            entry = entry.strip().split('\t')
            if len(entry) < 2:
                exit('kagi_fininf_error: {0}'.format(entry))
            freq, verb = entry[:2]

            freq = int(freq)
            arguments = ['INF']

            prev = ''
            if '+' in verb:
                prev, verb = verb.split('+')
                prev += '|'

            for v in verb.split('|'):
                if len(prev) > 0:
                    verb = '{0}|{1}'.format(prev, v)
                else:
                    verb = v
                if is_verb_wrong(verb):
                    found_wrong_verbs.add(verb)
                    continue
                verb_new = fix_verb(verb)
                if verb_new != verb:
                    found_wrong_verbs.add(verb)
                verb = verb_new
                smart_append(found_verbs, verb, freq, tuple(sorted(arguments)))
                sumfreq += freq
    return sumfreq, found_wrong_verbs, found_verbs


def mmo_process():
    verb_dict = process_mmo()
    verbs = defaultdict(list)
    for verb, frames in verb_dict.items():
        for mmoid, frame in frames.items():
            fr = []
            opt = []
            for arg, feats in frame[0].items():
                if arg == 'TV':
                    continue
                lex, case, postp = '', '', ''
                if 'lex' in feats:
                    lex = feats['lex'].strip('"')
                if ':lex' in feats:
                    lex = feats[':lex'].strip('"')
                if 'postp' in feats:
                    postp = '=' + feats['postp'].strip('"')
                if 'case' in feats:
                    case = '[' + feats['case'] + ']'
                elif ':advtype' in feats:
                    case = '[' + feats[':advtype'] + ']'
                new_arg = lex+case+postp
                if len(new_arg) == 0:
                    if arg == 'SUBJ':
                        continue
                    new_arg = '_'
                new_feats = {k: v for k, v in feats.items() if '-' != k and '-' != v}
                new_feats['arg_name'] = arg
                if ':opt' in new_feats:
                    opt.append((new_feats, new_arg))
                else:
                    fr.append((new_feats, new_arg))

            meta = {'mmoid': mmoid, 'EN.VP': frame[1]}

            # Append without optional element
            fr.sort(key=lambda x: x[1])
            verbs[verb].append((meta, tuple(fr)))

            # Append all combinations of optimonal elements
            for i in range(1, len(opt) + 1):
                fr_act = copy.deepcopy(fr)
                for c in combinations(opt, i):
                    fr_act.extend(c)
                    fr_act.sort(key=lambda x: x[1])
                    verbs[verb].append((meta, tuple(fr_act)))
    return len(verb_dict), {}, verbs  # Dummy wrong verbs list... TODO: research!


def read_resources_parallel(pickled_name, overwrite=False):
    with ProcessPoolExecutor(max_workers=6) as executor:
        create_verb_dict = executor.submit(verb_dict_process)
        create_isz = executor.submit(isz_process)
        create_tade = executor.submit(tade_process)
        create_kagi_verbs = executor.submit(kagi_verbs_process)
        create_kagi_inflist = executor.submit(kagi_inflist_process)
        create_mmo = executor.submit(mmo_process)

    wait([create_verb_dict, create_isz, create_kagi_verbs, create_kagi_inflist, create_mmo])

    verb_dict_sumfreq, verb_dict_wrong_verbs, verb_dict_verbs = create_verb_dict.result()
    isz_sumfreq, isz_wrong_verbs, isz_verbs = create_isz.result()
    tade_sumfreq, tade_wrong_verbs, tade_verbs = create_tade.result()
    kagi_sumfreq, kagi_wrong_verbs, kagi_verbs = create_kagi_verbs.result()
    inflist_sumfreq, inflist_wrong_verbs, inflist_verbs = create_kagi_inflist.result()
    mmo_sumfreq, mmo_wrong_verbs, mmo_verbs = create_mmo.result()

    all_verb = set(verb_dict_verbs.keys()) | set(isz_verbs.keys()) | set(tade_verbs.keys()) \
        | set(kagi_verbs.keys()) | set(inflist_verbs.keys()) | set(mmo_verbs.keys())

    all_wrong_verb = set(verb_dict_wrong_verbs) | set(isz_wrong_verbs) | set(tade_wrong_verbs) \
        | set(kagi_wrong_verbs) | set(inflist_wrong_verbs) | set(mmo_wrong_verbs)

    verbs_stat = Counter()
    verbs_stat_v = defaultdict(set)
    for v in all_verb:
        c = sum(int(v in r and (r != inflist_verbs.keys() or inflist_verbs.get(v, [[0]])[0][0] > 0))
                for r in (verb_dict_verbs.keys(),  isz_verbs.keys(), tade_verbs.keys(), kagi_verbs.keys(),
                          inflist_verbs.keys(), mmo_verbs.keys()))
        verbs_stat[c] += 1
        verbs_stat_v[c].add(v)

    print('No. of Verbs (verb_dict): ', len(verb_dict_verbs), verb_dict_sumfreq, len(verb_dict_wrong_verbs),
          file=sys.stderr)
    print('No. of Verbs (isz): ', len(isz_verbs), isz_sumfreq, len(isz_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (Tadé): ', len(tade_verbs), tade_sumfreq, len(tade_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (kagi_verbal_complex): ', len(kagi_verbs), kagi_sumfreq, len(kagi_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (inflist): ', len(inflist_verbs), inflist_sumfreq, len(inflist_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (MetaMorpho): ', len(mmo_verbs), mmo_sumfreq, file=sys.stderr)
    print('No. of Verbs (total): ', len(all_verb), len(all_wrong_verb), file=sys.stderr)
    for k, v in verbs_stat.items():
        print('No. of Verbs in {0} resource(s): '.format(k), v, file=sys.stderr)

    for v in sorted(verbs_stat_v[5]):
        print('In 5 resources:', v, file=sys.stderr)
    for v in sorted(verbs_stat_v[6]):
        print('In 6 resources:', v, file=sys.stderr)

    if overwrite or not os.path.exists(pickled_name):
        pickle.dump(((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
                     (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_verb),
                    gzip.open(pickled_name, 'wb'))

    return (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
           (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_verb
