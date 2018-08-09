#!/usr/bin/env python

def rm_spaces(s):
    new_s = ''
    for c in s:
        if c == ' ':
            pass
        else:
            new_s += c

    return new_s

f = open("monster-battle.log")

monsters = set()

# first pass to get unique monsters.

monster_start_health = {}

lines = f.readlines()
for l in lines:
    l = l.strip()

    if l.startswith('starting health of'):
        health_fields = l[19:].split('=')
        health = int(health_fields[1])
        name = health_fields[0].strip()
        monster_start_health[name] = health
        print "%s = %d" % (name, health)

    fields = l.split('|')
    if len(fields) >= 3:
        if fields[1].strip() == 'a':
            monster = fields[2].split('{')[0]
            monsters.add(monster)

# second pass to count attacks.

monster_attack_counts = dict()
for m in monsters:
    monster_attack_counts[m] = 0

for l in lines:
    fields = l.split('|')
    if len(fields) >= 3:
        if fields[1].strip() == 'a':
            monster = fields[2].split('{')[0]
            monster_attack_counts[monster] += 1

f.close()

# dump file compatible for gnuplot.

plotfile = open("monster-attacks.dat", "w")
i = 0
for monster, count in monster_attack_counts.iteritems():
    i += 1
    print >>plotfile, "%d %s %s" % (i, count, rm_spaces(monster))

plotfile.close()


