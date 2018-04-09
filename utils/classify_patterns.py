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
            new_frame = tuple(new_frame)
            new_frames.add(new_frame)
        else:
            new_frame = tuple()
            new_frames.add(tuple())
        freqs[(verb, new_frame)] = max(freq, freqs.get((verb, new_frame), 0))

    return new_frames


def print_stuff(arr, filename, freqs):
    with open(filename, 'w', encoding='UTF-8') as fname:
        for k, vs in sorted(arr.items(), key=lambda x: len(x[1]), reverse=True):
            if len(vs) > 1:
                print(k, file=fname)
                for key, val in sorted(vs.items(), key=lambda x: (-x[1], x[0])):
                    """
                    d = freqs[0]
                    kk = (k, key)
                    a = d.get(kk)
                    """
                    print('', key, val, freqs[0].get((k, key)), freqs[1].get((k, key)), freqs[2].get((k, key)),
                          freqs[3].get((k, key)), freqs[4].get((k, key)), sep='\t', file=fname)


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

    verb_dict_freqs = {}
    isz_freqs = {}
    inflist_freqs = {}
    tade_freqs = {}
    mmo_freqs = {}
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

            if w_inflist:
                inflist_frames = tuple(frame for frame in inflist_verbs[v])
                inflist_frames_preped = preprocess_frames(inflist_frames, (prev, verb), inflist_freqs)
                all_frame |= set(inflist_frames_preped)

            if w_tade:
                tade_frames = tuple(frame for frame in tade_verbs[v])
                tade_frames_preped = preprocess_frames(tade_frames, (prev, verb), tade_freqs)
                all_frame |= set(tade_frames_preped)

            if w_mmo:
                mmo_frames = tuple([1, tuple(arg[1] for arg in frame[1])] for frame in mmo_verbs[v])
                mmo_frames_preped = preprocess_frames(mmo_frames, (prev, verb), mmo_freqs)
                all_frame |= set(mmo_frames_preped)

            frames = sorted(all_frame)
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

    print()
    print('Total', len(frame_group_patt_to_id), '\n\n', file=sys.stderr)

    # Print results to file
    if not os.path.exists('patterns'):
        os.mkdir('patterns')

    freqs = (verb_dict_freqs, isz_freqs, tade_freqs, inflist_freqs, mmo_freqs)
    prev_patt_freqs = tuple({(prev, str([patt])): freq for ((prev, verb), patt), freq in freq_dict.items()}
                            for freq_dict in freqs)
    print_stuff(prev_patt, os.path.join('patterns', 'prev_patt.txt'), prev_patt_freqs)

    patt_prev_freqs = tuple({(str([patt]), prev): freq for ((prev, verb), patt), freq in freq_dict.items()}
                            for freq_dict in freqs)
    print_stuff(patt_prev, os.path.join('patterns', 'patt_prev.txt'), patt_prev_freqs)

    ################################################################################################
    verb_patt_freqs = tuple({(verb, str([patt])): freq for ((prev, verb), patt), freq in freq_dict.items()}
                            for freq_dict in freqs)
    print_stuff(verb_patt, os.path.join('patterns', 'verb_patt.txt'), verb_patt_freqs)

    patt_verb_freqs = tuple({(str([patt]), verb): freq for ((prev, verb), patt), freq in freq_dict.items()}
                            for freq_dict in freqs)
    print_stuff(patt_verb, os.path.join('patterns', 'patt_verb.txt'), patt_verb_freqs)

    ################################################################################################
    verb_to_patt_prev_freqs = tuple({(verb, (str([patt]), prev)): freq
                                     for ((prev, verb), patt), freq in freq_dict.items()}
                                    for freq_dict in freqs)
    print_stuff(verb_to_patt_prev, os.path.join('patterns', 'verb_to_patt_prev.txt'), verb_to_patt_prev_freqs)
    patt_prev_to_verb_freqs = tuple({((str([patt]), prev), verb): freq
                                     for ((prev, verb), patt), freq in freq_dict.items()}
                                    for freq_dict in freqs)
    print_stuff(patt_prev_to_verb, os.path.join('patterns', 'patt_prev_to_verb.txt'), patt_prev_to_verb_freqs)

    return frame_group_patt_count


def compute_distance(mintak):
    # Preliminary (alpha code) distance calculation between patterns
    mintak_keys = set(mintak.keys())

    import distance
    max_dist = 5
    not_found = 3
    maximum_dist = 3
    done = set()
    not_done = mintak_keys.copy()
    print(len(mintak_keys), file=sys.stderr)
    for m1 in sorted(mintak_keys):
        not_done -= {m1}
        for j, m2 in enumerate(not_done):
            print('keys:', j, '/', len(not_done), file=sys.stderr)
            if m1 == m2:
                continue
            if len(m1) < len(m2):
                elso = m1
                masodik = m2
            else:
                elso = m2
                masodik = m1
            dist = 0
            occupied = set()
            for i, elso_frame in enumerate(elso):
                maradek = set(masodik) - occupied
                if len(maradek) > 0:
                    dk = set()
                    for masodik_frame in maradek:
                        dis = distance.levenshtein(elso_frame, masodik_frame, max_dist=maximum_dist)
                        if dis >= 0:
                            dk.add((dis, masodik_frame))
                    if len(dk) > 0:
                        cost, nyertes = min(dk, key=lambda x: x[0])
                        occupied.add(nyertes)
                        dist += cost
                    else:
                        dist += not_found
                else:
                    dist += not_found
                if dist > max_dist:
                    break
            if dist <= max_dist:
                mintak[m1].append(m2)
                mintak[m2].append(m1)
        done.add(m1)
        print(len(done), file=sys.stderr)

    pickle.dump(mintak, gzip.open('hasonlo_mintak.pcl', 'wb'))
    for k, v in mintak.items():
        if len(v) > 0:
            print(k, v)
