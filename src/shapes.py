from opengl_functions import *
from utils import *
import random as r
import numpy as np
import ctypes
import abc

class transform_input():
    def __init__(self, t_x=0, t_y=0, t_z=0, rot_x=0, rot_y=0, rot_z=0, s_x=1, s_y=1, s_z=1):
        # Translation
        self.t = { "x": t_x, "y": t_y, "z": t_z } 

        # Rotation
        self.r = { "x": float(rot_x), "y": float(rot_y), "z": float(rot_z) } 

        # Scale
        self.s = { "x": float(s_x), "y": float(s_y), "z": float(s_z) }
        return

class shape:
    def __init__(self):
        self.vao = None 
        self.vbo = None
        self.primative = None
        self.vertices = None
        self.color = { "r": r.random(), "g": r.random(), "b": r.random() }
        self.transform = np.identity(4, np.float32)
        self.input = transform_input()
        return

    @abc.abstractmethod
    def create_vertices(self):
        pass

    def create(self, locations):
        self.vertices = self.create_vertices()
        if self.vertices is None:
            return
        loc_position = locations['position']
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_DYNAMIC_DRAW)
        stride = self.vertices.strides[0]
        offset = ctypes.c_void_p(0) # NULL pointer
        glEnableVertexAttribArray(loc_position)
        glVertexAttribPointer(loc_position, 3, GL_FLOAT, False, stride, offset)
        return

    def add_translation(self, x, y, z):
        self.input.t['x'] += x
        self.input.t['y'] += y
        self.input.t['z'] += z
        return

    def translate(self):
        x, y, z = self.input.t['x'], self.input.t['y'], self.input.t['z']
        x, y, z = convert_coord(x, y, z)
        mat_translation = np.array([ 
            1.0, 0.0, 0.0, x, 
            0.0, 1.0, 0.0, y, 
            0.0, 0.0, 1.0, z, 
            0.0, 0.0, 0.0, 1.0], np.float32)
        self.transform = multiplica_matriz(mat_translation, self.transform)
        return

    def add_rotation(self, axis, angle):
        self.input.r[axis] += angle
        return

    def rotate(self, axis):
        cos = math.cos(self.input.r[axis])
        sin = math.sin(self.input.r[axis])
        if axis == "x":
            mat_rotation = np.array([ 
                1.0, 0.0, 0.0, 0.0, 
                0.0, cos, -sin, 0.0, 
                0.0, sin, cos, 0.0, 
                0.0, 0.0, 0.0, 1.0], np.float32)
        elif axis == "y":
            mat_rotation = np.array([ 
                cos, 0.0, sin, 0.0, 
                0.0, 1.0, 0.0, 0.0, 
                -sin, 0.0, cos, 0.0, 
                0.0, 0.0, 0.0, 1.0], np.float32)
        elif axis == "z":
            mat_rotation = np.array([ 
                cos, -sin, 0.0, 0.0, 
                sin, cos, 0.0, 0.0, 
                0.0, 0.0, 1.0, 0.0, 
                0.0, 0.0, 0.0, 1.0], np.float32)
        else:
            return
        self.transform = multiplica_matriz(mat_rotation, self.transform)
        return

    def add_scale(self, x, y, z):
        self.input.s['x'] *= x
        self.input.s['y'] *= y
        self.input.s['z'] *= z
        return

    def scale(self):
        x, y, z = self.input.s['x'], self.input.s['y'], self.input.s['z']
        mat_scale = np.array([ 
            x, 0.0, 0.0, 0.0, 
            0.0, y, 0.0, 0.0, 
            0.0, 0.0, z, 0.0, 
            0.0, 0.0, 0.0, 1.0], np.float32)
        self.transform = multiplica_matriz(mat_scale, self.transform)
        return

    def add_color(self, r, g, b):
        self.color = { "r": r, "g": g, "b": b }
        return

    def update(self):
        ###! ORDER: SCALE, ROTATE, TRANSLATE
        # Translation before rotation = change rotation center
        self.scale()
        self.rotate("x")
        self.rotate("y")
        self.rotate("z")
        self.translate()
        return

    def bind_and_trasnform(self, locations):
        loc_transform = locations['transform']
        loc_color = locations['color']
        glBindVertexArray(self.vao)
        glUniform4f(loc_color, self.color['r'], self.color['g'], self.color['b'], 1.0)
        glUniformMatrix4fv(loc_transform, 1, GL_TRUE, self.transform)
        self.transform = np.identity(4, np.float32)
        return

    # Draw the whole shape with the same color
    def draw(self, locations):
        self.bind_and_trasnform(locations)

        if self.vertices is not None:
            glDrawArrays(self.primative, 0, len(self.vertices))

        return

