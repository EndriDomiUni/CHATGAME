#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random

# A dict with quest
quest = {
    # uovo
    '1': 'Tutti sanno aprirlo, nessuno sa chiuderlo.',
    # nome
    '2': "E' tuo ma lo usano spesso gli altri senza chiederti il permesso.",
    # freddo
    '3': 'Senza parlare fa tremare tutti.',
    # vacanze
    '4': 'Quando arrivano tutti se ne vanno.',
    # buchi
    '5': 'Più sono, meno pesano.',
    # mano
    '6': 'So scrivere, ma non so leggere.',
    # silenzio
    '7': 'Mi trovi in un posto desolato, e se parli me ne sono già andato'
}

# A dict with answer
answer = {
    '1': 'uovo',
    '2': 'nome',
    '3': 'freddo',
    '4': 'vacanze',
    '5': 'buchi',
    '6': 'mano',
    '7': 'silenzio'
}

# Role- "Master give a role"
level = 0
people = 0
army = 1
minor_vassal = 2
major_vassal = 3
marquis = 4
king = 5

role = [people, army, minor_vassal, major_vassal, marquis, king]

# A list with associate quest and answer,
# like this: "[[('1', 'Tutti sanno aprirlo, nessuno sa chiuderlo.'), ('1', 'uovo')],...]"
associate_quest_answer = []

for i, j in zip(quest.items(), answer.items()):
    temp = [i, j]
    associate_quest_answer.append(temp)

print(associate_quest_answer)

# trap from master
trap = -1


# return a quest from input
def get_quest(choise):
    return quest.get(quest, choise)


# return a new role if the player wins
def rank_up(level):
    level += 1
    for i in role:
        if level == i:
            return i
    return level - 1
