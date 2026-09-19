# game/engine.py

from game.systems.health import yearly_health, check_death


class Engine:
    def __init__(self, character):
        self.c = character

    def age_up(self):
        self.c.age += 1
        yearly_health(self.c)
        check_death(self.c)