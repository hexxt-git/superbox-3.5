from pyray import *

init_window(800, 600, "WINDOW")

rtx = load_render_texture(80, 80)

while not window_should_close():

    begin_texture_mode(rtx)
    clear_background(WHITE)
    draw_circle(20, 20, 8, RED)
    end_texture_mode()

    begin_drawing()
    clear_background(GRAY)
    draw_texture(rtx.texture, 50, 50, WHITE)
    draw_texture(rtx.texture, 50, 150, WHITE)
    draw_texture(rtx.texture, 150, 50, WHITE)
    draw_texture(rtx.texture, 150, 150, WHITE)

    end_drawing()

close_window()