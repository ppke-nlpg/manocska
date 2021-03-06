#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import os
import sys
import gzip
import pickle

from collections import defaultdict, Counter


def preprocess_frames(frames, verb, freqs) -> set:
    new_frames = set()
    for frame in frames:
        freq, frame = frame
        if len(frame) > 0:
            new_frame = []
            for arg in frame:
                if ('INF',) == frame:
                    new_frame = frame
                    break
                if '|' in arg and '=' in arg:
                    arg = arg.replace('ország-világ=előtt|ország-világ[Nom]', 'ország-világ=előtt').\
                        replace('frakcióvezető-helyettes[Nom]|frakcióvezető-helyettes=szerint',
                                'frakcióvezető-helyettes[Poss]=szerint').\
                        replace('frakcióvezető-helyettes[Nom]|frakcióvezető-helyettes[Poss]=szerint',
                                'frakcióvezető-helyettes[Poss]=szerint').\
                        replace('telek[Nom]|tél=belül', 'tél=belül').\
                        replace('közvélemény-kutatás=szerint|közvélemény-kutatás[Nom]', 'közvélemény-kutatás=szerint').\
                        replace('ország-világ=előtt|ország-világ[Nom]', 'ország-világ=előtt').\
                        replace('képviselő-testület=elé|képviselő-testület[Nom]', 'képviselő-testület=elé').\
                        replace('ország-világ=elé|ország-világ[Nom]', 'ország-világ=elé').\
                        replace('jelleg[Nom]|jellég[Poss]=fogva', 'jellég[Poss]=fogva')

                arg = arg.replace('[Poss]', '').replace('=felé|felé[Nom]', '=felé'). \
                    replace('=közé|közé[Nom]', '=közé'). \
                    replace('=mellé|mellé[Nom]', '=mellé')

                if '|' not in arg and '=' in arg:
                    arg = '=' + arg.split('=')[1]
                if '|' not in arg and '=' not in arg:
                    try:
                        arg = '[' + arg.split('[')[1]
                    except IndexError:
                        arg = '[Nom]'
                if '|' in arg and '=' not in arg:
                    s = set()
                    for e in arg.split('|'):
                        try:
                            v = '[' + e.split('[')[1]
                        except IndexError:
                            v = '[Nom]'
                        if len(v) > 0:
                            s.add(v)
                    if len(s) > 1:
                        arg = '|'.join(s)
                    else:
                        arg = s.pop()
                new_frame.append(arg)
            new_frame = tuple(new_frame)
            new_frames.add(new_frame)
        else:
            new_frame = tuple()
            new_frames.add(tuple())
        freqs[(verb, new_frame)] = max(freq, freqs.get((verb, new_frame), 0))

    return new_frames


def print_stuff(arr, filename, freqs, key1=lambda x: -len(x[1]), key2=lambda x: (-x[1], x[0])):
    with open(filename, 'w', encoding='UTF-8') as fname:
        for k, vs in sorted(arr.items(), key=key1):
            if len(vs) > 1:
                print(k, file=fname)
                for key, val in sorted(vs.items(), key=key2):
                    print('', key, val, *freqs[(k, key)], sep='\t', file=fname)


def norm(tup):
    if not any(tup):
        return None
    if len(tup) == 1:
        return tup[0]
    return tup


