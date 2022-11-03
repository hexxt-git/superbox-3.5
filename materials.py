from random import *
from pyray import *

MOISTER = 0

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
        self.temperature_exchange = 1
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = None
        self.melt_to = None
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
        self.temperature_exchange = 0
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = 20
        self.melt_to = Plastic
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
        self.temperature_exchange = 0
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = None
        self.melt_to = None
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
        self.gravity_effect = .6
        self.mass = .8
        self.bounce = .5
        self.liquidity = 1
        self.moister = 50
        self.temperature = 0
        self.temperature_exchange = .4
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = [MOISTER]
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
        self.freeze_at = -20
        self.freeze_to = Ice
        self.melt_at = 15
        self.melt_to = Steam
    def reaction_feedback(self, i):
        if i == MOISTER:
            self.moister -= 1
        if self.moister <= 0:
            self.current_decay_chance = [1]
            self.decay_to = [None]

class Steam:
    def __init__(self):
        v = randint( 200, 250)
        self.color = Color(
            v,
            v,
            v - randint(5 , 15),
            200
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = -.6
        self.mass = .3
        self.bounce = .05
        self.liquidity = .9
        self.moister = 0
        self.temperature = 20
        self.temperature_exchange = .6
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
        self.freeze_at = 5
        self.freeze_to = Water
        self.melt_at = None
        self.melt_to = None
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
        self.temperature = 5
        self.temperature_exchange = 0
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = None
        self.melt_to = None
    def reaction_feedback(self, i):
        pass

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
        self.temperature_exchange = 0.5
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = 60
        self.melt_to = Lava
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
        self.bounce = .8
        self.liquidity = .8
        self.moister = 0
        self.temperature = 70
        self.temperature_exchange = .9
        self.explosion_chance = 0
        self.explosive_power = 0
        self.explosion_radius = 0
        self.current_decay_chance = []
        self.decay_chance_growth = []
        self.decay_to = []
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
        self.freeze_at = 15
        self.freeze_to = Ash
        self.melt_at = None
        self.melt_to = None
    def reaction_feedback(self, i):
        pass

class Lava:
    def __init__(self):
        self.color = Color(
            randint(230, 240),
            randint(80, 90),
            randint(30, 40),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0.6
        self.mass = 3
        self.bounce = .7
        self.liquidity = .9
        self.moister = 0
        self.temperature = 120
        self.temperature_exchange = .9
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
        self.freeze_at = 50
        self.freeze_to = Stone
        self.melt_at = None
        self.melt_to = None
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
        self.temperature_exchange = .9
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = 20
        self.melt_to = Fire
    def reaction_feedback(self, i):
        pass

class Tnt:
    def __init__(self):
        self.color = Color(
            randint(240, 250),
            randint(40, 50),
            randint(30, 40),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 40
        self.bounce = 0
        self.liquidity = 0
        self.moister = 0
        self.temperature = 0
        self.temperature_exchange = 0
        self.explosion_chance = 1
        self.explosive_power = 100
        self.explosion_radius = 8
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = None
        self.melt_to = None
    def reaction_feedback(self, i):
        pass

class Plastic:
    def __init__(self):
        self.color = Color(
            randint(50, 230),
            randint(50, 230),
            randint(50, 230),
            randint(230, 250)
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = .8
        self.mass = 3
        self.bounce = .9
        self.liquidity = .8
        self.moister = 0
        self.temperature = 0
        self.temperature_exchange = 0.8
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = None
        self.melt_to = None
    def reaction_feedback(self, i):
        pass

class Ice:
    def __init__(self):
        self.color = Color(
            randint(95, 105),
            randint(170, 180),
            randint(230, 250),
            randint(200, 220)
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 20
        self.bounce = .9
        self.liquidity = .8
        self.moister = 20
        self.temperature = -30
        self.temperature_exchange = 0.5
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = 0
        self.melt_to = Water
    def reaction_feedback(self, i):
        pass

class Super_Ice:
    def __init__(self):
        self.color = Color(
            randint(150, 180),
            randint(200, 230),
            randint(230, 250),
            randint(200, 220)
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 0
        self.mass = 20
        self.bounce = .9
        self.liquidity = .8
        self.moister = 30
        self.temperature = -100
        self.temperature_exchange = 1
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
        self.freeze_at = None
        self.freeze_to = None
        self.melt_at = -30
        self.melt_to = Ice
    def reaction_feedback(self, i):
        pass