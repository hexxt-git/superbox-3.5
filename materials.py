from random import *
from pyray import *

class Stone:
    def __init__(self):
        v = randint(75, 95)
        self.color = Color(
            v,
            v,
            v + randint(5, 15),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 100
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
            randint(185, 200),
            randint(130, 140),
            randint(60, 70),
            255
        )
        if random() < .06:
            self.color = Color(
                randint(180, 190),
                randint(120, 130),
                randint(60, 70),
                255
            )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = 2
        self.bounce = .4
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

class Water:
    def __init__(self):
        self.color = Color(
            randint(65, 70),
            randint(145, 150),
            randint(205, 210),
            randint(230, 250)
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = .8
        self.bounce = .5
        self.liquidity = 1
        self.moister = 5
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

class BLACK:
    def __init__(self):
        self.color = Color(0,0,0,255)
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = .3
        self.bounce = .6
        self.liquidity = 1.5
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