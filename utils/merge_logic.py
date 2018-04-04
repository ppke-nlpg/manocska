#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from utils.read_resources import get_freq_w_ind_for_frame


def print_entry(verb, act_frame, szotar_freq, isz_freq, tade_freq, kagi_freq, kagi_freq_rank, inflist_freq,
                inflist_freq_rank, verb_dict_sumfreq, isz_sumfreq, tade_sumfreq):
    if act_frame == ():
        act_frame = '@'
    else:
        act_frame = ' '.join(act_frame)
    rank = sum((szotar_freq / verb_dict_sumfreq, isz_freq / isz_sumfreq, tade_freq / tade_sumfreq,
                kagi_freq_rank, inflist_freq_rank))
    print(verb, act_frame, szotar_freq, isz_freq, tade_freq, kagi_freq, inflist_freq,
          '{0:1.20f}'.format(rank), sep='\t')


def extract_inflist_freq_rank(verb, act_frame, inflist_verbs, inflist_sumfreq):
    inflist_freq = None
    inflist_freq_rank = 0
    if len(act_frame) > 0 and act_frame[0] == 'INF':
        inflist_freq = inflist_verbs.get(verb)
        if len(inflist_freq) == 0:
            inflist_freq = 0
        else:
            inflist_freq = inflist_freq[0][0]  # Freq for act frame
        inflist_freq_rank = inflist_freq / inflist_sumfreq
    return inflist_freq, inflist_freq_rank


def extract_kagi_freq_and_rank(verb, kagi_verbs, kagi_sumfreq):
    kagi_freq = None
    kagi_freq_rank = 0
    if '|' in verb:
        kagi_freq = kagi_verbs.get(verb, 0)
        kagi_freq_rank = kagi_freq / kagi_sumfreq
    return kagi_freq, kagi_freq_rank


def merge(*args):
    (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), all_ige = args

    for verb in sorted(all_ige):
        szotar_frames = tuple([frame[1] for frame in verb_dict_verbs[verb]])
        isz_frames = tuple([frame[1] for frame in isz_verbs[verb]])
        tade_frames = tuple([frame[1] for frame in tade_verbs[verb]])
        inflist_frames = tuple([frame[1] for frame in inflist_verbs[verb]])
        all_frame = set(szotar_frames) | set(isz_frames) | set(tade_frames) | set(inflist_frames)
        if len(szotar_frames) + len(isz_frames) + len(tade_frames) + len(inflist_frames) > len(all_frame):
            print(verb, list(sorted(set(szotar_frames) & set(isz_frames))),
                  list(sorted(set(isz_frames) & set(tade_frames))),
                  list(sorted(set(tade_frames) & set(szotar_frames))),
                  list(sorted(set(tade_frames) & set(inflist_frames))),  # TODO: document
                  kagi_verbs[verb], sep='\n', end='\n\n', file=sys.stderr)
        if len(all_frame) == 0:
            kagi_freq, kagi_freq_rank = extract_kagi_freq_and_rank(verb, kagi_verbs, kagi_sumfreq)
            print_entry(verb, ['???'], 0, 0, 0, kagi_freq, kagi_freq_rank, None, 0, verb_dict_sumfreq, isz_sumfreq,
                        tade_sumfreq)

        for act_frame in sorted(all_frame):
            szotar_freq = get_freq_w_ind_for_frame(verb_dict_verbs[verb], act_frame)[1]
            isz_freq = get_freq_w_ind_for_frame(isz_verbs[verb], act_frame)[1]
            tade_freq = get_freq_w_ind_for_frame(tade_verbs[verb], act_frame)[1]
            kagi_freq, kagi_freq_rank = extract_kagi_freq_and_rank(verb, kagi_verbs, kagi_sumfreq)
            inflist_freq, inflist_freq_rank = extract_inflist_freq_rank(verb, act_frame, inflist_verbs, inflist_sumfreq)
            print_entry(verb, act_frame, szotar_freq, isz_freq, tade_freq, kagi_freq, kagi_freq_rank, inflist_freq,
                        inflist_freq_rank, verb_dict_sumfreq, isz_sumfreq, tade_sumfreq)
