# -*- coding: utf-8 -*-

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

import numpy


class StoneWall():
    def __init__(self):
        # params
        self.win_width = 400
        self.win_height = 400
        self.view = numpy.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])
        self.eye = numpy.array([-0.75, 1.0, 1.5])
        self.eye_up = numpy.array([0.0, 1.0, 0.0])
        self.look_at = numpy.array([0.0, 0.0, -0.15])
        self.texture_id = 0
        self.vertexes = [[-0.5, -0.5, 0], [0.5, -0.5, 0], [0.5, 0.5, 0], [-0.5, 0.5, 0],
                         [-0.5, -0.5, -0.3], [0.5, -0.5, -0.3], [0.5, 0.5, -0.3], [-0.5, 0.5, -0.3]]
        self.tex_coords = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0],
                           [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
        # front - right - back - left - top - bottom
        self.surfaces = [[0, 1, 2, 3], [1, 5, 6, 2], [5, 4, 7, 6], [0, 3, 7, 4],
                         [3, 2, 6, 7], [1, 0, 4, 5]]

    def init(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        # depth test
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        # set texture
        img = Image.open("stone_wall.png")
        # img_data = numpy.array(list(img.get_data()), dtype=numpy.uint8)
        img_data = numpy.asarray(img, dtype=numpy.uint8)

        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1],
                     0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

    def reshape(self, w, h):
        self.win_width = max(1, w)
        self.win_height = max(1, h)
        # set viewport
        glViewport(0, 0, self.win_width, self.win_height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.win_width > self.win_height:
            glOrtho(self.view[0] * self.win_width / self.win_height, self.view[1] * self.win_width / self.win_height,
                      self.view[2], self.view[3],
                      self.view[4], self.view[5])
        else:
            glOrtho(self.view[0], self.view[1],
                      self.view[2] * self.win_height / self.win_width, self.view[3] * self.win_height / self.win_width,
                      self.view[4], self.view[5])

        # set MODELVIEW
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # set camera
        gluLookAt(
            self.eye[0], self.eye[1], self.eye[2],
            self.look_at[0], self.look_at[1], self.look_at[2],
            self.eye_up[0], self.eye_up[1], self.eye_up[2]
        )

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)

        glBegin(GL_QUADS)

        # front
        glNormal3f(0.0, 0.0, 1.0)
        for point in self.surfaces[0]:
            glTexCoord2fv(self.tex_coords[point])
            glVertex3fv(self.vertexes[point])
        # back
        glNormal3f(0.0, 0.0, -1.0)
        for point in self.surfaces[2]:
            glTexCoord2fv(self.tex_coords[point])
            glVertex3fv(self.vertexes[point])
        # right
        glNormal3f(1.0, 0.0, 0.0)
        glTexCoord2f(0.7, 0.0)
        glVertex3fv(self.vertexes[5])
        glTexCoord2f(1.0, 0.0)
        glVertex3fv(self.vertexes[1])
        glTexCoord2f(1.0, 1.0)
        glVertex3fv(self.vertexes[2])
        glTexCoord2f(0.7, 1.0)
        glVertex3fv(self.vertexes[6])
        # left
        glTexCoord2f(0.3, 0)
        glVertex3fv(self.vertexes[4])
        glTexCoord(0.0, 0.0)
        glVertex3fv(self.vertexes[0])
        glTexCoord(0.0, 1.0)
        glVertex3fv(self.vertexes[3])
        glTexCoord(0.3, 1.0)
        glVertex3fv(self.vertexes[7])
        # top
        glTexCoord(0.0, 1.0)
        glVertex3fv(self.vertexes[3])
        glTexCoord(1.0, 1.0)
        glVertex3fv(self.vertexes[2])
        glTexCoord(1.0, 0.7)
        glVertex3fv(self.vertexes[6])
        glTexCoord(0.0, 0.7)
        glVertex3fv(self.vertexes[7])
        # bottom
        glTexCoord(1.0, 0.0)
        glVertex3fv(self.vertexes[1])
        glTexCoord(0.0, 0.0)
        glVertex3fv(self.vertexes[0])
        glTexCoord(0.0, 0.3)
        glVertex3fv(self.vertexes[4])
        glTexCoord(1.0, 0.3)
        glVertex3fv(self.vertexes[5])

        glEnd()
        glFlush()


def main():
    graph = StoneWall()

    glutInit()
    glutInitDisplayMode(GLUT_ALPHA | GLUT_SINGLE | GLUT_DEPTH)
    glutInitWindowSize(400, 400)
    glutInitWindowPosition(200, 200)
    glutCreateWindow("Stone Wall")

    graph.init()
    glutDisplayFunc(graph.draw)
    glutReshapeFunc(graph.reshape)
    glutMainLoop()


if __name__ == '__main__':
    main()
