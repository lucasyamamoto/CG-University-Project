import numpy as np
import math

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

def build_vertices(vert_list):
    total_verts = len(vert_list)
    vertices = np.zeros(total_verts, [("position", np.float32, 3)])
    vertices['position'] = np.array(vert_list)
    return vertices

def multiplica_matriz(a,b):
    m_a = a.reshape(4,4)
    m_b = b.reshape(4,4)
    m_c = np.dot(m_a,m_b)
    c = m_c.reshape(1,16)
    return c

def CoordCilindro(t, h, r):
    x = r * math.cos(t)
    y = r * math.sin(t)
    z = h
    return (x,y,z)

def convert_coord(x, y, z):
    x = x/(WINDOW_WIDTH/2)
    y = y/(WINDOW_HEIGHT/2)
    z = z/(WINDOW_WIDTH/2)
    return (x, y, z)

