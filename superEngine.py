from math import *
from random import *
from pyray import *
import inspect
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
        self.max_wind = 0.005
        self.wind_variable = 0.0002
        self.wind_normalizer = .99
        self.gravity = 0.06
        self.world = [[None for x in range(self.width)] for y in range(self.height)]

    def render_texture(self, render_texture, color_mode):
        begin_texture_mode(render_texture)
        clear_background(Color(0, 0, 0, 0))  
        for y in range(self.height):
            if self.world[y].count(None) == self.width: continue
            for x in range(self.width):
                if self.world[y][x] is None: continue
                pixel = self.world[y][x]

                c = WHITE
                if color_mode == 0:  # light mode
                    c = pixel.color
                if color_mode == 1:  # energy mode
                    h = int(min(sqrt(pixel.vx**2 + pixel.vy**2) * pixel.mass * 150, 66))  
                    c = color_from_hsv(h, 95, 85)
                if color_mode == 2:  # velocity mode
                    r = min(int(abs(pixel.vx) ** .4 / self.max_v * 250), 250)
                    g = min(int(abs(pixel.vy) ** .4 / self.max_v * 250), 250)
                    b = min(r, g, 70)
                    c = Color(r, g, b, 255)
                if color_mode == 3: # moister mode
                    if hasattr(pixel, 'moister'):
                        m = int(max(min(pixel.moister / 5 * 255, 255), 0))
                        c = Color(m, m, m, 255)
                    else: c = BLACK

                draw_pixel(x, y, c)
        end_texture_mode()
        return render_texture
    
    def render(self, render_texture, camera, width, height):
        x_scale = int(self.width * camera.z)
        y_scale = int(self.height * camera.z)
        for y in range(-2, int(height/y_scale+1)):
            for x in range(-2, int(width/x_scale+1)):
                draw_texture_ex(render_texture.texture,
                Vector2(
                    x*x_scale + camera.x%x_scale,
                    y*y_scale + camera.y%y_scale
                ), 0, camera.z, WHITE)
    
    def attempt_swap(self, x, y, dx, dy):
        if x == dx and y == dy: return Fail
        if self.world[dy][dx] is not None: return Neighbor

        self.world[dy][dx] = self.world[y][x]
        self.world[y][x] = None
        return Success

    def update(self):
        #   world updates 🌍
        
        self.wind += (random()-.5)*self.wind_variable
        if self.wind > self.max_wind: self.wind = self.max_wind
        if self.wind < -self.max_wind: self.wind = -self.max_wind
        self.wind *= self.wind_normalizer
        wind_side = -1
        if self.wind < 0: wind_side = 1

        total_energy = 0
        for y in range(self.height):
            if self.world[y].count(None) == self.width: continue
            for x, pixel in enumerate(self.world[y]):
                if pixel is None: continue

                if abs(pixel.vy) < .5:
                    pixel.vy -= self.gravity * pixel.gravity_effect 
                if self.world[y][(x+wind_side)%(self.width-1)] is None:
                    pixel.vx += self.wind / pixel.mass

                #   physics ⛓️
                
                dx, dy = 0, 0 # velocity in this simulation is just the odds of praticle moving, one step at a time.
                if abs(pixel.vx) > random(): dx = 1
                if pixel.vx < 0: dx *= -1
                if abs(pixel.vy) > random(): dy = 1
                if pixel.vy < 0: dy *= -1
                dx += x
                dy += y
                dx %= self.width
                dy %= self.height

                # swapping stuff and collision reactions
                state = self.attempt_swap(x, y, dx, dy)
                if state == Neighbor:
                    neighbor = self.world[dy][dx]
                    # the ratio enery is redestibuted upon
                    ratio = neighbor.mass / (pixel.mass + neighbor.mass)
                    # force = velocity * mass
                    force_x = pixel.vx * pixel.mass
                    force_y = pixel.vy * pixel.mass
                    # particles in the real world do not colide perfectly aligned
                    # i simulate this by transfering a little x energy to y, and some y to x
                    # it also acts as a viscosity parameter since increasing it makes the particle more slippery
                    lost_x = force_x * (random()*2-1)*pixel.liquidity
                    lost_y = force_y * (random()*2-1)*pixel.liquidity
                    force_x -= lost_x + lost_y
                    force_y -= lost_y + lost_x

                    # bounce is how much energy is wasted
                    pixel.vx = - force_x * ratio / pixel.mass * pixel.bounce * neighbor.bounce
                    pixel.vy = - force_y * ratio / pixel.mass * pixel.bounce * neighbor.bounce
                    neighbor.vx += force_x * (1 - ratio) / neighbor.mass
                    neighbor.vy += force_y * (1 - ratio) / neighbor.mass
                    if neighbor.vx > self.max_v: neighbor.vx = self.max_v
                    if neighbor.vy > self.max_v: neighbor.vy = self.max_v
                if pixel.vx > self.max_v: pixel.vx = self.max_v
                if pixel.vy > self.max_v: pixel.vy = self.max_v
                total_energy += (pixel.vx + pixel.vy) * pixel.mass
            
                #   chimestry 🧪
                for i in range(len(pixel.current_decay_chance)):
                    pixel.current_decay_chance[i] += pixel.decay_chance_growth[i]

                for i in range(len(pixel.current_decay_chance)):
                    if pixel.current_decay_chance[i] > random() * 100:
                        if pixel.decay_to[i] is not None:
                            self.world[y][x] = pixel.decay_to[i]()
                            self.world[y][x].vx = (pixel.vx * pixel.mass) / self.world[y][x].mass
                            self.world[y][x].vy = (pixel.vy * pixel.mass) / self.world[y][x].mass
                        else: self.world[y][x] = None

                if state == Neighbor:
                    neighbor = self.world[dy][dx]
                    for reaction in pixel.reacts_as:
                        if reaction in neighbor.reacts_to:
                            reaction_index = neighbor.reacts_to.index(reaction)
                            for i in range(len(neighbor.reaction_results[reaction_index])):
                                if neighbor.reaction_odds[reaction_index][i] > random():
                                    pixel.reaction_feedback(reaction)
                                    if neighbor.reaction_results[reaction_index][i] is None:
                                        self.world[dy][dx] = None
                                    elif inspect.isclass(neighbor.reaction_results[reaction_index][i]): 
                                        self.world[dy][dx] = neighbor.reaction_results[reaction_index][i]()
                                        self.world[dy][dx].vx = (neighbor.vx * neighbor.mass) / self.world[dy][dx].mass
                                        self.world[dy][dx].vy = (neighbor.vy * neighbor.mass) / self.world[dy][dx].mass
                                    else:
                                        getattr(neighbor, neighbor.reaction_results[reaction_index][i])()
        return total_energy

class CAM:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.scroll_speed = .08
        self.vz = 0

# TODO: make an attempt to optimize the code
# TODO: explosives >:]
# TODO: magnetism :O
# TODO: improve the camera
# TODO: procedually generated islands

# DONE: smoke.
# DONE: better data visualizing color scheemes
# DONE: separate the sandbox and the engine
# DONE: FIX THE CAMERA
# DONE: better placing of pixels with the mouse
# DONE: fire.
# DONE: chimestry
# DONE: advanced chimestry
