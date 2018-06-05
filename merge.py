#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import pickle
import gzip
import argparse

from utils.merge_logic import merge, merge_xml
from utils.read_resources import read_resources_parallel
from utils.classify_patterns import gen_patterns


def main(args):
    if not args.read_pickle:
        # Read, Correct & Pickle
        (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
            (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige \
            = read_resources_parallel(args.pickle_name)
    else:
        # Load Pickled resources
        (verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
                (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige \
                = pickle.load(gzip.open(args.pickle_name))

    # Merge
    if args.XML:
        merge_xml((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
                  (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige)
    elif args.TSV:
        merge((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
              (kagi_verbs, kagi_sumfreq), (inflist_verbs, inflist_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige)
    elif args.gen_patterns:
        # Generate Patterns (currently beta state)
        gen_patterns(args.pickle_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--XML', help='Generate XML format', action='store_true', default=False)
    group.add_argument('--TSV', help='Generate TSV format', action='store_true', default=False)
    group.add_argument('--gen-patterns', help='Generate patterns', action='store_true', default=False)

    parser.add_argument('--pickle-file', help='The pickle file to save read resources', action="store",
                        dest='pickle_name', default='resources.pckl.gz')
    parser.add_argument('--read-pickle', help='Read resources from pickle', action="store_true", default=False)

    cli_args = parser.parse_args()
    main(cli_args)


"""
time (python3 merge.py --TSV 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k9,9nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
