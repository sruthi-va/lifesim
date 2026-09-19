import random


def yearly_health(c):
    if c.age > 40:
        c.health -= 1

    if c.age > 65:
        c.health -= 1

    c.health = max(0, min(100, c.health))


def death_chance(c):
    chance = max(0, c.age - 50) * 0.004

    if c.health < 40:
        chance += (40 - c.health) * 0.01

    if c.health <= 0:
        chance = 1

    return min(chance, 1)


def check_death(c):
    if random.random() < death_chance(c):
        c.alive = False

    return not c.alive