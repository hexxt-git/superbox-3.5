from math import *
from random import *
from pyray import *
from time import *
from materials import *

Fail = 0
Success = 1
Neighbor = 2

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.max_v = 2
        self.wind = 0
        self.max_wind = 0.004
        self.wind_variable = 0.00007
        self.gravity = 0.06
        world = []
        for y in range(self.height):
            world.append([])
            for x in range(self.width):
                    world[y].append(None)
        self.world = world

    def render_texture(self, render_texture, color_mode):
        begin_texture_mode(render_texture)
        clear_background(Color(0, 0, 0, 0))  
        for y in range(self.height):
            if self.world[y].count(None) == self.width: continue
            for x in range(self.width):
                if self.world[y][x] is None: continue
                cell = self.world[y][x]

                c = WHITE
                if color_mode == 0:  # light mode
                    c = cell.color
                if color_mode == 1:  # energy mode
                    v = int(min(sqrt((cell.vx**2 + cell.vy**2) * cell.mass) ** 0.5 * 230, 230)) + 255 - 230   
                    c = Color(v, v, v, 255)
                if color_mode == 2:  # velocity mode
                    r = int(abs(cell.vx) ** .4 / self.max_v * 220)
                    g = int(abs(cell.vy) ** .4 / self.max_v * 220)
                    b = min(r, g, 70)
                    c = Color(r+35, g+35, b+35, 255)

                draw_pixel(x, y, c)
        end_texture_mode()
        return render_texture
    def attempt_swap(self, x, y, dx, dy):
        if x == dx and y == dy: return Fail
        if self.world[dy][dx] is not None: return Neighbor

        self.world[dy][dx] = self.world[y][x]
        self.world[y][x] = None
        return Success

    def update(self):
        self.wind += random()*self.wind_variable - self.wind_variable/2
        if self.wind > self.max_wind: self.wind = self.max_wind
        if self.wind < -self.max_wind: self.wind = -self.max_wind
        self.wind *= 0.999
        wind_side = -1
        if self.wind < 0: wind_side = 1

        total_energy = 0
        for y in range(self.height):
            if self.world[y].count(None) == self.width: continue
            for x, cell in enumerate(self.world[y]):
                if cell is None: continue
                total_energy += (cell.vx + cell.vy) * cell.mass

                #gravity and wind
                if cell.vy > -.5:
                    cell.vy -= self.gravity * cell.gravity_effect 
                if self.world[y][(x+wind_side)%(self.width-1)] is None:
                    cell.vx += self.wind / cell.mass

                # delta from velocity
                dx, dy = 0, 0 # velocity in this simulation is just the odds of praticle moving, one step at a time.
                if abs(cell.vx) > random(): dx = 1
                if cell.vx < 0: dx *= -1
                if abs(cell.vy) > random(): dy = 1
                if cell.vy < 0: dy *= -1
                dx += x
                dy += y
                dx %= self.width
                dy %= self.height

                # swapping stuff and collision reactions
                state = self.attempt_swap(x, y, dx, dy)
                if state == Neighbor:
                    neighbor = self.world[dy][dx]
                    # the ratio enery is redestibuted upon
                    ratio = cell.mass / (cell.mass + neighbor.mass)
                    # force = velocity * mass
                    fx = cell.vx * cell.mass
                    fy = cell.vy * cell.mass
                    # particles in the real world do not colide perfectly aligned
                    # i simulate this by transfering a little x energy to y, and some y to x
                    # it also acts as a viscosity parameter since increasing it makes the particle more slippery
                    rx = random()*cell.liquidity-cell.liquidity/2 # TODO: fix the error in logic here
                    ry = random()*cell.liquidity-cell.liquidity/2
                    fx -= rx + ry
                    fy += rx - ry
                    # bounce is how much energy is wasted
                    cell.vx = - fx * ratio / cell.mass * cell.bounce * neighbor.bounce
                    cell.vy = - fy * ratio / cell.mass * cell.bounce * neighbor.bounce
                    neighbor.vx += fx * (1 - ratio) / neighbor.mass
                    neighbor.vy += fy * (1 - ratio) / neighbor.mass
                if cell.vx > self.max_v: cell.vx = self.max_v
                if cell.vy > self.max_v: cell.vy = self.max_v
        return total_energy

class CAM:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.scroll_speed = .1
        self.vz = 0

# TODO: fire. #simulated through temperature.
# TODO: explosives >:]
# TODO: magnetism :O

# DONE: smoke.
# DONE: better data visualizing color scheemes
# DONE: separate the sandbox and the engine
# DONE: FIX THE CAMERA

