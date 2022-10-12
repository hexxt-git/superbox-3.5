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

hud = Widget(0, 0, width, height, "hud", Color(0, 0, 0, 0))
hud.add_child(Widget(10, 10, 250, 50, "show/hide", Color(30, 30, 30, 230), "show/hide", 30, WHITE, clickable=True))
hud.add_child(Widget(10, 65, 250, 15, "list_parent", Color(30, 30, 30, 230), dragable=True))
hud.get_child("list_parent").add_child(Widget(0, 15, 250, 200, "list", Color(60, 60, 60, 180)))
hud.get_child("list").add_child(Widget( 0, 0, 250, 50, color=Color(230, 230, 230, 200), text="1", text_color=BLACK, clickable=True))
hud.get_child("list").add_child(Widget( 0, 55, 250, 50, color=Color(230, 230, 230, 200), text="2", text_color=BLACK, clickable=True))
hud.get_child("list").add_child(Widget( 0, 110, 250, 50, color=Color(230, 230, 230, 200), text="3", text_color=BLACK, clickable=True))
hud.add_child(Widget(-15, -15, 30, 30, 'printer', text=":p", text_size=20, clickable=True, color=RED, horizontal_align=CENTER, vertical_align=CENTER, text_x_offset=6, text_y_offset=-2))
hud.add_child(Widget(5, 5, 200, 30, 'test', text='test', color=Color(30, 30, 30, 230), vertical_align=END, horizontal_align=END, dragable=True))

def showHide():
    hud.get_child("list").visible = not hud.get_child("list").visible
hud.get_child("show/hide").execute = showHide
def printer():
    hud.print()
hud.get_child('printer').execute = printer
def gamin_background():
    hud.get_child('printer').color = color_from_hsv(
        color_to_hsv(hud.get_child('printer').color).x + 2,
        color_to_hsv(hud.get_child('printer').color).y,
        color_to_hsv(hud.get_child('printer').color).z,
        )
    hud.get_child('printer').color.a = 180
hud.get_child('printer').custom_updates.append(gamin_background)

set_config_flags(FLAG_WINDOW_RESIZABLE)
init_window( width, height, "superbox 3.0")
render_texture = load_render_texture(world.width, world.height)
set_target_fps(50)
step = 0
while not window_should_close():
    width = get_screen_width()
    height = get_screen_height()
    # ---- input ----
    #   navigation
    if not mouse_on_clickable:
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
    
    draw_rectangle_gradient_v(0, 0, width, height, Color(160, 220, 250, 255), Color(80, 185, 240, 255))
    render_texture = world.render_texture(render_texture, 0)
    world.render(render_texture, camera, width, height)

    # ui
    set_mouse_cursor(0)
    mouse_on_clickable = hud.update()
    if mouse_on_clickable: set_mouse_cursor(4)
    else: set_mouse_cursor(0)
    end_drawing()

close_window()