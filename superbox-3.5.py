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


world = World(150, 100)
camera = CAM(0, 0, 5) 
playing = True
mouse_on_clickable = False
cursor_size = 4

materials = [Water, Sand, Stone, Sky_stone, Wood, Fire, Smoke, Ash, Dirt]
selected = 0

views = ['color', 'energy', 'velocity', 'moister', 'temperature']
view = 0

hud = Widget(0, 0, 1, 1, "hud", Color(0, 0, 0, 0))
hud.add_child(Widget(10, 5, width-55, 30, "windometer", color=Color(0,0,0,0), borders=WHITE))
hud.add_child(Widget(10, 40, width-55, 30, "fpsmeter", color=Color(0,0,0,0), borders=WHITE))
hud.add_child(Widget(10, 5, 30, 30, "close", text="x", text_size=25, color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, text_x_offset=3, text_y_offset=0, clickable=True))
hud.add_child(Widget(10, 40, 30, 30, "fullscreen", text="[ ]", text_size=18, color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, text_x_offset=11, text_y_offset=1, clickable=True))
hud.add_child(Widget(10, 75, 30, 30, "pause", text="| |", text_size=16, color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, text_x_offset=11, text_y_offset=1, clickable=True))
hud.add_child(Widget(10, 5, 30, 30, "materials_btn", text="M", text_size=20, color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, vertical_align=END, clickable=True))
hud.add_child(Widget(10, 40, 30, 30, "tools_btn", text="T", text_size=20, color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, vertical_align=END, clickable=True))
hud.add_child(Widget(10, 75, 30, 30, "view_btn", text="V", text_size=20, color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, vertical_align=END, clickable=True))

hud.add_child(Widget(45, 5, 470, 20, "tools_head", text="T O O L S", text_size=20, text_color=Color(25,25,25,255), text_x_offset=15, color=WHITE, horizontal_align=END, vertical_align=END, dragable=True, visible=False))
hud.get_child("tools_head").add_child(Widget(10, 20, 470, 300, "tools", text='WIP', color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, vertical_align=END))

hud.add_child(Widget(45, 5, 470, 20, "materials_head", text="M A T E R I A L S", text_size=20, text_color=Color(25,25,25,255), text_x_offset=15, color=WHITE, horizontal_align=END, vertical_align=END, dragable=True, visible=False))
hud.get_child("materials_head").add_child(Widget(0, 20, 470, 300, "materials", color=Color(130,130,130,140), borders=WHITE, horizontal_align=END, vertical_align=END))


hud.get_child("windometer").add_child(Widget(0, 0, 120, hud.get_child("windometer").h, "wind", color=Color(130,130,130,140), text="windometer", text_size=20, text_x_offset=13))
hud.get_child("fpsmeter").add_child(Widget(0, 0, 120, hud.get_child("fpsmeter").h, "wind", color=Color(130,130,130,140), text="FPS-meter", text_size=20, text_x_offset=7))
def windometer_update():
    hud.get_child("windometer").w = width-55
    draw_rectangle(int(hud.get_child("windometer").x + hud.get_child("windometer").w/2), int(hud.get_child("windometer").y + 4), 1, hud.get_child("windometer").h-8, WHITE)
    if world.max_wind != 0:
        draw_rectangle(int(hud.get_child("windometer").x + hud.get_child("windometer").w/2 + world.wind/world.max_wind*hud.get_child("windometer").w/2), int(hud.get_child("windometer").y + 2), 2, hud.get_child("windometer").h-4, WHITE)
def fpsmeter_update():
    hud.get_child("fpsmeter").w = width-55
    if get_frame_time() != 0:
        draw_rectangle(int(hud.get_child("fpsmeter").x + 1/get_frame_time()/50*hud.get_child("fpsmeter").w-2), int(hud.get_child("fpsmeter").y + 2), 2, hud.get_child("fpsmeter").h-4, WHITE)
def pause():
    global playing
    playing = not playing
    if not playing:
        hud.get_child("pause").text_size = 21
        hud.get_child("pause").text = '>'
        hud.get_child("pause").text_x_offset = 4
    else:
        hud.get_child("pause").text_size = 16
        hud.get_child("pause").text = '| |'
        hud.get_child("pause").text_x_offset = 11
