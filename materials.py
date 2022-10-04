from random import *
from pyray import *

# reactions
BURN = 0
EXTINGWISH = 1
MELT = 2
WEAK_MELT= 3
DIRT = 4
MOISTER = 5



class Plastic:
    def __init__(self):
        self.color = Color(
            randint(30, 220),
            randint(30, 220),
            randint(30, 220),
            randint(230, 255)
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = .9
        self.bounce = .8
        self.liquidity = .5
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
            randint(210, 220),
            randint(160, 175),
            randint(60, 65),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = 1
        self.bounce = .2
        self.liquidity = .1
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [DIRT]
        self.reaction_results = [[Dirt]]
        self.reaction_odds = [[0.1]]
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
        self.liquidity = .2
        self.moister = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [MOISTER]
        self.reaction_results = [['moisterize']]
        self.reaction_odds = [[0.5]]
    def moisterize(self):
        self.moister += 0.2
        self.update()
    def reaction_feedback(self, i):
        self.moister -= 1
        self.update()
    def update(self):
        if self.moister > 1.5:
            self.reacts_as = [DIRT, MOISTER]
        else:
            self.reacts_as = []
        if self.moister < 5:
            self.reacts_to = [MOISTER]
            self.reaction_results = [['moisterize']]
            self.reaction_odds = [[0.5]]
        else:
            self.reacts_to = []
            self.reaction_results = []
            self.reaction_odds = []

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
        self.mass = 100
        self.bounce = .3
        self.liquidity = .1
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [MELT, WEAK_MELT]
        self.reaction_results = [[Lava],[Lava]]
        self.reaction_odds = [[.1], [0.003]]
    def reaction_feedback(self, i):
        pass

class Sky_Stone:
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
            randint(100, 110),
            randint(190, 200),
            200
        )
        self.vx = 0
        self.vy = 0
        self.gravity_effect = 1
        self.mass = .5
        self.bounce = .8
        self.liquidity = 1
        self.moister = 5
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = [EXTINGWISH, DIRT, MOISTER]
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
    def reaction_feedback(self, reaction):
        if reaction == DIRT:
            self.moister -= 1
            if self.moister <= 0: self.current_decay_chance = [1]

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
        self.current_decay_chance = [0, 0]
        self.decay_chance_growth = [.004, .0005]
        self.decay_to = [Smoke, Ash]
        self.reacts_as = [BURN, WEAK_MELT]
        self.reacts_to = [EXTINGWISH]
        self.reaction_results = [[Smoke, None]]
        self.reaction_odds = [[.2, .05]]
    def reaction_feedback(self, i):
        pass

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
        self.current_decay_chance = [0]
        self.decay_chance_growth = [.0035]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
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
        self.mass = 30
        self.bounce = .4
        self.liquidity = 0
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = [BURN]
        self.reaction_results = [[Fire, Ash]]
        self.reaction_odds = [[.5, .3]]
    def reaction_feedback(self, i):
        pass

class Ash   :
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
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0]   
        self.decay_to = [None]
        self.reacts_as = []
        self.reacts_to = []
        self.reaction_results = []
        self.reaction_odds = []
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
        self.gravity_effect = 1
        self.mass = .7
        self.bounce = .7
        self.liquidity = .9
        self.current_decay_chance = [0]
        self.decay_chance_growth = [0.006]
        self.decay_to = [Stone]
        self.reacts_as = [BURN, MELT]
        self.reacts_to = [EXTINGWISH]
        self.reaction_results = [[Stone, Smoke]]
        self.reaction_odds = [[0.6, 0.05]]
    def reaction_feedback(self, i):
        pass