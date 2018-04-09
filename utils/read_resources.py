#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
import os
import pickle
import gzip

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
            if len(entry) == 3:
                verb, freq, example = entry
                arguments = []
            elif len(entry) >= 4:
                verb, *arguments, freq, example = entry
            elif entry == ['']:
                break
            else:
                verb, arguments, freq = None, [], 0  # Dummy assignment to silence IDE
                exit('verb_dict_error: {0}'.format(entry))
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
                if len(entry) == 2:
                    verb, freq = entry
                    arguments = []
                elif len(entry) >= 3:
                    verb, *arguments, freq = entry
                else:
                    verb, arguments, freq = None, [], 0  # Dummy assignment to silence IDE
                    exit('isz_error: {0}'.format(entry))
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
            if len(entry) == 5:
                verb, arguments, freq, igegyak, arany = entry
                if arguments[0] == '@':
                    arguments = ''
            else:
                verb, arguments, freq = None, [], 0  # Dummy assignment to silence IDE
                exit('tade_error: {0}'.format(entry))
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
            if len(entry) == 2:
                freq, verb_w_ik = entry
            else:
                verb_w_ik, freq = [], 0  # Dummy assignment to silence IDE
                exit('kagi_verbs_error: {0}'.format(entry))
            ik, verb = verb_w_ik.split('+')
            freq = int(freq)
            if is_verb_wrong(verb):
                found_wrong_verbs.add(verb)
                continue
            verb_new = fix_verb(verb)
            if verb_new != verb:
                found_wrong_verbs.add(verb)
            verb = verb_new
            found_verbs['{0}|{1}'.format(ik, verb)] = freq
            sumfreq += freq
    return sumfreq, found_wrong_verbs, found_verbs


def kagi_inflist_process():
    # TODO: document
    found_verbs = defaultdict(list)
    sumfreq = 0
    with open('infinitival_constructions/FinInf.txt', encoding='UTF-8') as inflist:
        for entry in inflist:
            entry = entry.strip().split('\t')
            if len(entry) >= 2:
                freq, verb_w_ik = entry[:2]
                if '+' in verb_w_ik:
                    ik, verb = verb_w_ik.split('+')
                    verb = '{0}|{1}'.format(ik, verb)
                else:
                    freq, verb = entry[:2]
            else:
                verb, freq = [], 0  # Dummy assignment to silence IDE
                exit('kagi_fininf_error: {0}'.format(entry))
            freq = int(freq)
            arguments = ['INF']
            smart_append(found_verbs, verb, freq, tuple(sorted(arguments)))
            sumfreq += freq
    return sumfreq, found_verbs


def mmo_process():
    verb_dict = process_mmo()
    verbs = defaultdict(list)
    for verb, frames in verb_dict.items():
        for mmoid, frame in frames.items():
            fr = []
            opt = []
            for arg, feats in frame[0].items():  # TODO: opt=YES feature...
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
                    new_arg = '@'
                new_feats = {k: v for k, v in feats.items() if '-' != k and '-' != v}
                new_feats['arg_name'] = arg
                if ':opt' in new_feats:
                    opt.append((new_feats, new_arg))
                else:
                    opt.append((new_feats, new_arg))
                    fr.append((new_feats, new_arg))
            fr.sort(key=lambda x: x[1])
            meta = {'mmoid': mmoid, 'EN.VP': frame[1]}
            verbs[verb].append((meta, tuple(fr)))
            if len(opt) > 0:
                opt.sort(key=lambda x: x[1])
                verbs[verb].append((meta, tuple(opt)))
    return len(verb_dict), verbs


def dummy_process():
    return 0, set(), {}


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
    inflist_sumfreq, inflist_verbs = create_kagi_inflist.result()
    mmo_sumfreq, mmo_verbs = create_mmo.result()

    all_ige = set(verb_dict_verbs.keys()) | set(isz_verbs.keys()) | set(tade_verbs.keys()) | set(inflist_verbs.keys()) \
        | set(kagi_verbs.keys()) | set(mmo_verbs.keys())

    print('No. of Verbs (verb_dict): ', len(verb_dict_verbs), verb_dict_sumfreq, len(verb_dict_wrong_verbs),
          file=sys.stderr)
    print('No. of Verbs (isz): ', len(isz_verbs), isz_sumfreq, len(isz_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (Tadé): ', len(tade_verbs), tade_sumfreq, len(tade_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (kagi_verbal_complex): ', len(kagi_verbs), kagi_sumfreq, len(kagi_wrong_verbs), file=sys.stderr)
    print('No. of Verbs (inflist): ', len(inflist_verbs), inflist_sumfreq, file=sys.stderr)
    print('No. of Verbs (MetaMorpho): ', len(mmo_verbs), mmo_sumfreq, file=sys.stderr)
    print('No. of Verbs (total): ', len(all_ige), file=sys.stderr)

    if overwrite or not os.path.exists(pickled_name):
        pickle.dump(((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
                     (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige),
                    gzip.open(pickled_name, 'wb'))

    return (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige
