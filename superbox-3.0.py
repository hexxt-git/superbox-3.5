from math import *
from random import *
from pyray import *
from time import *

Fail = 0
Success = 1
Neighbor = 2

class Plastic:
    def __init__(self):
        self.color = Color(randint(0, 255), randint(0, 255), randint(0, 255), randint(220, 255))
        self.vx = 0
        self.vy = 0
        self.gravity = 1
        self.mass = .9
        self.absorption = 0
        self.viscosity = 0.5

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
        self.gravity = 1
        self.mass = 1
        self.absorption = 0.2
        self.viscosity = 0.3

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
        self.gravity = 0
        self.mass = 500
        self.absorption = 0.3
        self.viscosity = 0.6

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
        self.gravity = 1
        self.mass = 0.5
        self.absorption = 0.01
        self.viscosity = 0.8

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
        self.gravity = -1
        self.mass = 0.4
        self.absorption = 0.001
        self.viscosity = .8

cell_names = ['plastic', 'stone', 'sand', 'water', 'smoke']
cell_classes = [Plastic, Stone, Sand, Water, Smoke]
selected = 0

class Camera:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def attempt_swap(x, y, dx, dy):
    if x == dx and y == dy: return Fail
    if not wrap_y and dy >= world_height - 1: return Fail
    if not wrap_x and dx >= world_width - 1: return Fail
    if world[dy][dx] is not None: return Neighbor

    world[dy][dx] = world[y][x]
    world[y][x] = None
    return Success

width = 800
height = 600
world_width = 200
world_height = 200
color_mode = 0
wrap_y = True # <--------------- fix thisss
wrap_x = True
wind = 0
max_wind = 0.005
wind_variable = 0.0001

gravity = 0.05


world = []
for y in range(world_height):
    world.append([])
    for x in range(world_width):
        if (x*.7 - 60)**2 + (y*1.5 - 180)**2 + sin(x*0.7)*80 <= 20**2: # i spent way too much time on this bs
            world[y].append(Stone())
        else:
            world[y].append(None)
camera = Camera(0, 0, 5)

init_window( width, height, "superbox 3.0")
set_target_fps(50)
render_texture = load_render_texture(world_width, world_height)
#hide_cursor()
while not window_should_close():

    # ---- input ----
    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x
        camera.y += get_mouse_delta().y
    if get_mouse_wheel_move() > 0:
        if camera.z <= 50:
            camera.z += 1
    if get_mouse_wheel_move() < 0:
        if camera.z > 1:
            camera.z -= 1
    if is_key_pressed(KEY_TAB):
        color_mode += 1
        color_mode %= 2
    if is_key_pressed(KEY_SPACE):
        selected += 1
        selected %= len(cell_names)

    #   interaction
    if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
        x = int((get_mouse_x() - camera.x ) / camera.z)
        y = int((- get_mouse_y() + camera.y ) / camera.z)
        if wrap_y:
            y %= (world_height - 1)
        if wrap_x:
            x %= (world_width - 1)
        if x < world_width and x >= 0 and y < world_height and y >= 0:
            if is_key_down(KEY_LEFT_CONTROL):
                world[y][x] = None
            else:
                world[y][x] = cell_classes[selected]()

    # ---- simulation ----
    total_energy = 0
    # wind speed
    wind += random()*wind_variable-wind_variable/2
    if wind > max_wind: wind = max_wind
    if wind < -max_wind: wind = -max_wind
    wind_side = -1
    if wind < 0: wind_side = 1
    wind *= 0.999

    for y in range(world_height):
        if world[y].count(None) == world_width: continue
        for x, cell in enumerate(world[y]):
            if cell is None: continue
            total_energy += (cell.vx + cell.vy) * cell.mass

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
            dx %= world_width
            dy %= world_height

            # swapping stuff and collision reactions
            state = attempt_swap(x, y, dx, dy)
            if state == Neighbor:
                # the ratio enery is redestibuted upon
                ratio = cell.mass / (cell.mass + world[dy][dx].mass)
                # force = velocity * mass
                fx = cell.vx * cell.mass
                fy = cell.vy * cell.mass
                # particles in the real world do not colide perfectly aligned
                # i simulate this by transfering a little x energy to y, and some y to x
                # it also acts as a viscosity parameter since increasing it makes the particle more slippery
                rx = random()*cell.viscosity-cell.viscosity/2 # TODO: fix the error in logic here
                ry = random()*cell.viscosity-cell.viscosity/2
                fx += rx
                fy -= rx
                fx += ry
                fy -= ry
                # absorption is how much energy is wasted
                cell.vx = - fx * ratio / cell.mass * cell.absorption * world[dy][dx].absorption
                cell.vy = - fy * ratio / cell.mass * cell.absorption * world[dy][dx].absorption
                world[dy][dx].vx += fx * (1 - ratio) / world[dy][dx].mass
                world[dy][dx].vy += fy * (1 - ratio) / world[dy][dx].mass
            
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
                v = int(min(sqrt(cell.vx**2 + cell.vy**2) ** 0.5 * 230, 230)) + 255 - 230   
                c = Color(v, v, v, 255)

            draw_pixel(x, y, c)
    end_texture_mode()
    
    begin_drawing()
    clear_background(WHITE)
    draw_rectangle_gradient_v(0, 0, width, height, Color(153, 218, 255, 255), Color(84, 193, 255, 255))

    #       tile the texture to fill the screen
    xs = world_width * camera.z # this solution is still flawed.
    ys = world_height * camera.z
    for y in range(-1, (int(height/xs) + 1) if wrap_y else 0):
        for x in range(-1, (int(width/ys) + 1) if wrap_x else 0):
            x1 = x * xs + camera.x % xs if wrap_x else camera.x
            y1 = y * ys + camera.y % ys if wrap_y else camera.y
            draw_texture_ex(render_texture.texture, Vector2(x1, y1), 0, camera.z, WHITE)
    # HUD
    draw_rectangle(int((wind/max_wind/2+0.5)*.95*width), 5, 2, 20, WHITE)
    draw_rectangle(int(width/2-1), 3, 2, 4, WHITE)


    draw_fps(5, 5)
    draw_text(cell_names[selected] + '  // press space to change material', 5, 25, 23, DARKGREEN)
    end_drawing()

close_window()

    # TODO: better data visualizing color scheemes  
    # TODO: separate the sandbox and the engine
    # like Sand Stone and water constructors and inputs are parts of the sandbox, but rendering and simulating is engine work.
    # meaning i would have to make many things into functions
    # TODO: fire. simulated through temperature.
    # TODO: smoke.
    # TODO: explosives >:]

