from math import *
from random import *
from pyray import *
from time import *
from superEngine import *
from materials import *

material_names = ['plastic', 'stone', 'sky stone', 'sand', 'water', 'smoke']
material_classes = [Plastic, Stone, Sky_Stone, Sand, Water, Smoke]

width = 800
height = 600
color_mode = 0
selected = 1
cursor_size = 5

world = World(300, 300)
camera = CAM(0, 0, 5)

init_window( width, height, "superbox 3.0")
render_texture = load_render_texture(world.width, world.height)
set_target_fps(50)
hide_cursor()
while not window_should_close():

    x_scale = int(world.width * camera.z)
    y_scale = int(world.height * camera.z)

    # ---- input ----
    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x
        camera.y += get_mouse_delta().y
    if not is_key_down(KEY_LEFT_SHIFT):
        if get_mouse_wheel_move() > 0: camera.vz += camera.scroll_speed
        if get_mouse_wheel_move() < 0: camera.vz -= camera.scroll_speed
    else:
        if get_mouse_wheel_move() > 0 and cursor_size < 8: cursor_size += 1
        if get_mouse_wheel_move() < 0 and cursor_size > 1: cursor_size -= 1
    if camera.z * (1 + camera.vz) > 1:
        camera.z *= 1 + camera.vz
        camera.x *= 1 + camera.vz
        camera.y *= 1 + camera.vz
    else: camera.vx = 0
    camera.vz *= .75
    
    
    if is_key_pressed(KEY_TAB):
        color_mode += 1
        color_mode %= 3
    if is_key_pressed(KEY_SPACE):
        if is_key_down(KEY_SPACE): selected -= 2
        selected += 1
        selected %= len(material_names)

    #   interaction
    if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
        x = int((get_mouse_x() - camera.x) / camera.z) % world.width
        y = int((- get_mouse_y() + camera.y) / camera.z) % world.height
        for y0 in range(int(-cursor_size-1), int(cursor_size+1)):
            for x0 in range(int(-cursor_size-1), int(cursor_size+1)):
                if y0**2 + x0**2 <= cursor_size**2:
                    x1 = (x0 + x) % world.width
                    y1 = (y0 + y) % world.height
                    if x1 < world.width and x1 >= 0 and x1 < world.height and x1 >= 0:
                        if is_key_down(KEY_LEFT_CONTROL):
                            world.world[y1][x1] = None
                        else:
                            world.world[y1][x1] = material_classes[selected]()
                            if is_key_down(KEY_LEFT_SHIFT):
                                world.world[y1][x1].vx = random()*1.8-.9
                                world.world[y1][x1].vy = random()*1.8-.9

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
            
    # HUD
    draw_rectangle(int((world.wind/world.max_wind/2+0.5)*.95*width), 5, 2, 20, WHITE)
    draw_rectangle(int(width/2-1), 3, 2, 4, WHITE)
    draw_circle(get_mouse_x(), get_mouse_y(), int(cursor_size * camera.z), material_classes[selected]().color)

    draw_text(material_names[selected], 5, 5, 28, WHITE)
    end_drawing()

close_window()