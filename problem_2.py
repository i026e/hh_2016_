#! /usr/bin/env python3

# -*- coding: utf-8 -*-

"""
Created on Thu Sep 22 2016

@author: pavel
"""

import sys

def consequtive(str_a, str_b, part_a = False, part_b = False):
    # partial => a или b могут быть частью числа

    a = int(str_a)
    b = int(str_b)

    #print(a, b, part_a, part_b)

    if not (part_a or part_b):
        return a + 1 == b


    len_a = len(str_a)
    len_b = len(str_b)


    if part_a and not part_b:
        c = b - 1
        return str_a == str(c)[-len_a:]

    if part_b and not part_a:
        c = a + 1
        return str_b == str(c)[:len_b]

    if part_a and part_b:
        # should not be the case
        # see overlap
        return True

def overlap(a, b):
    # zabc + xyz => xyzabc + 1
    c = str(int(a) + 1)
    for i in range(len(b)):
        substring = b[i:]

        if c[0:len(substring)] == substring:
            return int(b[:i] + c)
    return int(b + c)

def elements(line):
    length = len(line)

    def recursive(start, end, numbers = None):
        number = line[start:end]

        if end >= length: # последний символ - возвращаем ответ
            if numbers is None:
                return [int(number)]
            else:
                if (len(numbers) == 1): # 2 числа в итоге
                    return [int(numbers[0]), overlap(numbers[0], number)]

                elif consequtive(numbers[-1], number, \
                                part_a = False, \
                                part_b = True):
                    return [int(i) for i in numbers] + [int(number)]
                else:
                    return None


        if numbers is not None:
            if not consequtive(numbers[-1], number, \
                               part_a = (len(numbers) == 1)): # без вариантов
                return recursive(start, end + 1, numbers)


        #имеет смысл разделять строку как можно чаще,
        #            чтобы получить наименьший ответ ?

        # сначала cчитаем number за отдельное число

        tmp = [] if numbers is None else numbers

        answer1 = recursive(end, end + 1, tmp + [number])
        answer2 = recursive(start, end + 1, numbers)

        #print(answer1, answer2)

        if answer1 is None :
            return answer2

        if answer2 is None:
            return answer1

        if max(answer1) < max(answer2):
            return answer1

        # потом за часть ,большего числа
        return answer2

    values = recursive(0, 1, None)
    #print(values)



    return values


def index_of(number):
    order = len(str(number))

    #num_numbers = 0
    length = 0

    for i in range(1, order):
        num_numbers = 10**i - 10**(i-1)
        #print(num_numbers)
        length += num_numbers * i

    length += (number - 10**(order - 1)) * order
    #print(length)
    return length + 1


def find_index(values):
    max_val = max(values)
    index = values.index(max_val)

    min_val = max_val - index
    shift = len(str(min_val)) - len(str(values[0]))

    index = index_of(min_val) + shift
    return index

def position_in_digit_seq(line):
    if len(line) <= 0:
        return -1
    if not line.isdigit():
        return -1

    values = elements(line)
    #print(values)
    ind = find_index(values)

    return ind


def tests():
    s999 = ''.join(str(i) for i in range(1, 999+1))

    def correct_answer(val):
        return s999.find(str(val)) + 1


    assert index_of(6) == correct_answer(6)
    assert index_of(10) == correct_answer(10)
    assert index_of(11) == correct_answer(11)

    assert index_of(578) == correct_answer(578)
    assert index_of(129) == correct_answer(129)

    assert index_of(55) == correct_answer(55)

    assert index_of(123) != correct_answer(123)
    assert index_of(5152) != correct_answer(5152)


    cases = {"6789" : 6,
             "111"  : 12,
             "556" : None,
             "34445464748495051525" : None,
             "99100" : None,
             "661" : None,

             }

    for line, answer in cases.items():
        if answer is not None:
            assert answer == correct_answer(line)


        ind = position_in_digit_seq(line.strip())

        print(line, ind, correct_answer(line))
        assert ind == correct_answer(line)


    assert position_in_digit_seq("123451234612347123481234912350") \
        == position_in_digit_seq("1234512346123471234812349123501235112352123531235412355")

    assert position_in_digit_seq("123451234612347123481234912350") \
        != position_in_digit_seq("1234512346123471234812349123501235112352123531235412356")

def main(*args):
    for line in sys.stdin:
        print(position_in_digit_seq(line.strip()))

if __name__ == "__main__":
    main(*sys.argv)
    tests()