def gen_patterns(pickled_name, w_verb_dict=True, w_isz=True, w_tade=True, w_inflist=True, w_mmo=True):
    frame_group_patt_to_id = Counter()
    id_to_frame_group_patt = defaultdict(tuple)
    frame_group_patt_count = Counter()

    prev_patt = defaultdict(Counter)
    patt_prev = defaultdict(Counter)

    verb_patt = defaultdict(Counter)
    patt_verb = defaultdict(Counter)

    verb_to_prev_patt = defaultdict(Counter)
    prev_patt_to_verb = defaultdict(Counter)

    (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        _, (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige \
        = pickle.load(gzip.open(pickled_name))

    all_ige = set()

    if w_verb_dict:
        all_ige |= set(verb_dict_verbs.keys())

    if w_isz:
        all_ige |= set(isz_verbs.keys())

    if w_tade:
        all_ige |= set(tade_verbs.keys())

    if w_inflist:
        all_ige |= set(inflist_verbs.keys())

    if w_mmo:
        all_ige |= set(tade_verbs.keys())

    prev_by_ige = defaultdict(set)
    for verb in sorted(all_ige):
        if '|' in verb:
            prev, verb = verb.split('|', maxsplit=1)
        else:
            prev = 'X'
        prev_by_ige[verb].add(prev)

    verb_dict_freqs = {}
    isz_freqs = {}
    inflist_freqs = {}
    tade_freqs = {}
    mmo_freqs = {}
    freqs_to_frames = {}
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
                verb_dict_frames = tuple(frame for frame in verb_dict_verbs[v])
                verb_dict_frames_preped = preprocess_frames(verb_dict_frames, (prev, verb), verb_dict_freqs)
                all_frame |= set(verb_dict_frames_preped)

            if w_isz:
                isz_frames = tuple(frame for frame in isz_verbs[v])
                isz_frames_preped = preprocess_frames(isz_frames, (prev, verb), isz_freqs)
                all_frame |= set(isz_frames_preped)

            if w_tade:
                tade_frames = tuple(frame for frame in tade_verbs[v])
                tade_frames_preped = preprocess_frames(tade_frames, (prev, verb), tade_freqs)
                all_frame |= set(tade_frames_preped)

            if w_inflist:
                inflist_frames = tuple(frame for frame in inflist_verbs[v])
                inflist_frames_preped = preprocess_frames(inflist_frames, (prev, verb), inflist_freqs)
                all_frame |= set(inflist_frames_preped)

            if w_mmo:
                mmo_frames = tuple([1, tuple(arg[1] for arg in frame[1])] for frame in mmo_verbs[v])
                mmo_frames_preped = preprocess_frames(mmo_frames, (prev, verb), mmo_freqs)
                all_frame |= set(mmo_frames_preped)

            frames = tuple(sorted(all_frame))
            verb_dict_freqs_for_frames = norm(tuple(verb_dict_freqs.get(((prev, verb), frame)) for frame in frames))
            isz_freqs_for_frames = norm(tuple(isz_freqs.get(((prev, verb), frame)) for frame in frames))
            tade_freqs_for_frames = norm(tuple(tade_freqs.get(((prev, verb), frame)) for frame in frames))
            inflist_freqs_for_frames = norm(tuple(inflist_freqs.get(((prev, verb), frame)) for frame in frames))
            mmo_freqs_for_frames = norm(tuple(mmo_freqs.get(((prev, verb), frame)) for frame in frames))

            freqs_to_frames[((prev, verb), frames)] = (verb_dict_freqs_for_frames, isz_freqs_for_frames,
                                                       tade_freqs_for_frames, inflist_freqs_for_frames,
                                                       mmo_freqs_for_frames)
            if frames not in frame_group_patt_to_id:
                id_to_frame_group_patt[len(frame_group_patt_to_id)] = frames
                frame_group_patt_to_id[frames] = len(frame_group_patt_to_id)
                frame_group_patt_count[frames] += 1

            # Without verb
            prev_patt[prev][frames] += 1
            patt_prev[frames][prev] += 1

            # Without PreV
            verb_patt[verb][frames] += 1
            patt_verb[frames][verb] += 1

            # Verb to prev and frame_group and vice versa
            verb_to_prev_patt[verb][(prev, frames)] += 1
            prev_patt_to_verb[(prev, frames)][verb] += 1

            for frame in frames:
                print('', frame, sep='\t\t', file=sys.stderr)

    print()
    print('Total', len(frame_group_patt_to_id), '\n\n', file=sys.stderr)

    # Print results to file
    if not os.path.exists('patterns'):
        os.mkdir('patterns')

    prev_patt_freqs = {(prev, patt): freq for ((prev, verb), patt), freq in sorted(freqs_to_frames.items())}
    print_stuff(prev_patt, os.path.join('patterns', 'prev_patt.txt'), prev_patt_freqs)

    patt_prev_freqs = {(patt, prev): freq for ((prev, verb), patt), freq in sorted(freqs_to_frames.items())}
    print_stuff(patt_prev, os.path.join('patterns', 'patt_prev.txt'), patt_prev_freqs)

    ################################################################################################
    verb_patt_freqs = {(verb, patt): freq for ((prev, verb), patt), freq in sorted(freqs_to_frames.items())}
    print_stuff(verb_patt, os.path.join('patterns', 'verb_patt.txt'), verb_patt_freqs)

    patt_verb_freqs = {(patt, verb): freq for ((prev, verb), patt), freq in sorted(freqs_to_frames.items())}
    print_stuff(patt_verb, os.path.join('patterns', 'patt_verb.txt'), patt_verb_freqs)

    ################################################################################################
    verb_to_prev_patt_freqs = {(verb, (prev, patt)): freq
                               for ((prev, verb), patt), freq in freqs_to_frames.items()}
    print_stuff(verb_to_prev_patt, os.path.join('patterns', 'verb_to_prev_patt.txt'), verb_to_prev_patt_freqs)

    prev_patt_to_verb_freqs = {((prev, patt), verb): freq
                               for ((prev, verb), patt), freq in freqs_to_frames.items()}
    print_stuff(prev_patt_to_verb, os.path.join('patterns', 'prev_patt_to_verb.txt'), prev_patt_to_verb_freqs,
                key1=lambda x: x)

    return frame_group_patt_count
