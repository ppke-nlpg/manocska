#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

from utils.merge_logic import merge
from utils.read_resources import read_resources_parallel

# Read & Correct
(verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq), \
        (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), all_ige \
        = read_resources_parallel('resources.pcl')

# Merge
merge((verb_dict_verbs, verb_dict_sumfreq), (isz_verbs, isz_sumfreq), (tade_verbs, tade_sumfreq),
      (inflist_verbs, inflist_sumfreq), (kagi_verbs, kagi_sumfreq), all_ige)

"""
time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k8,8nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
