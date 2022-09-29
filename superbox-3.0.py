from math import *
from random import *
from pyray import *
from time import *

Fail = 0
Success = 1
Neighbor = 2

# cool idea: temperature raised by collision

# fuck you past me implement shit 

class Cell:
    def __init__(self, color):
        self.color = color
        self.vx = 0
        self.vy = 0
        self.gravity = 0
        self.mass = 1
        self.bounce = 1

class Sand(Cell):
    def __init__(self):
        self.color = Color(
            randint(210, 220),
            randint(160, 175),
            randint(60, 65),
            255
        )
        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.mass = 1
        self.bounce = 0.02

class Stone(Cell):
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
        self.gravity = -1
        self.mass = 500
        self.bounce = 0.005

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def attempt_swap(x, y, dx, dy):
    if x == dx and y == dy: return Fail
    if world[dy][dx] is not None: return Neighbor

    world[dy][dx] = world[y][x]
    world[y][x] = None
    return Success

width = 800
height = 600
world_width = 500
world_height = 500
scale = 5
color_mode = 0
wrap = True
wind = 0
max_wind = 0.008

gravity = 0.05

world = []
for y in range(world_height):
    world.append([])
    for x in range(world_width):
        world[y].append(None)
camera = Camera(0, 0)

init_window( width, height, "superbox 3.0")
set_target_fps(50)
render_texture = load_render_texture(world_width, world_height)
while not window_should_close():

    # ---- input ----

    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x
        camera.y += get_mouse_delta().y
    if get_mouse_wheel_move() > 0:
        if scale <= 100:
            scale += 1
            camera.x += (width/scale - width/(scale - 1)) / 2
            camera.y += (height/scale - height/(scale - 1)) / 2
    if get_mouse_wheel_move() < 0:
        if scale > 1:
            scale -= 1
            camera.x += (width/scale - width/(scale + 1)) / 2
            camera.y += (height/scale - height/(scale + 1)) / 2
    if is_key_pressed(KEY_TAB):
        color_mode += 1
        color_mode %= 2

    #   interaction
    if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
        x = int((get_mouse_x() - camera.x ) / scale) % (world_width - 1)
        y = int((- get_mouse_y() + camera.y ) / scale - 1) % (world_height - 1)
        if is_key_down(KEY_LEFT_SHIFT):
            world[y][x] = Sand()
            world[y][x].vy = -.9
        elif is_key_down(KEY_LEFT_CONTROL):
            world[y][x] = None
        else:
            world[y][x] = Stone()

    # ---- simulation ----
    total_energy = 0
    # wind speed
    wind += random()*0.00025-0.000125
    if wind > max_wind: wind = max_wind
    if wind < -max_wind: wind = -max_wind
    wind_side = -1
    if wind < 0: wind_side = 1

    for y in range(world_height):
        if world[y].count(None) == world_width: continue
        for x, cell in enumerate(world[y]):
            if cell is None: continue
            total_energy += cell.vx + cell.vy

            #gravity and wind
            if cell.vy > -.5:
                cell.vy -= gravity * cell.gravity 
            if world[y][(x+wind_side)%(world_width-1)] is None:
                cell.vx += wind / cell.mass

            # delta from velocity
            dx, dy = 0, 0
            if abs(cell.vx) > random(): dx = 1
            if cell.vx < 0: dx *= -1
            if abs(cell.vy) > random(): dy = 1
            if cell.vy < 0: dy *= -1
            dx += x
            dy += y

            if wrap:
                dx %= world_width
                dy %= world_height

            # swapping stuff and collision reactions
            state = attempt_swap(x, y, dx, dy)
            if state == Neighbor:
                ratio = cell.mass / (cell.mass + world[dy][dx].mass)
                fx = cell.vx * cell.mass
                fy = cell.vy * cell.mass
                cell.vx = - fx * ratio / cell.mass * cell.bounce
                cell.vy = - fy * ratio / cell.mass * cell.bounce
                world[dy][dx].vx  += fx * (1 - ratio) / world[dy][dx].mass
                world[dy][dx].vy += fy * (1 - ratio) / world[dy][dx].mass
                #print(ratio)

            #if cell.vx > 1: cell.vx = 1
            #if cell.vy > 1: cell.vy = 1

    #print(total_energy)
    # ---- rendering ----
    #       render the whole world in a texture
    begin_texture_mode(render_texture)
    clear_background(Color(0, 0, 0, 0))
    
    for y in range(world_height):
        if world[y].count(None) == world_width: continue
        for x in range(world_width):
            if world[y][x] is None: continue

            cell = world[y][x]

            if color_mode == 0: 
                c = cell.color
            if color_mode == 1: 
                v = int(min(sqrt(cell.vx**2 + cell.vy**2) * cell.mass ** 0.5 * 230, 230)) + 255 - 230   
                c = Color(v, v, v, 255)
            draw_pixel(x, y, c)
    end_texture_mode()
    
    begin_drawing()
    clear_background(WHITE)
    draw_rectangle_gradient_v(0, 0, width, height, Color(153, 218, 255, 255), Color(84, 193, 255, 255))

    #       tile the texture to fill the screen
    xs = world_width * scale
    ys = world_height * scale
    for y in range(-1, int(height/xs) + 1):
        for x in range(-1, int(width/ys) + 1):
            x1 = x * xs + camera.x % xs
            y1 = y * ys + camera.y % ys
            draw_texture_ex(render_texture.texture, Vector2(x1, y1), 0, scale, WHITE)

    # HUD
    draw_rectangle(int(width/2-1), int(height/2-7), 1, 14, WHITE)
    draw_rectangle(int(width/2-7), int(height/2-1), 14, 1, WHITE)
    draw_rectangle(int((wind/max_wind/2+0.5)*.95*width), 5, 2, 30, WHITE)
    
    draw_fps(3, 3)
    end_drawing()

close_window()
