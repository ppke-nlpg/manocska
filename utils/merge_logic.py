#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
import locale
import copy
from collections import defaultdict, Counter
from itertools import repeat

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

from .read_resources import get_freq_w_ind_for_frame


def prev_split(verb):
    res = verb.split('|', maxsplit=1)
    prev, verb = 'X', res[0]
    if len(res) > 1:
        prev, verb = res
    return prev, verb


def extract_kagi_freq_and_rank(verb, kagi_verbs, kagi_sumfreq):
    kagi_freq = None
    kagi_freq_rank = 0
    if '|' in verb:
        kagi_freq = kagi_verbs.get(verb, 0)
        kagi_freq_rank = kagi_freq / kagi_sumfreq
    return kagi_freq, kagi_freq_rank


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


def compute_all_frames(verb, verb_dict_verbs, isz_verbs, tade_verbs, kagi_verbs, inflist_verbs, mmo_verbs):
    verb_dict_frames = tuple([frame[1] for frame in verb_dict_verbs[verb]])
    isz_frames = tuple(frame[1] for frame in isz_verbs[verb])
    tade_frames = tuple(frame[1] for frame in tade_verbs[verb])
    inflist_frames = tuple(frame[1] for frame in inflist_verbs[verb])
    mmo_frames = tuple(tuple(arg[1] for arg in frame[1]) for frame in mmo_verbs[verb])
    all_frame = set(verb_dict_frames) | set(isz_frames) | set(tade_frames) | set(inflist_frames) | set(mmo_frames)

    # INFO output  # TODO: MMO
    if len(verb_dict_frames) + len(isz_frames) + len(tade_frames) + len(inflist_frames) > len(all_frame):
        print(verb, list(sorted(set(verb_dict_frames) & set(isz_frames))),
              list(sorted(set(isz_frames) & set(tade_frames))),
              list(sorted(set(tade_frames) & set(verb_dict_frames))),
              list(sorted(set(tade_frames) & set(inflist_frames))),  # TODO: document
              kagi_verbs[verb], sep='\n', end='\n\n', file=sys.stderr)
    return all_frame


def print_entry(*args):
    verb, act_frame, (verb_dict_freq, verb_dict_sumfreq), (isz_freq, isz_sumfreq), (tade_freq, tade_sumfreq),\
        (kagi_freq, kagi_freq_rank), (inflist_freq, inflist_freq_rank), (mmo_freq, mmo_rank, _) = args

    if act_frame == ():
        act_frame = '@'
    else:
        act_frame = ' '.join(act_frame)
    rank = sum((verb_dict_freq / verb_dict_sumfreq, isz_freq / isz_sumfreq, tade_freq / tade_sumfreq,
                kagi_freq_rank, inflist_freq_rank, mmo_rank))
    print(verb, act_frame, verb_dict_freq, isz_freq, tade_freq, kagi_freq, inflist_freq, mmo_freq,
          '{0:1.20f}'.format(rank), sep='\t')


