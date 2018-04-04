#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
import sys

from collections import defaultdict, Counter

"""
from utils.correction_tables import never_prev_verbs, light_verb_exception_verbs, not_prev_verbs, not_prev_verbs2, \
    false_prev_good, funny_ik_replacements, good_verbs_humor_not_recognised, good_verbs_humor_not_recognised2,\
    good_verbs_humor_not_recognised3, double_prev_verbs, not_rev_verbs_drop_prev, funny_prev_drop_prev, \
    not_prev_verbs3, verb_add_ik_suffix, prev_and_ik_verbs, del_prev_and_add_ik
"""

from utils.correction_tables import wrong_verbs, wrong_verbs2, not_prev_verbs_TODO_FR, verb_bad_prev, wrong_verbs3, \
    bad_forms, bad_forms2, fix_verb


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


def ige_szotar_process():
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
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev \
                    or verb in wrong_verbs3 or verb in bad_forms or verb in bad_forms2:
                found_wrong_verbs.add(verb)
                continue
            verb_new = fix_verb(verb)
            if verb_new != verb:
                found_wrong_verbs.add(verb)
            verb = verb_new
            arguments = [i.replace(' =', '=') for i in arguments]  # Because at the end args will be separated by spaces
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
                if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or \
                        verb in verb_bad_prev or verb in wrong_verbs3 or verb in bad_forms or verb in bad_forms2:
                    found_wrong_verbs.add(verb)
                    continue
                verb_new = fix_verb(verb)
                if verb_new != verb:
                    found_wrong_verbs.add(verb)
                verb = verb_new
                arguments = [i.replace(' =', '=') for i in
                             arguments]  # Because at the end args will be separated by spaces
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
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev\
                    or verb in wrong_verbs3 or verb in bad_forms or verb in bad_forms2:
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
                if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or \
                        verb in verb_bad_prev or verb in wrong_verbs3 or verb in bad_forms or verb in bad_forms2:
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
            if verb in wrong_verbs or verb in wrong_verbs2 or verb in not_prev_verbs_TODO_FR or verb in verb_bad_prev\
                    or verb in wrong_verbs3 or verb in bad_forms or verb in bad_forms2:
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