class tetrahedron(shape):
    def __init__(self):
        super().__init__()
        return

    def create_vertices(self):

        # 4 choose 3
        # (1.0, 1.0, 1.0), # 1
        # (1.0, -1.0, -1.0), # 2
        # (-1.0, 1.0, -1.0), # 3
        # (-1.0, -1.0, 1.0) # 4

        vertices_list = [ 

                # 1-2-3
                (1.0, 1.0, 1.0), # 1
                (1.0, -1.0, -1.0), # 2
                (-1.0, 1.0, -1.0), # 3

                # 1-3-4
                (1.0, 1.0, 1.0), # 1
                (-1.0, 1.0, -1.0), # 3
                (-1.0, -1.0, 1.0), # 4

                # 1-4-2
                (1.0, 1.0, 1.0), # 1
                (-1.0, -1.0, 1.0), # 4
                (1.0, -1.0, -1.0), # 2

                # 2-4-3
                (1.0, -1.0, -1.0), # 2
                (-1.0, -1.0, 1.0), # 4
                (-1.0, 1.0, -1.0), # 3

                ]

        return build_vertices(vertices_list)

    def draw(self, locations):
        self.bind_and_trasnform(locations)

        loc_color = locations['color']
        glUniform4f(loc_color, 1, 0, 0, 1.0) ### vermelho
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glUniform4f(loc_color, 0, 0, 1, 1.0) ### azul
        glDrawArrays(GL_TRIANGLES, 3, 3)
        glUniform4f(loc_color, 0, 1, 0, 1.0) ### verde
        glDrawArrays(GL_TRIANGLES, 6, 3)
        glUniform4f(loc_color, 1, 1, 0, 1.0) ### amarela
        glDrawArrays(GL_TRIANGLES, 9, 3)

        return


class cube(shape):
    def __init__(self):
        super().__init__()
        return

    def create_vertices(self):
        vertices_list = [
                # Face 1 do Cubo (vértices do quadrado)
                (-1.0, -1.0, +1.0),
                (+1.0, -1.0, +1.0),
                (-1.0, +1.0, +1.0),
                (+1.0, +1.0, +1.0),

                # Face 2 do Cubo
                (+1.0, -1.0, +1.0),
                (+1.0, -1.0, -1.0),         
                (+1.0, +1.0, +1.0),
                (+1.0, +1.0, -1.0),

                # Face 3 do Cubo
                (+1.0, -1.0, -1.0),
                (-1.0, -1.0, -1.0),            
                (+1.0, +1.0, -1.0),
                (-1.0, +1.0, -1.0),

                # Face 4 do Cubo
                (-1.0, -1.0, -1.0),
                (-1.0, -1.0, +1.0),         
                (-1.0, +1.0, -1.0),
                (-1.0, +1.0, +1.0),

                # Face 5 do Cubo
                (-1.0, -1.0, -1.0),
                (+1.0, -1.0, -1.0),         
                (-1.0, -1.0, +1.0),
                (+1.0, -1.0, +1.0),

                # Face 6 do Cubo
                (-1.0, +1.0, +1.0),
                (+1.0, +1.0, +1.0),           
                (-1.0, +1.0, -1.0),
                (+1.0, +1.0, -1.0)
                ]
        return build_vertices(vertices_list)

    def draw(self, locations):
        self.bind_and_trasnform(locations)

        loc_color = locations['color']
        glUniform4f(loc_color, 1, 0, 0, 1.0) ### vermelho
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glUniform4f(loc_color, 0, 0, 1, 1.0) ### azul
        glDrawArrays(GL_TRIANGLE_STRIP, 4, 4)
        glUniform4f(loc_color, 0, 1, 0, 1.0) ### verde
        glDrawArrays(GL_TRIANGLE_STRIP, 8, 4)
        glUniform4f(loc_color, 1, 1, 0, 1.0) ### amarela
        glDrawArrays(GL_TRIANGLE_STRIP, 12, 4)
        glUniform4f(loc_color, 0.5, 0.5, 0.5, 1.0) ### cinza
        glDrawArrays(GL_TRIANGLE_STRIP, 16, 4)
        glUniform4f(loc_color, 0.5, 0, 0, 1.0) ### marrom
        glDrawArrays(GL_TRIANGLE_STRIP, 20, 4)