def merge(*args, print_fun=print_entry):
    (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_verb \
        = args

    non_inf_all = 0
    non_inf = Counter()
    inf_all = 0
    inf = Counter()

    for verb in sorted(all_verb):
        all_frame = compute_all_frames(verb, verb_dict_verbs, isz_verbs, tade_verbs, kagi_verbs, inflist_verbs,
                                       mmo_verbs)

        if len(all_frame) == 0:
            kagi_freq, kagi_freq_rank = extract_kagi_freq_and_rank(verb, kagi_verbs, kagi_sumfreq)
            print_fun(verb, ['???'], (0, verb_dict_sumfreq), (0, isz_sumfreq), (0, tade_sumfreq),
                      (kagi_freq, kagi_freq_rank), (None, 0), (0, 0, mmo_verbs[verb]))
            non_inf_all += 1
            non_inf[1] += 1

        mmo_frames = set(tuple(arg[1] for arg in frame[1]) for frame in mmo_verbs[verb])
        for act_frame in sorted(all_frame):
            verb_dict_freq = get_freq_w_ind_for_frame(verb_dict_verbs[verb], act_frame)[1]
            isz_freq = get_freq_w_ind_for_frame(isz_verbs[verb], act_frame)[1]
            tade_freq = get_freq_w_ind_for_frame(tade_verbs[verb], act_frame)[1]
            kagi_freq, kagi_freq_rank = extract_kagi_freq_and_rank(verb, kagi_verbs, kagi_sumfreq)
            inflist_freq, inflist_freq_rank = extract_inflist_freq_rank(verb, act_frame, inflist_verbs, inflist_sumfreq)
            mmo_freq = int(act_frame in mmo_frames)
            mmo_rank = mmo_freq/mmo_sumfreq

            # How many resource contanins the frame...
            c = sum(int(f > 0) for f in (verb_dict_freq, isz_freq, tade_freq, kagi_freq_rank,
                                         inflist_freq_rank, mmo_freq))
            if act_frame == ('INF',):
                inf_all += 1
                inf[c] += 1
            else:
                non_inf_all += 1
                non_inf[c] += 1

            print_fun(verb, act_frame, (verb_dict_freq, verb_dict_sumfreq), (isz_freq, isz_sumfreq),
                      (tade_freq, tade_sumfreq), (kagi_freq, kagi_freq_rank), (inflist_freq, inflist_freq_rank),
                      (mmo_freq, mmo_rank, mmo_verbs[verb]))

    # Print some stats...
    print('INF (all): ', inf_all, file=sys.stderr)
    for k, v in inf.items():
        print('INF ({0} resource(s)): '.format(k), v, file=sys.stderr)
    print('NON-INF (all): ', non_inf_all, file=sys.stderr)
    for k, v in non_inf.items():
        print('NON-INF ({0} resource(s)): '.format(k), v, file=sys.stderr)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'UTF-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def print_entry_xml_fun(verb_index):
    inf_node_index = {}
    no_inf_node_index = {}

    def print_entry_xml(*args):
        verb, act_frame, (verb_dict_freq, verb_dict_sumfreq), (isz_freq, isz_sumfreq), (tade_freq, tade_sumfreq),\
           (kagi_freq, kagi_freq_rank), (inflist_freq, inflist_freq_rank), (mmo_freq, mmo_rank, mmo_frames) = args

        mmo_compatible_frames = [frame for frame in mmo_frames if tuple(arg[1] for arg in frame[1]) == act_frame]

        rank = '{0:1.20f}'.format(sum((verb_dict_freq / verb_dict_sumfreq, isz_freq / isz_sumfreq,
                                       tade_freq / tade_sumfreq, kagi_freq_rank, inflist_freq_rank, mmo_rank)))
        freq_dict = {'verb_dict': verb_dict_freq, 'isz': isz_freq, 'tade': tade_freq, 'finInf': inflist_freq,
                     'mmo': mmo_freq}

        # Locate subtree
        preve = verb_index[verb]

        # Has any arguments?
        if act_frame == ['???']:
            preve.set('kagilist', str(kagi_freq))
            preve.set('rank', rank)
            return

        # Has INF argument or not...
        if act_frame == ('INF',):
            if verb not in inf_node_index:
                inf_node_index[verb] = SubElement(preve, 'inf', rank=rank)

            # Add freqs
            SubElement(inf_node_index[verb], 'freqs', {k: str(v) for k, v in freq_dict.items()
                                                       if v is not None and v > 0})

        else:
            if verb not in no_inf_node_index:
                infe = SubElement(preve, 'no_inf')
                # Put Frames frame an arg and freqs
                no_inf_node_index[verb] = SubElement(infe, 'frames')

            if len(mmo_compatible_frames) == 0:
                create_frame_node(act_frame, no_inf_node_index[verb], rank, freq_dict)
            else:
                for mmo_frame in mmo_compatible_frames:
                    create_frame_node(act_frame, no_inf_node_index[verb], rank, freq_dict, mmo_frame)

    def create_frame_node(act_frame, frames, rank, freq_dict, mmo_frame=(None, ())):
        attrdict = {}
        # if mmo_frame is not None:
        #    attrdict = {'mmo_id': mmo_frame[0]['mmoid'], 'en': mmo_frame[0]['EN.VP']}

        mmo_arg_dict = {arg[1]: {ak.strip(':'): av.strip('"') for ak, av in arg[0].items()} for arg in mmo_frame[1]}
        frame = SubElement(frames, 'frame', rank=rank, **attrdict)
        args = SubElement(frame, 'args')
        # Add args
        if act_frame == ():
            SubElement(args, 'no_arg')
        else:
            for arg in act_frame:
                lex = ''
                case = ''
                postp = ''
                if '=' in arg:
                    lex, postp = arg.split('=', maxsplit=1)
                elif '[' in arg:
                    lex, case = arg.rsplit('[', maxsplit=1)
                    case = '[' + case
                arg_dict = copy.deepcopy(mmo_arg_dict.get(arg, {}))
                if len(lex) > 0:
                    arg_dict['lex'] = lex
                if len(case) > 0:
                    arg_dict['case'] = case
                if len(postp) > 0:
                    arg_dict['postp'] = postp
                SubElement(args, 'arg', **arg_dict)
        # Add freqs
        SubElement(frame, 'freqs', {k: str(v) for k, v in freq_dict.items() if v is not None and v > 0})

        return frame

    return print_entry_xml


def add_child_with_attrs(root, elem_val, tag, key, vals, other_attrs=None, parent=None):
    """ElementTree helper function"""
    elem_index = {}
    if other_attrs is None:
        other_attrs = {}
    if parent is not None:
        root = SubElement(root, parent)
    for k, v in zip(repeat(key), sorted(vals, key=locale.strxfrm)):
        elem_index['|'.join((v, elem_val))] = SubElement(root, tag, **{k: v}, **other_attrs.get(v, {}))
    return elem_index


def merge_xml(*args):
    _, _, _, _, _, _, all_ige = args

    # Precompute values
    verbs = defaultdict(set)
    for verb in sorted(all_ige):
        prev, verb = prev_split(verb)
        if len(prev) > 0:
            verbs[verb].add(prev)
        else:
            verbs[verb].add('X')

    # Create root
    top = Element('manocska')

    # Add verbs
    add_child_with_attrs(top, '', 'verb', 'lex', verbs.keys())

    verb_index = {}
    # Add PreVs
    for verb, prevs in verbs.items():
        # Select Verb (None if not found):
        ve = top.find('verb[@lex="{0}"]'.format(verb))
        if ve is None:
            raise KeyError('Verb {0} not found!'.format(verb))

        if 'X' in prevs:
            verb_index[verb] = SubElement(ve, 'no_prev')
            prevs.remove('X')
        verb_index.update(add_child_with_attrs(ve, verb, 'prev', 'lex', prevs, parent='prevs'))

    # Add frames
    merge(*args, print_fun=print_entry_xml_fun(verb_index))
    print(prettify(top))
