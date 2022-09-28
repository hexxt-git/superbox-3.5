from math import *
from random import *
from pyray import *
from time import *

Fail = 0
Border = 0
Success = 1
Neighbor = 2

# cool idea: temperature raised by collision

class Cell :
    def __init__(self, color):
        self.color = color
        self.vx = random() - .5
        self.vy = random() - .5
class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def attempt_swap(world, x, y, dx, dy):
    if dx == 0 and dy == 0: return Fail
    if y + dy == world_height: return Border
    if y + dy == -1: return Border
    if x + dx == world_width: return Border
    if x + dx == -1: return Border
    if world[y+dy][x+dx] is not None: return Neighbor

    world[y+dy][x+dx] = cell
    world[y][x] = None
    return Success

width = 800
height = 600
scale = 10
world_width = 80
world_height = 60


world = []
for y in range(world_height):
    world.append([])
    for x in range(world_width):
        #color = Color(int(y/world_height*255), int(x/world_width*255), randint(0,255),255)
        color = Color(randint(0, 255), randint(0, 255), randint(0, 255), 255)
        if random() < 0.3:
            world[y].append(Cell(color))
        else: world[y].append(None)
camera = Camera(0, 0)

init_window( width, height, "superbox 3.0")
set_target_fps(60)
while not window_should_close():

    # ---- input ----
    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x / scale
        camera.y += get_mouse_delta().y / scale
    if get_mouse_wheel_move() > 0:
        if scale <= 50:
            scale += 1 # there is some issue here idfk..
            # i also shouldn't be adding i should be multiplxing
            camera.x += (width/scale - width/(scale - 1)) / 2
            camera.y += (height/scale - height/(scale - 1)) / 2
    if get_mouse_wheel_move() < 0:
        if scale >= 5:
            scale -= 1
            camera.x += (width/scale - width/(scale + 1)) / 2
            camera.y += (height/scale - height/(scale + 1)) / 2
    #   interaction
    if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
        x = int(get_mouse_x() / scale - camera.x)
        y = int(get_mouse_y() / scale - camera.y)
        if x >= 0 and x < world_width and y >= 0 and y < world_height:
            if is_key_down(KEY_LEFT_SHIFT):
                world[y][x] = Cell(YELLOW)
                world[y][x].vx = 0
                world[y][x].vy = -1
            else:
                world[y][x] = Cell(GRAY)
                world[y][x].vx = 0
                world[y][x].vy = 0

    # ---- simulation ----
    for y in range(world_height):
        for x, cell in enumerate(world[y]):
            if cell is None: continue
            # velocity from surroundings
            cell.vy += 0.01

            # delta from velocity
            dx, dy = 0, 0
            if abs(cell.vx) > random(): dx = 1
            if cell.vx < 0: dx *= -1
            if abs(cell.vy) > random(): dy = 1
            if cell.vy < 0: dy *= -1

            # swapping stuff and collision reactions
            state = attempt_swap(world, x, y, dx, dy)
            if state == Neighbor:
                # these ratios and the variation will depend on the bouncyness and absorption of the cells
                world[y+dy][x+dx].vx += cell.vx * .5 + (random()*.05 - .025) # adding some randomisation to immitate particles not colliding perfectly centered but still in a pixely way
                world[y+dy][x+dx].vy += cell.vy * .5 + (random()*.05 - .025)
                cell.vx *= 0.4
                cell.vy *= 0.4

    # ---- rendering ----
    begin_drawing()
    clear_background(Color( 15, 15, 40, 255))
    for y in range(-1, int(height / scale)+1):
        world_y = y - int(camera.y)
        if camera.y < 0: world_y += 1
        if world_y < 0: continue
        if world_y >= world_height: break
        if world[world_y].count(None) == world_width: continue
        for x in range(-1, int(width / scale)+1):
            world_x = x - int(camera.x)
            if camera.x < 0: world_x += 1
            if world_x < 0: continue
            if world_x >= world_width: break
            if world[world_y][world_x] is None: continue

            cell = world[world_y][world_x]
            draw_rectangle(int((x + camera.x%1)*scale), int((y + camera.y%1)*scale), scale, scale, cell.color)

    draw_rectangle(int(width/2-1), int(height/2-8), 2, 16, WHITE)
    draw_rectangle(int(width/2-8), int(height/2-1), 16, 2, WHITE)
    draw_fps(3, 3)
    end_drawing()

close_window()