class octahedron(shape):
    def __init__(self):
        super().__init__()
        return

    def create_vertices(self):
        vertices_list = [

                # (1.0, 0.0, 0.0), # 1
                # (-1.0, 0.0, 0.0), # 2

                # (0.0, 1.0, 0.0), # 1
                # (0.0, -1.0, 0.0), # 2

                # (0.0, 0.0, 1.0), # 1
                # (0.0, 0.0, -1.0), # 2

                # 1-1-1
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0), 

                # 2-1-1
                (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, 1.0), 

                # 1-2-1
                (1.0, 0.0, 0.0),
                (0.0, -1.0, 0.0),
                (0.0, 0.0, 1.0), 

                # 1-1-2
                (1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, -1.0),

                # 2-1-2
                (-1.0, 0.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 0.0, -1.0),

                # 1-2-2
                (1.0, 0.0, 0.0),
                (0.0, -1.0, 0.0),
                (0.0, 0.0, -1.0),

                # 2-2-1
                (-1.0, 0.0, 0.0),
                (0.0, -1.0, 0.0),
                (0.0, 0.0, 1.0),

                # 2-2-2
                (-1.0, 0.0, 0.0),
                (0.0, -1.0, 0.0),
                (0.0, 0.0, -1.0),
                ]
        return build_vertices(vertices_list)

    def draw(self, locations):
        self.bind_and_trasnform(locations)

        loc_color = locations['color']

        # Pyramid 1
        glUniform4f(loc_color, 1, 0, 0, 1.0) ### vermelho
        glDrawArrays(GL_TRIANGLES, 0, 3)
        glUniform4f(loc_color, 0, 0, 1, 1.0) ### azul
        glDrawArrays(GL_TRIANGLES, 3, 3)
        glUniform4f(loc_color, 0, 1, 0, 1.0) ### verde
        glDrawArrays(GL_TRIANGLES, 6, 3)
        glUniform4f(loc_color, 1, 1, 0, 1.0) ### amarela
        glDrawArrays(GL_TRIANGLES, 9, 3)

        # Pyramid 2
        glUniform4f(loc_color, 1, 0, 0, 1.0) ### vermelho
        glDrawArrays(GL_TRIANGLES, 12, 3)
        glUniform4f(loc_color, 0, 0, 1, 1.0) ### azul
        glDrawArrays(GL_TRIANGLES, 15, 3)
        glUniform4f(loc_color, 1, 1, 0, 1.0) ### amarela
        glDrawArrays(GL_TRIANGLES, 18, 3)
        glUniform4f(loc_color, 0, 1, 0, 1.0) ### verde
        glDrawArrays(GL_TRIANGLES, 21, 3)


class icosahedron(shape):
    def __init__(self):
        super().__init__()
        self.primative = GL_TRIANGLES
        return

    def create_vertices(self):
        r = 1.618

        A = (0, 1, r)
        B = (0, -1 , r)
        C = (0, 1, -r)
        D = (0, -1, -r)

        E = (1, r, 0)
        F = (-1, r, 0)
        G = (1, -r, 0)
        H = (-1, -r, 0)

        I = (r, 0, 1)
        J = (r, 0, -1)
        K = (-r, 0, 1)
        L = (-r, 0, -1)

        vertices_list = [
                # Top
                A, B, I,
                A, B, K,
                A, I, E,
                A, E, F,
                A, F, K,

                # Bottom
                D, C, J,
                D, C, L,
                D, L, H,
                D, H, G,
                D, G, J,

                # Middle
                B, G, I,
                G, I, J,
                I, J, E,
                J, E, C,
                E, C, F,
                C, F, L,
                F, L, K,
                L, K, H,
                K, H, B,
                H, B, G,
                ]

        return build_vertices(vertices_list)

    def draw(self, locations):
        self.bind_and_trasnform(locations)

        loc_color = locations['color']
        if self.vertices is not None:
            l = len(self.vertices["position"])
            for i in range(0, l, 3):
                glUniform4f(loc_color, (i*3/l)%1, (i*5/l)%1, (i*7/l)%1, 1.0)
                glDrawArrays(GL_TRIANGLES, i, 3)


class dodecahedron(shape):
    def __init__(self):
        super().__init__()
        self.primative = GL_TRIANGLE_FAN
        return

    def create_vertices(self):
        r = 1.618

        A = (1, 1, 1)
        B = (1, 1, -1)
        C = (1, -1, 1)
        D = (1, -1, -1)
        E = (-1, 1, 1)
        F = (-1, 1, -1)
        G = (-1, -1, 1)
        H = (-1, -1, -1)

        I = (0, 1/r, r)
        J = (0, 1/r, -r)
        K = (0, -1/r, r)
        L = (0, -1/r, -r)

        M = (1/r, r, 0)
        N = (1/r, -r, 0)
        O = (-1/r, r, 0)
        P = (-1/r, -r, 0)

        Q = (r, 0, 1/r)
        R = (r, 0, -1/r)
        S = (-r, 0, 1/r)
        T = (-r, 0, -1/r)

        vertices_list = [

                # 12 faces
                K, C, N, P, G,
                K, I, A, Q, C,
                K, I, E, S, G,
                I, A, M, O, E,
                A, Q, R, B, M,
                C, N, D, R, Q,
                G, S, T, H, P,
                E, O, F, T, S,
                M, B, J, F, O,
                T, F, J, L, H,
                P, H, L, D, N,
                B, R, D, L, J,
                ]

        return build_vertices(vertices_list)

    def draw(self, locations):
        self.bind_and_trasnform(locations)

        loc_color = locations['color']

        if self.vertices is not None:
            l = len(self.vertices["position"])
            for i in range(0, l, 5):
                glUniform4f(loc_color, (i*3/l)%1, (i*5/l)%1, (i*7/l)%1, 1.0)
                glDrawArrays(GL_TRIANGLE_FAN, i, 5)

