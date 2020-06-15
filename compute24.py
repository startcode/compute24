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


class Op:
    def __init__(self, op, name, rank, communitive):
        self.op = op
        self.name = name
        self.rank = rank  # association priority
        self.communitive = communitive

    def run(self, a, b):
        return self.op(a, b)


# All the operations and their names.
AllOps = [
    Op(add, '+', 1, True),
    Op(sub, '-', 1, False),
    Op(mul, '*', 2, True),
    Op(div, '/', 2, False)
]


class OpTree:
    def __init__(self, op, val, left, right):
        self.op = op
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def init_from_op(self, op, left, right):
        return self(op, op.run(left.val, right.val), left, right)

    @classmethod
    def init_from_val(self, val):
        return self(None, val, None, None)

    def __str__(self):
        if self.left == None or self.right == None:
            return str(self.val)
        left_str = ""
        if self.left.op == None or self.left.op.rank > self.op.rank:
            left_str = str(self.left)
        else:
            left_str = "(%s)" % str(self.left)

        right_str = ""
        if self.right.op == None or self.right.op.rank > self.op.rank:
            right_str = str(self.right)
        else:
            right_str = "(%s)" % str(self.right)

        if self.op.communitive and left_str > right_str:
            left_str, right_str = right_str, left_str

        return "%s %s %s" % (left_str, self.op.name, right_str)


def CombineOpTree(left, right, op):
    if op.communitive:
        if left.val > right.val:
            left, right = right, left
    return OpTree.init_from_op(op, left, right)


# Evaluate all possible combinations of nums.
def eval_num(nums):
    results = []
    if len(nums) == 1:
        OpTree.init_from_val(3)
        results.append(OpTree.init_from_val(nums[0]))
        return results

    for i in range(1, len(nums)):
        # Divide the numbers into first half and second half
        first_half = eval_num(nums[0:i])
        second_half = eval_num(nums[i:])
        # Try each operation to combine first half and second half results.
        for op in AllOps:
            for t1 in first_half:
                for t2 in second_half:
                    if op.name == '/':
                        if t2.val == 0: continue
                        if t1.val % t2.val != 0: continue
                    results.append(CombineOpTree(t1, t2, op))
    return results


def search(nums):
    results = set([])
    for n in set(itertools.permutations(nums)):
        for r in eval_num(n):
            if (r.val == 24):
                results.add(str(r))

    for r in results:
        print("%s = 24" % r)


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
