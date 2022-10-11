from random import *
from pyray import *

class Stone:
    def __init__(self):
        v = randint(75, 90)
        self.color = Color(
            v,
            v,
            v + randint(0, 10),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 50
        self.bounce = .3
        self.liquidity = .1
        self.moister = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
    def reaction_feedback(self, i):
        pass

class Sand:
    def __init__(self):
        self.color = Color(
            200,
            130,
            90,
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = 2
        self.bounce = .3
        self.liquidity = .2
        self.moister = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
    def reaction_feedback(self, i):
        pass