def fullscreen():
    set_window_size(get_monitor_width(get_current_monitor()), get_monitor_height(get_current_monitor()))
    toggle_fullscreen()
    if not is_window_fullscreen():
        set_window_size(800, 600)
def materials_btn():
    hud.get_child("materials_head").visible = not hud.get_child("materials_head").visible
def tools_btn():
    hud.get_child("tools_head").visible = not hud.get_child("tools_head").visible
def view_mode():
    global view
    view += 1
    if is_key_down(KEY_LEFT_SHIFT): view -= 2
    view %= 4
def select_material(m):
    global selected
    selected = m

hud.get_child("windometer").custom_updates.append(windometer_update)
hud.get_child("fpsmeter").custom_updates.append(fpsmeter_update)
hud.get_child("close").execute = close_window
hud.get_child("fullscreen").execute = fullscreen
hud.get_child("pause").execute = pause
hud.get_child("materials_btn").execute = materials_btn
hud.get_child("tools_btn").execute = tools_btn
hud.get_child("view_btn").execute = view_mode
for i in range(len(materials)):
    hud.get_child("materials").add_child(Widget((i%3)*155+5, int(i/3)*45+5, 150, 40, id="m-"+str(i), text=materials[i].__name__.replace('_', ' '), text_size=20, color=Color(70, 70, 70, 110), borders=WHITE, vertical_align=END, horizontal_align=END, clickable=True))
    hud.get_child("m-"+str(i)).execute = [select_material, i]
hud.get_child("materials").h = ceil(len(materials)/3)*45+5

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
        if is_mouse_button_down(MOUSE_BUTTON_MIDDLE):
            camera.x += get_mouse_delta().x * .8
            camera.y += get_mouse_delta().y * .8
        if get_mouse_wheel_move() > 0: camera.vz += camera.scroll_speed
        if get_mouse_wheel_move() < 0: camera.vz -= camera.scroll_speed
        if (is_mouse_button_down(MOUSE_BUTTON_LEFT) or is_mouse_button_down(MOUSE_BUTTON_RIGHT)) and not (is_key_down(KEY_LEFT_SHIFT) or is_key_down(KEY_RIGHT_SHIFT)):
            x = int((get_mouse_x() - camera.x) / camera.z) % world.width
            y = int((- get_mouse_y() + camera.y) / camera.z) % world.height
            for y0 in range(int(-cursor_size-1), int(cursor_size+1)):
                for x0 in range(int(-cursor_size-1), int(cursor_size+1)):
                    if y0**2 + x0**2 <= cursor_size**2:
                        x1 = (x0 + x) % world.width
                        y1 = (y0 + y) % world.height
                        if x1 < world.width and x1 >= 0 and y1 < world.height and y1 >= 0:
                                world.world[y1][x1] = materials[selected]()
                                if is_mouse_button_down(MOUSE_BUTTON_RIGHT):
                                    world.world[y1][x1] = None

    if is_key_pressed(KEY_F): fullscreen()
    if is_key_pressed(KEY_SPACE): pause()
    if is_key_pressed(KEY_TAB): view_mode()
    # ---- simulation ----
    step += 1
    
    if camera.z * (1 + camera.vz) > 1.2:
        camera.z *= 1 + camera.vz
        camera.x *= 1 + camera.vz
        camera.y *= 1 + camera.vz
    else: camera.vx = 0
    camera.vz *= .8
    if abs(camera.vz) < .01: camera.vz = 0

    #if step % 1000 == 0: save()

    if playing:
        world.update()

    # ---- rendering ----
    begin_drawing()
    clear_background(WHITE)
    
    draw_rectangle_gradient_v(0, 0, width, height+100, Color(160, 220, 250, 255), Color(80, 185, 240, 255))
    render_texture = world.render_texture(render_texture, view)
    world.render(render_texture, camera, width, height)

    # ui
    set_mouse_cursor(0)
    mouse_on_clickable = hud.update()
    if mouse_on_clickable: set_mouse_cursor(4)
    elif is_cursor_on_screen(): set_mouse_cursor(3)
    draw_text(views[view], 10, height-30, 23, WHITE)

    end_drawing()

close_window()