class grid(shape):
    def __init__(self):
        super().__init__()
        self.primative = GL_LINES
        self.color = { "r": 0.0, "g": 0.0, "b": 0.0 }
        return

    def create_vertices(self):
        vertices_list = []
        for i in range(10):
            vertices_list.append([-0.1*i, -0.9, 0.0]) 
            vertices_list.append([-0.1*i, 0.9, 0.0])
            vertices_list.append([-0.9, -0.1*i, 0.0])
            vertices_list.append([0.9, -0.1*i, 0.0])
        for i in range(10):
            vertices_list.append([0.1*i, -0.9, 0.0]) 
            vertices_list.append([0.1*i, 0.9, 0.0])
            vertices_list.append([-0.9, 0.1*i, 0.0])
            vertices_list.append([0.9, 0.1*i, 0.0])
        return build_vertices(vertices_list)

class plane(grid):
    def __init__(self):
        super().__init__()
        self.primative = GL_TRIANGLE_STRIP

class penta(shape):
    def __init__(self):
        super().__init__()
        self.primative = GL_TRIANGLE_FAN
        return

    def create_vertices(self):
        vertices_list = [
                (-1,0,0),
                (-0.5,-1,0),
                (0.5,-1,0),
                (1,0,0),
                (0,1,0)
                ]
        return build_vertices(vertices_list)

class prism(shape):
    def __init__(self, radius, height, sides):
        super().__init__()
        self.primative = GL_TRIANGLES
        self.radius = float(radius)
        self.height = float(height)
        self.sides = int(sides)
        return

    def create_vertices(self):
        pi = np.pi
        sector_step = (pi*2)/self.sides # variar de 0 até 2π

        vertices_list = []
        for i in range(0, self.sides): # para cada lado
            u = i * sector_step # angulo setor
            un = 0 # angulo do proximo sector
            if i + 1 == self.sides:
                un = pi*2
            else:
                un = (i + 1)*sector_step

            # verticies do poligono
            p0=CoordCilindro(u, 0, self.radius)
            p1=CoordCilindro(u, self.height, self.radius)
            p2=CoordCilindro(un, 0, self.radius)
            p3=CoordCilindro(un, self.height, self.radius)

            # triangulo 1 (primeira parte do poligono)
            vertices_list.append(p0)
            vertices_list.append(p2)
            vertices_list.append(p1)

            # triangulo 2 (segunda e ultima parte do poligono)
            vertices_list.append(p3)
            vertices_list.append(p1)
            vertices_list.append(p2)

            vertices_list.append(p0)
            vertices_list.append(p2)
            vertices_list.append(CoordCilindro(0, 0, 0))

            #faz um triangulo a partir do mesmo angulo u, mas com as alturas em h = vn
            vertices_list.append(p1)
            vertices_list.append(p3)
            vertices_list.append(CoordCilindro(0, self.height, 0))

        return build_vertices(vertices_list)

    # Overriding draw
    def draw(self, locations):
        self.bind_and_trasnform(locations)

        loc_color = locations['color']
        if self.vertices is not None:
            for triangle in range(0,len(self.vertices),3):
                r.seed(triangle)
                R = r.random()
                G = r.random()
                B = r.random()  
                glUniform4f(loc_color, R, G, B, 1.0)
                glDrawArrays(GL_TRIANGLES, triangle, 3)     
        return

## Shape array

# Create the VAOs and VBOS and bind them to the objects
def create_shapes(shape_array, locations):
    len_array = len(shape_array) if len(shape_array) > 1 else 2
    vao = glGenVertexArrays(len_array) # vertex array object
    vbo = glGenBuffers(len_array) # vertex buffer object
    for idx, shape in enumerate(shape_array):
        shape.vao = vao[idx]
        shape.vbo = vbo[idx]
        shape.create(locations)
    return

def update_shapes(shape_array):
    for shape in shape_array:
        shape.update()
    return

def draw_shapes(shape_array, locations):
    # Clear screen
    glClear((GL_COLOR_BUFFER_BIT) | (GL_DEPTH_BUFFER_BIT)) # type: ignore
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Draw
    for shape in shape_array:
        shape.draw(locations)
    return
