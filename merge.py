#!/usr/bin/python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

import sys

from utils.merge_logic import merge
from utils.read_resources import ige_szotar_process, isz_process, tade_process, kagi_verbs_process, kagi_inflist_process


verb_dict_sumfreq, verb_dict_wrong_verbs, verb_dict_verbs = ige_szotar_process()
print('No. of Verbs (ige_szotar): ', len(verb_dict_verbs), verb_dict_sumfreq, len(verb_dict_wrong_verbs),
      file=sys.stderr)

isz_sumfreq, isz_wrong_verbs, isz_verbs = isz_process()
print('No. of Verbs (isz): ', len(isz_verbs), isz_sumfreq, len(isz_wrong_verbs), file=sys.stderr)

tade_sumfreq, tade_wrong_verbs, tade_verbs = tade_process()
print('No. of Verbs (Tadé): ', len(tade_verbs), tade_sumfreq, len(tade_wrong_verbs), file=sys.stderr)

kagi_sumfreq, kagi_wrong_verbs, kagi_verbs = kagi_verbs_process()
print('No. of Verbs (kagi_verbal_complex): ', len(kagi_verbs), kagi_sumfreq, len(kagi_wrong_verbs), file=sys.stderr)

inflist_sumfreq, inflist_verbs = kagi_inflist_process()
print('No. of Verbs (inflist): ', len(inflist_verbs), inflist_sumfreq, file=sys.stderr)

all_ige = set(verb_dict_verbs.keys()) | set(isz_verbs.keys()) | set(tade_verbs.keys()) | set(inflist_verbs.keys()) | \
          set(kagi_verbs.keys())
print('No. of Verbs (total): ', len(all_ige), file=sys.stderr)

merge(verb_dict_sumfreq, isz_sumfreq, tade_sumfreq, inflist_verbs, inflist_sumfreq, kagi_verbs, kagi_sumfreq,
      all_ige, verb_dict_verbs, isz_verbs, tade_verbs)

"""
time (python3 merge.py 2> manocska.log.txt | tee manocska.txt | sort --parallel=$(nproc) -t$'\t' -k8,8nr -k1,2 | \
tee manocska.sorted.txt | grep -v $'[^\t ][=[]' > manocska.sorted.nolex.txt) &&
cat manocska.sorted.txt | grep $'[^\t ][=[]' > manocska.sorted.lex.txt
"""
