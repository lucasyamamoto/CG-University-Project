from OpenGL.GL import *
# from OpenGL.GL import (
#         GL_COMPILE_STATUS, GL_LINK_STATUS, GL_FRAGMENT_SHADER, GL_VERTEX_SHADER,
#         GL_DEPTH_TEST, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_LINES,
#         GL_ARRAY_BUFFER, GL_FLOAT, GL_DYNAMIC_DRAW, GL_TRUE, GL_TRIANGLES,
#         glShaderSource, glCompileShader, glGetShaderiv, glGetShaderInfoLog,
#         glAttachShader, glCreateShader, glDeleteShader, glGetProgramInfoLog,
#         glCreateProgram, glLinkProgram, glGetProgramiv, glUseProgram,
#         glGenVertexArrays, glBindVertexArray, glGenBuffers, glBindBuffer,
#         glClear, glClearColor, glDrawArrays, glEnable, glVertexAttribPointer,
#         glGetAttribLocation, glGetUniformLocation, glBufferData,
#         glEnableVertexAttribArray, glUniformMatrix4fv, glUniform4f,
#         )

def process_shader(program, shader, code): 
    # Set shaders source
    glShaderSource(shader, code)

    # Compile shaders
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(error)
        raise RuntimeError("Error compiling shader")

    # Attach shader objects to the program
    glAttachShader(program, shader)

def build_opengl_program(program):
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
    glUseProgram(program)

def init_opengl():
    program  = glCreateProgram()

    vertex_code = """
            attribute vec3 position;
            uniform mat4 transform;
            void main(){
                gl_Position = transform * vec4(position,1.0);
            }
            """

    fragment_code = """
            uniform vec4 color;
            void main(){
                gl_FragColor = color;
            }
            """

    # fragment shader
    fragment = glCreateShader(GL_FRAGMENT_SHADER)
    process_shader(program, fragment, fragment_code)

    # vertex shader
    vertex = glCreateShader(GL_VERTEX_SHADER)
    process_shader(program, vertex, vertex_code)

    build_opengl_program(program)

    # delete shader object after linking
    glDeleteShader(vertex)
    glDeleteShader(fragment)

    # importante para 3D
    glEnable(GL_DEPTH_TEST) 

    # locations of the varibles in the program
    locations = {
        "position": glGetAttribLocation(program, "position"),
        "color": glGetUniformLocation(program, "color"),
        "transform": glGetUniformLocation(program, "transform")
    }
    return locations

