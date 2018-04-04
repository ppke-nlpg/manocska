#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from collections import defaultdict, Counter

import pickle


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


def gen_patterns(pickled_name, w_tade=True):
    c = Counter()
    crev = defaultdict(str)
    c2 = Counter()
    # d = defaultdict(list)

    prev_patt = defaultdict(Counter)
    patt_prev = defaultdict(Counter)

    verb_patt = defaultdict(Counter)
    patt_verb = defaultdict(Counter)

    verb_to_patt_prev = defaultdict(Counter)
    patt_prev_to_verb = defaultdict(Counter)

    verb_dict_verbs, isz_verbs, tade_verbs, _, inflist_verbs = pickle.load(open(pickled_name, 'rb'))

    all_ige = set(verb_dict_verbs.keys()) | set(isz_verbs.keys()) | set(inflist_verbs.keys())
    if w_tade:
        all_ige |= set(tade_verbs.keys())

    prev_by_ige = defaultdict(set)
    for verb in sorted(all_ige):
        if '|' in verb:
            prev, verb = verb.split('|', maxsplit=1)
        else:
            prev = 'X'
        prev_by_ige[verb].add(prev)

    for verb, prevs in sorted(prev_by_ige.items()):
        print(verb)
        for prev in sorted(prevs):
            if prev != 'X':
                v = prev + '|' + verb
            else:
                v = verb
            print('', prev, sep='\t')

            szotar_frames = tuple([frame[1] for frame in verb_dict_verbs[v]])
            isz_frames = tuple([frame[1] for frame in isz_verbs[v]])
            tade_frames = tuple([frame[1] for frame in tade_verbs[v]])
            inflist_frames = tuple([frame[1] for frame in inflist_verbs[v]])
            all_frame = set(szotar_frames) | set(isz_frames) | set(inflist_frames)
            if w_tade:
                all_frame |= set(tade_frames)
            frames = sorted(preprocess_frames(all_frame))
            frames_str = str(frames)
            if frames_str not in c:
                crev[len(c)] = frames_str
                c[frames_str] = len(c)
                c2[frames_str] += 1
                # d[tuple(frames)] = []

            prev_patt[prev][frames_str] += 1
            patt_prev[frames_str][prev] += 1

            verb_patt[verb][frames_str] += 1
            patt_verb[frames_str][verb] += 1

            verb_to_patt_prev[verb][(prev, frames_str)] += 1
            patt_prev_to_verb[(prev, frames_str)][verb] += 1

            # for frame in frames:
            #     print('', frame, sep='\t\t')

    # Print results
    if w_tade:
        print_stuff(prev_patt, 'prev_patt_w_tádé.txt')
        print_stuff(patt_prev, 'patt_prev_w_tádé.txt')

        print_stuff(verb_patt, 'verb_patt_w_tádé.txt')
        print_stuff(patt_verb, 'patt_verb_w_tádé.txt')

        print_stuff(verb_to_patt_prev, 'verb_to_patt_prev_w_tádé.txt')
        print_stuff(patt_prev_to_verb, 'patt_prev_to_verb_w_tádé.txt')
    else:

        print_stuff(prev_patt, 'prev_patt.txt')
        print_stuff(patt_prev, 'patt_prev.txt')

        print_stuff(verb_patt, 'verb_patt.txt')
        print_stuff(patt_verb, 'patt_verb.txt')

        print_stuff(verb_to_patt_prev, 'verb_to_patt_prev.txt')
        print_stuff(patt_prev_to_verb, 'patt_prev_to_verb.txt')

# Preliminary (alpha code) distance calculation between patterns


"""
print("ennyi", len(c), '\n\n')
common = c2.most_common(10)
a = '\n'.join(str(i) for i in common)
print(a)

pickle.dump(d, open('mintak.pcl', 'wb'))
"""
"""
mintak = pickle.load(open('mintak.pcl', 'rb'))
mintak_keys = set(mintak.keys())

import distance
max_dist = 5
NOT_FOUND = 3
maximum_dist = 3
done = set()
not_done = mintak_keys.copy()
print(len(mintak_keys), file=sys.stderr)
for m1 in sorted(mintak_keys):
    not_done -= {m1}
    for j, m2 in enumerate(not_done):
        print('keys:', j,'/',len(not_done), file=sys.stderr)
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
            #print(i,'/', len(elso), file=sys.stderr)
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
                    dist += NOT_FOUND
            else:
                dist += NOT_FOUND
            if dist > max_dist:
                break
        if dist <= max_dist:
            mintak[m1].append(m2)
            mintak[m2].append(m1)
    done.add(m1)
    #if len(done) %  == 0:
    print(len(done), file=sys.stderr)

pickle.dump(d, open('hasonlo_mintak.pcl', 'wb'))
for k, v in mintak.items():
    if len(v) > 0:
        print(k, v)

"""
