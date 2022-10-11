from math import *
from random import *
from pyray import *
from time import *
from superEngine import *
from materials import *

width = 800
height = 600

def save():
    world_save = world.save()
    return True

world = World(200, 200)
camera = CAM(0, 0, 5) 
state = 0
mouse_on_clickable = False

hud = Widget(0, 0, width, height, Color(0, 0, 0, 0))
hud.add_child(Widget(50, 50, 250, 50, RED, "child", 30, BLUE, clickable=True))
hud.add_child(Widget(50, 120, 250, 300, GREY,))

init_window( width, height, "superbox 3.0")
render_texture = load_render_texture(world.width, world.height)
set_target_fps(50)
step = 0
while not window_should_close():
    # ---- input ----
    #   navigation
    if is_mouse_button_down(MOUSE_BUTTON_LEFT):
        camera.x += get_mouse_delta().x
        camera.y += get_mouse_delta().y
    if not is_key_down(KEY_LEFT_SHIFT):
        if get_mouse_wheel_move() > 0: camera.vz += camera.scroll_speed
        if get_mouse_wheel_move() < 0: camera.vz -= camera.scroll_speed
    if camera.z * (1 + camera.vz) > 1:
        camera.z *= 1 + camera.vz
        camera.x *= 1 + camera.vz
        camera.y *= 1 + camera.vz
    else: camera.vx = 0
    camera.vz *= .75
    if abs(camera.vz) < .01: camera.vz = 0

    # ---- simulation ----
    step += 1
    #if step % 1000 == 0: save()
    world.update()

    # ---- rendering ----
    begin_drawing()
    clear_background(WHITE)
    
    draw_rectangle_gradient_v(0, 0, width, height, Color(153, 218, 255, 255), Color(84, 193, 255, 255))
    render_texture = world.render_texture(render_texture, 0)
    world.render(render_texture, camera, width, height)

    # ui
    set_mouse_cursor(0)
    mouse_on_clickable = hud.update()
    if mouse_on_clickable:
        set_mouse_cursor(4)
    else: set_mouse_cursor(0)
    end_drawing()

close_window()