#!/usr/bin/env python3

import socket
import math
import random
import threading
import signal
import sys

VALUE = int(math.pow(10, 6))
GOAL = 333

ascci_template = r"""/$$$$$$            /$$$$$$  /$$$          /$$   /$$                     /$$                     /$$
"""

banner = r"""
Can you guess the random number between 1 and 10 a thousand times? If you do I'll give you the flag.
Surely you would need infinite luck, or is it just a one in a million chance?

Good luck!

(make sure to place spaces between the values)
"""


def __build_rule_from_template(seed, builder):
    image = ""
    image += str(seed)
    for c in ascci_template:
        if c == "$":
            value = random.randint(0, len(builder) - 1)
            image += builder[value]
        else:
            image += c

    return image


def __print_rules(seed):
    characters = "abcdefghi"
    ascii_image = __build_rule_from_template(seed, characters)
    print(ascii_image)


def value_guesser(seed):
    print(seed)
    random.seed(seed)
    __print_rules(seed)


for seed in range(1, VALUE + 1):
    value_guesser(seed)
