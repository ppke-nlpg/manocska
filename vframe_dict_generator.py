#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-
"""
    author: Noémi Vadász
    last update: 2018.01.11.

    VFrame dictionary compiler

    input
        verb+prev list                                          https://github.com/kagnes/hungarian_verbal_complex
        verb+inf list                                           https://github.com/kagnes/infinitival_constructions

    output
        vframe_to_read      human-readable form of dictionary
            one verb per line
                őriz	?, meg: X
            ?           infinitival argument with no preverb
            meg: ?  infinitival argument with the preverb
            meg: X  no infinitival argument with the preverb

        vframe_to_eval      input for VFrame searcher           https://github.com/ppke-nlpg/vframe
            one verb per line
                őriz    X:?, meg:X
            X:?         infinitival argument with no preverb
            meg:?   infinitival argument with the preverb
            meg:X   no infinitival argument with the preverb

        vframe_dict.py      input for AnaGramma                 https://github.com/ppke-nlpg/TO_BE_RELEASED # TODO
            python dictionary, one verb per line
                'őriz#V': {'X#PreV': '?', 'meg#PreV': 'X'},

"""

from collections import defaultdict
from itertools import chain
import locale
locale.setlocale(locale.LC_ALL, 'hu_HU.utf8')


class VFrameDefaultDict(defaultdict):
    def __str__(self):
        return '{0}'.format(','.join(self._add_x(('{0}:{1}'.format(k, v)
                                                  for k, v in sorted(self.items(), key=lambda x: locale.strxfrm(str(x)))
                                                  if k != 'X'), repr_format='eval')))

    def __repr__(self):
        return '{0}}},'.format(', '.join(self._add_x(("{0}#PreV': {1}".format(repr(k)[:-1], repr(v))
                                                      for k, v in sorted(self.items(),
                                                                         key=lambda x: locale.strxfrm(str(x)))
                                                      if k != 'X'), repr_format='dict')))

    def toreadable(self):
        return '{0}'.format(', '.join(self._add_x('{0}: {1}'.format(k, v)
                                                  for k, v in sorted(self.items(), key=lambda x: locale.strxfrm(str(x)))
                                                  if k != 'X')))

    def _add_x(self, dict_iter, repr_format='read'):
        x = self.get('X')
        if x is not None:
            if repr_format == 'dict':
                return chain(["'X#PreV': '{0}'".format(x)], dict_iter)
            elif repr_format == 'eval':
                return chain(['X:{0}'.format(x)], dict_iter)
            else:
                return chain([x], dict_iter)

        return dict_iter


def split_and_store_verb_w_prev(verb_w_prev, vframe, value):
    prev, verb = verb_w_prev.split('+', maxsplit=1)  # prev-verb separator: +

    if '|' in verb:
        first_verb, second_verb = verb.split('|', maxsplit=1)
        inverted = second_verb + '|' + first_verb
        vframe[first_verb][prev] = 'X'
        vframe[second_verb][prev] = 'X'
        vframe[inverted][prev] = 'X'

    if '-' in prev:  # to store 'be-be' type preverbs and 'be' too
        vframe[verb][prev.split('-', maxsplit=1)[0]] = value
    vframe[verb][prev] = value


def main():

    # defaultdict collection for VFrame
    vframe = VFrameDefaultDict(lambda: VFrameDefaultDict(str))

    # read freqPrevFin.txt (https://github.com/kagnes/hungarian_verbal_complex)
    with open('kagi_verbal_complex/freqPrevFin.txt', encoding='UTF-8') as prev_list:
        for line in prev_list:  # put instance to vframe structure with default None infinitival argument
            split_and_store_verb_w_prev(line.strip().split(maxsplit=1)[1], vframe, 'X')

    # read FinInf.txt (https://github.com/kagnes/infinitival_constructions)
    with open('infinitival_constructions/FinInf.txt', encoding='UTF-8') as inf_list:
        for line in inf_list:
            infline = line.strip().split('\t', maxsplit=5)
            if len(infline) == 6 and '%' in infline[5]:  # manually corrected verb stem or preverb-verb segmentation
                verb_w_prev = infline[5].lstrip('%')
            else:
                verb_w_prev = infline[1]

            if '+' in verb_w_prev:  # prev-verb separator: +
                split_and_store_verb_w_prev(verb_w_prev, vframe, '?')  # ? allows infinitival argument
            else:
                verb = verb_w_prev
                vframe[verb]['X'] = '?'

    # print results: input for evaluating VFrame algorithm and formatted input for AnaGramma VFrame module
    with open('vframe_dict/vframe_dict.py', 'w', encoding='UTF-8') as vframe_dict, \
            open('vframe_dict/vframe_to_eval', 'w', encoding='UTF-8') as vframe_to_eval, \
            open('vframe_dict/vframe_to_read', 'w', encoding='UTF-8') as vframe_to_read:

        print('#!/usr/bin/env python3',
              '# -*- coding: utf-8, vim: expandtab:ts=4 -*-',
              '',
              'verb_prev_restrs_dict = {', sep='\n', file=vframe_dict)

        for v, prevs in sorted(vframe.items(), key=lambda x: locale.strxfrm(str(x))):
            print("    '{0}#V': {{".format(v), repr(prevs), sep='', file=vframe_dict)
            print('{0}\t'.format(v), str(prevs), sep='', file=vframe_to_eval)
            print('{0}\t'.format(v), prevs.toreadable(), sep='', file=vframe_to_read)

        print('}', file=vframe_dict)


if __name__ == '__main__':
    main()
