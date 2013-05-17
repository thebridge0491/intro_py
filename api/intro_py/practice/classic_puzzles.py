# -*- coding: utf-8 -*-
'''Classic puzzles module

'''

from __future__ import (absolute_import, division, print_function,
    unicode_literals)

import logging, inspect
from future.builtins import (ascii, filter, hex, map, oct, zip, range)

__all__ = ['hanoi', 'hanoi_moves', 'nqueens', 'nqueens_grid']


MODULE_LOGGER = logging.getLogger(__name__)

def hanoi(src, dest, spare, num_disks):
    if 1 > num_disks: return []
    return (hanoi(src, spare, dest, num_disks - 1) + [(src, dest)] +
        hanoi(spare, dest, src, num_disks - 1))

def hanoi_moves(num_disks, ans):
    calc_len = int(2.0 ** num_disks) - 1
    def stat_txt(res_len):
        return '(n = {0}) 2**n - 1 = {1} {2} (length answer) = {3}'.format(
            num_disks, calc_len, '==' if calc_len == res_len else '!=',
            res_len)
    def hanoi_pegs(res):
        dict1 = {0: list(range(1, num_disks + 1)), 1: [], 2: []}
        def iter(dict_pegs, lst, acc):
            if [] == lst: return acc
            else:
                tup = lst[0]
                (el1, el2) = (tup[0] - 1, tup[1] - 1)
                lst2 = dict_pegs.get(el2, [])
                if [] == dict_pegs.get(el1, []): pegdn_dict = {}
                else:
                    rst = dict_pegs.get(el1, [])
                    dict_pegs[el1] = rst[1:]
                    dict_pegs[el2] = [rst[0]] + lst2
                    pegdn_dict = dict_pegs
                return iter(pegdn_dict, lst[1:],
                    [list(pegdn_dict.values())] + acc)
        return list(reversed(iter(dict1, res, [])))
    def proc(h_t):
        return "'move from {0} to {1}'".format(h_t[0], h_t[1])
    return ([stat_txt(len(ans)), '-' * 40], list(zip(map(proc, ans),
        hanoi_pegs(ans))))

def nqueens(num):
    def threatp(x1_y1, x2_y2):
        (x1, y1), (x2, y2) = x1_y1, x2_y2
        return (x1 == x2) or (y1 == y2) or (abs(x1 - x2) == abs(y1 - y2))
    def safep(pos, placed_set):
        if 0 == len(placed_set): return True
        else:
            return ((not threatp(pos, placed_set[0])) and
                safep(pos, placed_set[1:]))
    def iter(col, row, placed_set, board):
        if (num - 1) < col: return [list(reversed(placed_set))] + board
        elif (num - 1) < row: return board
        elif safep((col, row), placed_set):
            return iter(col, row + 1, placed_set,
                iter(col + 1, 0, [(col, row)] + placed_set, board))
        else: return iter(col, row + 1, placed_set, board)
    return iter(0, 0, [], [])

def nqueens_grid(num, ans):
    # from functools import reduce
    lst_n = list(range(num))
    lst_ltrs = [' '] + [chr(n + ord('a')) for n in lst_n]
    #
    # def mk_row(acc, col_row):
    #    (col, row) = col_row
    #    res = [str(row)] + list(map(lambda i: ('Q' if i == col
    #        else ' '), lst_n))
    #    return [res] + acc
    # grid = reduce(mk_row, sorted(ans, key=(lambda a1_a2: a1_a2[1])), [lst_ltrs])
    grid = sorted([x for (c, r) in ans for x in [[str(r)] +
        ['Q' if i == c else ' ' for i in lst_n]]], reverse=True) + [lst_ltrs]
    return grid


def lib_main(argv=None):
    print('hanoi(1, 2, 3, 4):', hanoi(1, 2, 3, 4))
    return 0

if '__main__' == __name__:
    sys.exit(lib_main(sys.argv[1:]))
