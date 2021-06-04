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

list_quest = quest.items()
list_answer = answer.items()

# Role- "Master give a role"

# level = 0

lvl0 = "people"
lvl1 = "army"
lvl2 = "minor_vassal"
lvl3 = "major_vassal"
lvl4 = "marquis"
lvl5 = "king"

role = [lvl0, lvl1, lvl2, lvl3, lvl4, lvl5]

# A list with associate quest and answer,
# like this: "[[('1', 'Tutti sanno aprirlo, nessuno sa chiuderlo.'), ('1', 'uovo')],...]"
associate_quest_answer = []

for i, j in zip(list_quest, list_answer):
    temp = [i, j]
    associate_quest_answer.append(temp)

# print(associate_quest_answer)

# trap from master
trap = 0
key_quest = 0
value_quest = ""


# return a random quest
def get_quest():
    return quest.get(random.randint(1, 8))


# return a number between 1-3
def get_trap():
    trap = random.randint(1, 3)
    return trap


# check answer
def check_answer(msg, key):
    return msg == bytes(answer[key], "utf8")


# set quest
def assigns_quest():
    return random.choice(list(quest.items()))
