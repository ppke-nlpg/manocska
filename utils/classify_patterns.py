#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys
import gzip
import pickle

from collections import defaultdict, Counter


def preprocess_frames(frames) -> set:
    new_frames = set()
    for frame in frames:
        if len(frame) > 0:
            new_frame = []
            for arg in frame:
                if ('INF',) == frame:
                    new_frame = frame
                    break
                if '|' in arg and '=' in arg:
                    arg = arg.replace('ország-világ=előtt|ország-világ[NOM]', 'ország-világ=előtt').\
                        replace('frakcióvezető-helyettes[NOM]|frakcióvezető-helyettes=szerint',
                                'frakcióvezető-helyettes[PSe3]=szerint').\
                        replace('frakcióvezető-helyettes[NOM]|frakcióvezető-helyettes[PSe3]=szerint',
                                'frakcióvezető-helyettes[PSe3]=szerint').\
                        replace('telek[NOM]|tél=belül', 'tél=belül').\
                        replace('közvélemény-kutatás=szerint|közvélemény-kutatás[NOM]', 'közvélemény-kutatás=szerint').\
                        replace('ország-világ=előtt|ország-világ[NOM]', 'ország-világ=előtt').\
                        replace('képviselő-testület=elé|képviselő-testület[NOM]', 'képviselő-testület=elé').\
                        replace('ország-világ=elé|ország-világ[NOM]', 'ország-világ=elé').\
                        replace('jelleg[NOM]|jellég[PSe3]=fogva', 'jellég[PSe3]=fogva')

                arg = arg.replace('[PSe3]', '').replace('=felé|felé[NOM]', '=felé'). \
                    replace('=közé|közé[NOM]', '=közé'). \
                    replace('=mellé|mellé[NOM]', '=mellé')

                if '|' not in arg and '=' in arg:
                    arg = '=' + arg.split('=')[1]
                if '|' not in arg and '=' not in arg:
                    try:
                        arg = '[' + arg.split('[')[1]
                    except IndexError:
                        arg = '[NOM]'
                if '|' in arg and '=' not in arg:
                    s = set()
                    for e in arg.split('|'):
                        try:
                            v = '[' + e.split('[')[1]
                        except IndexError:
                            v = '[NOM]'
                        if len(v) > 0:
                            s.add(v)
                    if len(s) > 1:
                        arg = '|'.join(s)
                    else:
                        arg = s.pop()
                new_frame.append(arg)
            new_frames.add(tuple(new_frame))
        else:
            new_frames.add(tuple())

    return new_frames


def print_stuff(arr, filename):
    with open(filename, 'w', encoding='UTF-8') as fname:
        for k, vs in sorted(arr.items(), key=lambda x: len(x[1]), reverse=True):
            if len(vs) > 1:
                print(k, file=fname)
                for key, val in sorted(vs.items(), key=lambda x: (-x[1], x[0])):
                    print('', key, val, sep='\t', file=fname)


def gen_patterns(pickled_name, w_verb_dict=True, w_isz=True, w_tade=True, w_inflist=True, w_mmo=True):
    frame_group_patt_to_id = Counter()
    id_to_frame_group_patt = defaultdict(str)
    frame_group_patt_count = Counter()

    prev_patt = defaultdict(Counter)
    patt_prev = defaultdict(Counter)

    verb_patt = defaultdict(Counter)
    patt_verb = defaultdict(Counter)

    verb_to_patt_prev = defaultdict(Counter)
    patt_prev_to_verb = defaultdict(Counter)

    (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (inflist_verbs, inflist_sumfreq), _, (mmo_verbs, mmo_sumfreq), all_ige \
        = pickle.load(gzip.open(pickled_name))

    all_ige = set()

    if w_verb_dict:
        all_ige |= set(verb_dict_verbs.keys())

    if w_isz:
        all_ige |= set(isz_verbs.keys())

    if w_inflist:
        all_ige |= set(inflist_verbs.keys())

    if w_tade:
        all_ige |= set(tade_verbs.keys())

    if w_mmo:
        all_ige |= set(tade_verbs.keys())

    prev_by_ige = defaultdict(set)
    for verb in sorted(all_ige):
        if '|' in verb:
            prev, verb = verb.split('|', maxsplit=1)
        else:
            prev = 'X'
        prev_by_ige[verb].add(prev)

    for verb, prevs in sorted(prev_by_ige.items()):
        print(verb, file=sys.stderr)
        for prev in sorted(prevs):
            if prev != 'X':
                v = prev + '|' + verb
            else:
                v = verb
            print('', prev, sep='\t', file=sys.stderr)

            all_frame = set()
            if w_verb_dict:
                verb_dict_frames = tuple([frame[1] for frame in verb_dict_verbs[v]])
                all_frame |= set(verb_dict_frames)

            if w_isz:
                isz_frames = tuple([frame[1] for frame in isz_verbs[v]])
                all_frame |= set(isz_frames)

            if w_inflist:
                inflist_frames = tuple([frame[1] for frame in inflist_verbs[v]])
                all_frame |= set(inflist_frames)

            if w_tade:
                tade_frames = tuple([frame[1] for frame in tade_verbs[v]])
                all_frame |= set(tade_frames)

            if w_mmo:
                mmo_frames = tuple(tuple(arg[1] for arg in frame[1]) for frame in mmo_verbs[verb])
                all_frame |= set(mmo_frames)

            frames = sorted(preprocess_frames(all_frame))
            frames_str = str(frames)
            if frames_str not in frame_group_patt_to_id:
                id_to_frame_group_patt[len(frame_group_patt_to_id)] = frames_str
                frame_group_patt_to_id[frames_str] = len(frame_group_patt_to_id)
                frame_group_patt_count[frames_str] += 1

            # Without verb
            prev_patt[prev][frames_str] += 1
            patt_prev[frames_str][prev] += 1

            # Without PreV
            verb_patt[verb][frames_str] += 1
            patt_verb[frames_str][verb] += 1

            # Verb to prev and frame_group and vice versa
            verb_to_patt_prev[verb][(prev, frames_str)] += 1
            patt_prev_to_verb[(prev, frames_str)][verb] += 1

            for frame in frames:
                print('', frame, sep='\t\t', file=sys.stderr)

    # Print results
    if not os.path.exists('patterns'):
        os.mkdir('patterns')
    print_stuff(prev_patt, os.path.join('patterns', 'prev_patt.txt'))
    print_stuff(patt_prev, os.path.join('patterns', 'patt_prev.txt'))

    print_stuff(verb_patt, os.path.join('patterns', 'verb_patt.txt'))
    print_stuff(patt_verb, os.path.join('patterns', 'patt_verb.txt'))

    print_stuff(verb_to_patt_prev, os.path.join('patterns', 'verb_to_patt_prev.txt'))
    print_stuff(patt_prev_to_verb, os.path.join('patterns', 'patt_prev_to_verb.txt'))
