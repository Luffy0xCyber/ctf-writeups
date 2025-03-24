import math
import random
import threading
import signal
import sys

seed = 961818


#!/usr/bin/env python3


VALUE = int(math.pow(10, 6))
GOAL = 333

ascci_template = r"""
/$$$$$$            /$$$$$$  /$$$          /$$   /$$                     /$$                     /$$
|_  $$_/           /$$__  $$|__/          |__/  | $$                    | $$                    | $$
  | $$   /$$$$$$$ | $$  \__/ /$$ /$$$$$$$  /$$ /$$$$$$    /$$$$$$       | $$ /$$   /$$  /$$$$$$$| $$   /$$
  | $$  | $$__  $$| $$$$    | $$| $$__  $$| $$|_  $$_/   /$$__  $$      | $$| $$  | $$ /$$_____/| $$  /$$/
  | $$  | $$  \ $$| $$_/    | $$| $$  \ $$| $$  | $$    | $$$$$$$$      | $$| $$  | $$| $$      | $$$$$$/
  | $$  | $$  | $$| $$      | $$| $$  | $$| $$  | $$ /$$| $$_____/      | $$| $$  | $$| $$      | $$_  $$
 /$$$$$$| $$  | $$| $$      | $$| $$  | $$| $$  |  $$$$/|  $$$$$$$      | $$|  $$$$$$/|  $$$$$$$| $$ \  $$
|______/|__/  |__/|__/      |__/|__/  |__/|__/   \___/   \_______/      |__/ \______/  \_______/|__/  \__/
"""

banner = r"""
Can you guess the random number between 1 and 10 a thousand times? If you do I'll give you the flag.
Surely you would need infinite luck, or is it just a one in a million chance?

Good luck!

(make sure to place spaces between the values)
"""


def __build_rule_from_template(builder):
    image = ""
    for c in ascci_template:
        if c == "$":
            value = random.randint(0, len(builder) - 1)
            image += builder[value]
        else:
            image += c

    return image


def __print_rules():
    characters = "abcdefghi"
    ascii_image = __build_rule_from_template(characters)
    print(ascii_image)


def __check_value():
    answer = ""
    for v in range(GOAL):
        value = random.randint(1, 10)
        answer += str(value)
        answer += " "
    return answer


def value_guesser():
    random.seed(seed)
    __print_rules()

    answer = __check_value()
    print(answer)


value_guesser()
