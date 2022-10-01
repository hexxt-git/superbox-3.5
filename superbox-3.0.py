from math import *
from random import *
from pyray import *
from time import *
from superEngine import *
from materials import *

cell_names = ['plastic', 'stone', 'sand', 'water', 'smoke']
cell_classes = [Plastic, Stone, Sand, Water, Smoke]
selected = 1

width = 800
height = 600
color_mode = 0


world = World(300, 300)
camera = CAM(0, 0, 5)

init_window( width, height, "superbox 3.0")
render_texture = load_render_texture(world.width, world.height)
set_target_fps(50)
#hide_cursor()
while not window_should_close():

    x_scale = int(world.width * camera.z)
    y_scale = int(world.height * camera.z)

    # ---- input ----
    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x
        camera.y += get_mouse_delta().y
    if get_mouse_wheel_move() > 0:
        if camera.z * (1 + camera.scroll_speed) <= 50:
            camera.vz += camera.scroll_speed
    if get_mouse_wheel_move() < 0:
        if camera.z * (1 - camera.scroll_speed) > 1:
            camera.vz -= camera.scroll_speed
    camera.z *= 1 + camera.vz
    camera.x *= 1 + camera.vz
    camera.y *= 1 + camera.vz
    camera.vz *= .8
    
    
    if is_key_pressed(KEY_TAB):
        color_mode += 1
        color_mode %= 3
    if is_key_pressed(KEY_SPACE):
        selected += 1
        selected %= len(cell_names)

    #   interaction
    if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
        x = int((get_mouse_x() - camera.x) / camera.z)
        y = int((- get_mouse_y() + camera.y) / camera.z)
        y %= world.height
        x %= world.width
        if x+1 < world.width and x >= 0 and y+1 < world.height and y >= 0:
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

    for y in range(-2, int(height/y_scale+1)): # im so done with this
        for x in range(-2, int(width/x_scale+1)):
            draw_texture_ex(render_texture.texture,
            Vector2(
                x*x_scale + camera.x%x_scale,
                y*y_scale + camera.y%y_scale
            ), 0, camera.z, WHITE)
            #draw_text(f'{int(x)}, {y}', int(x*x_scale +camera.x%x_scale), int(y*y_scale +camera.y%y_scale), int(camera.z * 5), WHITE)
    # HUD
    draw_rectangle(int((world.wind/world.max_wind/2+0.5)*.95*width), 5, 2, 20, WHITE)
    draw_rectangle(int(width/2-1), 3, 2, 4, WHITE)

    draw_fps(5, 5)
    draw_text(cell_names[selected] + '  // press space to change material', 5, 25, 23, DARKGREEN)
    end_drawing()

close_window()