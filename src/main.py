import glfw
import sys
import numpy as np

from opengl_functions import *
from shapes import *
from utils import *

shape_index = 0
global_input = transform_input()
def key_event(window, key, scancode, action, mods):
    global global_input, shape_index
    
    # print('[key event] key=',key)
    # print('[key event] scancode=',scancode)
    # print('[key event] action=',action)
    # print('[key event] mods=',mods)
    # print('-------')

    # Action = 0: key up
    # Action = 1: key down
    # Action = 2: key repeat
    if action == 2:
        return

    # Translate input
    if key == 262: global_input.t['x'] = 1*action
    if key == 263: global_input.t['x'] = -1*action
    if key == 265: global_input.t['y'] = 1*action
    if key == 264: global_input.t['y'] = -1*action
    if key == 74: global_input.t['z'] = 1*action
    if key == 75: global_input.t['z'] = -1*action

    # Rotate input
    if key == 87: global_input.r['x'] = (np.pi/80)*action
    if key == 83: global_input.r['x'] = (-np.pi/80)*action
    if key == 68: global_input.r['y'] = (np.pi/80)*action
    if key == 65: global_input.r['y'] = (-np.pi/80)*action
    if key == 81: global_input.r['z'] = (np.pi/80)*action
    if key == 69: global_input.r['z'] = (-np.pi/80)*action

    # Scale input
    if key == 61: global_input.s['x'] = 0.01*action + 1
    if key == 45: global_input.s['x'] = -0.01*action + 1

    # Select shape
    if key >= 49 and key <= 53:
        shape_index = key - 49

def init_window():
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "My OpenGL", None, None)
    glfw.make_context_current(window)
    glfw.show_window(window)
    return window


def main():
    window = init_window()
    locations = init_opengl()

    # Store the shapes in an array
    shapes = []

    ### Shapes here - One time transformations - Start ###
    # All shapes start at the origin (center)
    
    tetra = tetrahedron()
    tetra.add_scale(0.15, 0.15, 0.15)
    tetra.add_translation(-300, 300, 0)
    tetra.add_rotation('x', r.random())
    tetra.add_rotation('y', r.random())
    tetra.add_rotation('z', r.random())

    c = cube()
    c.add_scale(0.15, 0.15, 0.15)
    c.add_translation(300, 300, 0)
    c.add_rotation('x', r.random())
    c.add_rotation('y', r.random())
    c.add_rotation('z', r.random())

    octa = octahedron()
    octa.add_scale(0.3, 0.3, 0.3)
    octa.add_translation(-300, -300, 0)
    octa.add_rotation('x', r.random())
    octa.add_rotation('y', r.random())
    octa.add_rotation('z', r.random())

    ico = icosahedron()
    ico.add_scale(0.15, 0.15, 0.15)
    ico.add_translation(300, -300, 0)
    ico.add_rotation('x', r.random())
    ico.add_rotation('y', r.random())
    ico.add_rotation('z', r.random())

    dode = dodecahedron()
    dode.add_scale(0.15, 0.15, 0.15)
    dode.add_rotation('x', r.random())
    dode.add_rotation('y', r.random())
    dode.add_rotation('z', r.random())

    # Shape used as a selection indicator
    select = icosahedron()
    select.add_scale(0.02, 0.02, 0.02)
    select.add_translation(0, 0, 0)

    g = grid()

    ### Shapes here - End ###

    shapes.append(tetra)
    shapes.append(c)
    shapes.append(octa)
    shapes.append(ico)
    shapes.append(dode)
    shapes.append(select)
    shapes.append(g)

    create_shapes(shapes, locations)
    amount_with_input = 5

    glfw.set_key_callback(window,key_event)
    while not glfw.window_should_close(window):

        # Input:
        # A, D: Rotate around x (rot_x)
        # W, S: Rotate around y (rot_y)
        # Q, E: Rotate around z (rot_z)
        # Arrow Keys: Translate x and y (t_x, t_y)
        # J, K: Translate z (t_z)
        # -, +: Scale
        # 1 - 5: Select shape

        glfw.poll_events() 
        gt_x, gt_y, gt_z = global_input.t['x'], global_input.t['y'], global_input.t['z']
        gr_x, gr_y, gr_z = global_input.r['x'], global_input.r['y'], global_input.r['z']
        gs_x, gs_y, gs_z = global_input.s['x'], global_input.s['y'], global_input.s['z']

        if shape_index < amount_with_input:
            shape_to_move = shapes[shape_index]
            shape_to_move.add_translation(gt_x, gt_y, gt_z)
            shape_to_move.add_rotation('x', gr_x)
            shape_to_move.add_rotation('y', gr_y)
            shape_to_move.add_rotation('z', gr_z)
            shape_to_move.add_scale(gs_x, gs_x, gs_x) # homogeneous scale
            select.input.t['x'] = shape_to_move.input.t['x'] - 70 - 300*shape_to_move.input.s['x']
            select.input.t['y'] = shape_to_move.input.t['y'] + 70 + 300*shape_to_move.input.s['x']

        select.add_rotation('x', math.pi/80)
        select.add_rotation('y', math.pi/80)
        select.add_rotation('z', math.pi/80)

        update_shapes(shapes)
        draw_shapes(shapes, locations)

        # Cube position
        # print("X", c.input.t['x'])
        # print("Y", c.input.t['y'])
        # print("Z", c.input.t['z'])

        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    sys.exit(main())
