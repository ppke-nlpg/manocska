#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
from collections import defaultdict, Counter


def get_freq_w_ind_for_frame(frames, frame):
    for i, (freq, curr_frame) in enumerate(frames):
        if curr_frame == frame:
            return i, freq
    else:
        return -1, 0


def smart_append(verbs_dict, verb, freq, frame):
    if verb in verbs_dict:
        frame_ind, frame_freq = get_freq_w_ind_for_frame(verbs_dict[verb], frame)
        if frame_ind >= 0:
            verbs_dict[verb][frame_ind][0] = frame_freq + freq
            return
    verbs_dict[verb].append([freq, frame])

szotar_igek = defaultdict(list)
szotar_sumfreq = 0
with open('ige_szotar/szotar.kimenet.txt', encoding='UTF-8') as szotar:
    for l in szotar:
        l = l.strip().split('\t')
        if len(l) == 3:
            ige, gyak, pelda = l
            vonzatok = []
        elif len(l) >= 4:
            ige, *vonzatok, gyak, pelda = l
        else:
            break
        gyak = int(gyak)
        vonzatok = [i.replace(' =', '=') for i in vonzatok]  # Because at the end args will be separated by spaces
        szotar_igek[ige].append([gyak, tuple(sorted(vonzatok))])
        szotar_sumfreq += gyak

print('Igék száma (szótár): ', len(szotar_igek), file=sys.stderr)

isz_igek = defaultdict(list)
isz_sumfreq = 0
with open('isz/igeiszerkezet-lista.kimenet.txt', encoding='UTF-8') as isz:
    for l in isz:
        if not l.startswith((' 0', 'Igeskicc')):
            l = l.strip().split('\t')
            if len(l) == 2:
                ige, gyak = l
                vonzatok = []
            elif len(l) >= 3:
                ige, *vonzatok, gyak = l
            else:
                break
            gyak = int(gyak)
            vonzatok = [i.replace(' =', '=') for i in vonzatok]  # Because at the end args will be separated by spaces
            isz_igek[ige].append([gyak, tuple(sorted(vonzatok))])
            isz_sumfreq += gyak

print('Igék száma (igei szerkezetek): ', len(isz_igek), file=sys.stderr)

tade_igek = defaultdict(list)
tade_sumfreq = 0
with open('tade/tade.kimenet.tsv', encoding='UTF-8') as tade:
    for l in tade:
        l = l.strip().split('\t')
        if len(l) == 5:
            ige, vonzatok, gyak, igegyak, arany = l
            if vonzatok[0] == '@':
                vonzatok = ''
        elif len(l) >= 6:
            ige, vonzatok, gyak, igegyak, arany = l
        else:
            break
        vonzatok = tuple(vonzatok.split())
        gyak = int(gyak)
        if ' ' in ige:
            if ige.startswith('"'):
                print('Dropped: {0}'.format(ige), file=sys.stderr)
                continue
            ige, inf = ige.split()
            smart_append(tade_igek, inf, gyak, tuple(sorted(vonzatok)))  # Here stuff can be non uniq...
            tade_sumfreq += gyak
            vonzatok = ['INF_' + inf]
        smart_append(tade_igek, ige, gyak, tuple(sorted(vonzatok)))  # Here stuff can be non uniq...
        tade_sumfreq += gyak

print('Igék száma (Tadé): ', len(tade_igek), file=sys.stderr)

kagi_igek = Counter()
kagi_sumfreq = 0
with open('kagi_verbal_complex/freqPrevFin.txt', encoding='UTF-8') as kagi:
    for l in kagi:
        l = l.strip().split(' ')
        if len(l) == 2:
            gyak, ige = l
        else:
            break
        ik, igek = ige.split('+')
        gyak = int(gyak)
        for i in ('{0}|{1}'.format(ik, i) for i in igek.split('|')):  # One or more
            kagi_igek[ige] = gyak
            kagi_sumfreq += gyak

print('Igék száma (kagi): ', len(kagi_igek), file=sys.stderr)

all_ige = set(szotar_igek.keys()) | set(isz_igek.keys()) | set(tade_igek.keys())
print('Igék száma (összesen): ', len(all_ige), file=sys.stderr)

for ige in sorted(all_ige):
    szotar_ige = tuple([keret[1] for keret in szotar_igek[ige]])
    isz_ige = tuple([keret[1] for keret in isz_igek[ige]])
    tade_ige = tuple([keret[1] for keret in tade_igek[ige]])
    all_frame = set(szotar_ige) | set(isz_ige) | set(tade_ige)
    if len(szotar_ige) + len(isz_ige) + len(tade_ige) > len(all_frame):
        print(ige, list(sorted(set(szotar_ige) & set(isz_ige))), list(sorted(set(isz_ige) & set(tade_ige))),
              list(sorted(set(tade_ige) & set(szotar_ige))), kagi_igek[ige], file=sys.stderr)
    for act_frame in sorted(all_frame):
        szotar_freq = get_freq_w_ind_for_frame(szotar_igek[ige], act_frame)[1]
        isz_freq = get_freq_w_ind_for_frame(isz_igek[ige], act_frame)[1]
        tade_freq = get_freq_w_ind_for_frame(tade_igek[ige], act_frame)[1]
        kagi_freq = kagi_igek[ige]
        if act_frame == ():
            act_frame = '@'
        else:
            act_frame = ' '.join(act_frame)
        rank = szotar_freq / szotar_sumfreq + isz_freq / isz_sumfreq + tade_freq / tade_sumfreq \
            + kagi_freq / kagi_sumfreq
        print(ige, act_frame, szotar_freq, isz_freq, tade_freq, kagi_freq, rank, sep='\t')

"""
time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k6,6g | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt)
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
