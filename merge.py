#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys
import pickle
import gzip

from utils.merge_logic import merge, merge_xml
from utils.read_resources import read_resources_parallel
from utils.classify_patterns import gen_patterns

# Read, Correct & Pickle
(verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige \
        = read_resources_parallel('resources.pckl.gz')

"""
(verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige \
        = pickle.load(gzip.open('resources.pckl.gz'))
"""

# Merge
if len(sys.argv) > 1 and sys.argv[1] == '--XML':
    merge_xml((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
              (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige)
else:
    merge((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
          (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), (mmo_verbs, mmo_sumfreq), all_ige)

# Generate Patterns (currently alpha state, disabled)
# gen_patterns('resources.pcl')

"""
time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k9,9nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
