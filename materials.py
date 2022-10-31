from random import *
from pyray import *

BURN = 0
EXTINGWISH = 1
MELT = 2
WEAK_MELT= 3
DIRT = 4
MOISTER = 5

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
        self.temperature = 0
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

class Sky_stone:
    def __init__(self):
        v = randint(3, 10)
        if random() > .95: v = randint(10, 15)
        self.color = Color(
            v,
            v,
            v + randint(0, 15),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 100000000
        self.bounce = .5
        self.liquidity = 0
        self.moister = 0
        self.temperature = 0
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
        self.temperature = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [MOISTER]
        self.reaction_results = [['moisterize']]
        self.reaction_odds = [[0.3]]
    def moisterize(self):
        self.moister += 1
        if self.moister > 5:
            self.current_decay_chance = [1]
            self.decay_to = [Dirt]
    def reaction_feedback(self, i):
        pass

class Dirt:
    def __init__(self):
        self.color = Color(
            randint(100, 110),
            randint(50, 70),
            randint(25, 35),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = 1.5
        self.bounce = .15
        self.liquidity = .3
        self.moister = 0
        self.temperature = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [MOISTER]
        self.reaction_results = [['moisterize']]
        self.reaction_odds = [[0.3]]
    def moisterize(self):
        self.moister += 1
        if self.moister >= 5:
            self.reacts_as = [MOISTER]
        else:
            self.reacts_as = []
        if self.moister >= 10:
            self.reacts_to = []
    def reaction_feedback(self, i):
        if i == MOISTER:
            self.moister -= 3
        if self.moister < 10:
            self.reacts_to = [MOISTER]

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
        self.moister = 50
        self.temperature = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = [EXTINGWISH, MOISTER]
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
    def reaction_feedback(self, i):
        if i == MOISTER:
            self.moister -= 1
        if self.moister <= 0:
            self.current_decay_chance = [1]
            self.decay_to = [None]

class Smoke:
    def __init__(self):
        v = randint( 180, 240)
        self.color = Color(
            v,
            v,
            v - randint(10 , 20),
            200
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = -.6
        self.mass = .3
        self.bounce = .05
        self.liquidity = .9
        self.moister = 0
        self.temperature = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [.0035]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
    def reaction_feedback(self, i):
        pass

class Ash:
    def __init__(self):
        v = randint(25, 35)
        if random() > .9: v = randint(45, 55)
        self.color = Color(
            v,
            v,
            v + randint(0, 15),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = 0.3
        self.bounce = .3
        self.liquidity = .3
        self.moister = 0
        self.temperature = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [MOISTER]
        self.reaction_results = [[Water]]
        self.reaction_odds = [[0.02]]
    def reaction_feedback(self, i):
        pass

class Fire:
    def __init__(self):
        self.color = Color(
            randint(240, 255),
            randint(100, 110),
            randint(50, 60),
            255
        )
        if random() < .1:
            self.color = Color(
            randint(240, 255),
            randint(80, 100),
            randint(40, 50),
            255
        )
        if random() < .1:
            self.color = Color(
            randint(180, 200),
            randint(130, 160),
            randint(30, 40),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = -.1
        self.mass = .1
        self.bounce = .6
        self.liquidity = .6
        self.moister = 0
        self.temperature = 50
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0, 0]
        self.decay_chance_growth = [.004, .0005]
        self.decay_to = [Smoke, Ash]
        self.reacts_as = [BURN, WEAK_MELT]
        self.reacts_to = [EXTINGWISH]
        self.reaction_results = [[Smoke, None]]
        self.reaction_odds = [[.2, .1]]
    def reaction_feedback(self, i):
        pass

class Wood:
    def __init__(self):
        self.color = color_from_hsv(
            randint(10, 15),
            random()*.1+.35,
            random()*.05+.15
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 25
        self.bounce = .4
        self.liquidity = .1
        self.moister = 0
        self.temperature = 0
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [BURN]
        self.reaction_results = [[Fire, Ash]]
        self.reaction_odds = [[0.4, 0.1]]
    def reaction_feedback(self, i):
        pass