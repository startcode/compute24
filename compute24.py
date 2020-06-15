#!/usr/bin/env python

import itertools
import sys


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    return a / b


# All the operations and their names.
op_and_name = [(add, '+'), (sub, '-'), (mul, '*'), (div, '/')]


# Evaluate all possible combinations of nums. The result is a list of tuples.
# The first is a number, the second is how to compute this number.
def eval_num(nums):
    if len(nums) == 1:
        return [(nums[0], "%s" % nums[0])]
    results = []
    for i in range(1, len(nums)):
        # Divide the numbers into first half and second half
        first_half = eval_num(nums[0:i])
        second_half = eval_num(nums[i:])
        # Try each operation to combine first half and second half results.
        for op, name in op_and_name:
            for x1 in first_half:
                for x2 in second_half:
                    if name == '/':
                        if x2[0] == 0: continue
                        if x1[0] % x2[0] != 0: continue
                    results.append((op(x1[0], x2[0]),
                                    "(%s %s %s)" % (x1[1], name, x2[1])))
    return results


def search(nums):
    for n in set(itertools.permutations(nums)):
        for r in eval_num(n):
            if (r[0] == 24): print("%s = 24" % r[1])


if __name__ == "__main__":
    while True:
        user_input = raw_input("Type in four numbers, like '1 2 3 4' :")
        bad_input = False
        for x in user_input:
            if not x.isspace() and not x.isdigit():
                bad_input = True
                print("Plase only type in digits")
                break
        if bad_input: continue
        nums = [int(x) for x in user_input.strip().split()]
        if len(nums) != 4:
            print("Please type in exactly 4 numbers")
            continue
        search(nums)
