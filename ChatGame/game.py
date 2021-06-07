#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

# A dict with quest
quest = {
    1: 'Tutti sanno aprirlo, nessuno sa chiuderlo.',
    2: "E' tuo ma lo usano spesso gli altri senza chiederti il permesso.",
    3: 'Senza parlare fa tremare tutti.',
    4: 'Quando arrivano tutti se ne vanno.',
    5: 'Più sono, meno pesano.',
    6: 'So scrivere, ma non so leggere.',
    7: 'Mi trovi in un posto desolato, e se parli me ne sono già andato'
}

# A dict with answer
answer = {
    1: 'uovo',
    2: 'nome',
    3: 'freddo',
    4: 'vacanze',
    5: 'buchi',
    6: 'mano',
    7: 'silenzio'
}

role = ["people", "army", "minor_vassal", "major_vassal", "marquis", "king"]

""" return a random quest """


def get_quest():
    return quest.get(random.randint(1, 8))


""" return a key with value get between 1-3"""


def get_trap():
    trap = random.randint(1, 3)
    return trap


""" check msg gets in input and compere msg with answer to check """


def check_answer(msg, key):
    return msg == bytes(answer[key], "utf8")


""" return a random quest"""


def assigns_quest():
    return random.choice(list(quest.items()))


""" return new role """


def rank_role(increase):
    return role[increase]


""" check win"""


def win(actual_role):
    return actual_role == role[5]
