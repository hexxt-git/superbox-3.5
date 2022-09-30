from math import *
from random import *
from pyray import *
from time import *
from superEngine import *
from materials import *

cell_names = ['plastic', 'stone', 'sand', 'water', 'smoke']
cell_classes = [Plastic, Stone, Sand, Water, Smoke]
selected = 0

width = 800
height = 600
color_mode = 0


world = World(200, 100)
camera = CAM(0, 0, 5)

init_window( width, height, "superbox 3.0")
render_texture = load_render_texture(world.width, world.height)
set_target_fps(50)
#hide_cursor()
while not window_should_close():

    # ---- input ----
    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x
        camera.y += get_mouse_delta().y
    if get_mouse_wheel_move() > 0:
        if camera.z <= 50: camera.z *= 1 + camera.scroll_speed
    if get_mouse_wheel_move() < 0:
        if camera.z > 1: camera.z *= 1 - camera.scroll_speed
    if is_key_pressed(KEY_TAB):
        color_mode += 1
        color_mode %= 3
    if is_key_pressed(KEY_SPACE):
        selected += 1
        selected %= len(cell_names)

    #   interaction
    if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
        x = int((get_mouse_x() - camera.x ) / camera.z)
        y = int((- get_mouse_y() + camera.y ) / camera.z)
        y %= (world.height - 1)
        x %= (world.width - 1)
        if x < world.width and x >= 0 and y < world.height and y >= 0:
            if is_key_down(KEY_LEFT_CONTROL):
                world.world[y][x] = None
                world.world[y][x+1] = None
                world.world[y+1][x] = None
                world.world[y+1][x+1] = None
            else:
                world.world[y][x] = cell_classes[selected]()
                world.world[y][x+1] = cell_classes[selected]()
                world.world[y+1][x] = cell_classes[selected]()
                world.world[y+1][x+1] = cell_classes[selected]()

    # ---- simulation ----
    world.update()

    # ---- rendering ----
    begin_drawing()
    clear_background(WHITE)
    draw_rectangle_gradient_v(0, 0, width, height, Color(153, 218, 255, 255), Color(84, 193, 255, 255))

    render_texture = world.render_texture(render_texture, color_mode)
    draw_texture_ex(render_texture.texture, Vector2(camera.x, camera.y), 0, camera.z, WHITE)

    # HUD
    draw_rectangle(int((world.wind/world.max_wind/2+0.5)*.95*width), 5, 2, 20, WHITE)
    draw_rectangle(int(width/2-1), 3, 2, 4, WHITE)

    draw_fps(5, 5)
    draw_text(cell_names[selected] + '  // press space to change material', 5, 25, 23, DARKGREEN)
    end_drawing()

close_window()