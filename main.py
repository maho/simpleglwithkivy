'''
3D Rotating Monkey Head
========================

This example demonstrates using OpenGL to display a rotating monkey head. This
includes loading a Blender OBJ file, shaders written in OpenGL's Shading
Language (GLSL), and using scheduled callbacks.

The monkey.obj file is an OBJ file output from the Blender free 3D creation
software. The file is text, listing vertices and faces and is loaded
using a class in the file objloader.py. The file simple.glsl is
a simple vertex and fragment shader written in GLSL.
'''
import array

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *


class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        super(Renderer, self).__init__(**kwargs)
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
#            PushMatrix()
#            self.setup_scene()
#            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
        
        #vertices
        buffid, = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffid)
        #buff = "\x00\x80\xA2\x43\x00\x80\xA2\x43\xFF\x00\x00\xFF\x00\x80\xED\x43\x00\x80\xA2\x43\xFF\x00\x00\xFF\x00\x00\xC8\x43\x00\x80\xED\x43\xFF\x00\x00\xFF\x00\x00"\
        #             "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" 
        buff = array.array('f', [
                            50.0, -50.0, 1., 1., 1., 1., 
                            -50.0, -50.0, 1., 1., 1., 1., 
                            0., 50., 1., 1., 1., 1.]).tostring()
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(buff), 
                     buff,
                     GL_STREAM_DRAW)
        #indices
        ibuffid, = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibuffid)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6, 
                "\x00\x00\x01\x00\x02\x00", 
                GL_STREAM_DRAW)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_SHORT, "\x00\x00\x01\x00\x02\x00")
         

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)
        pass

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-200, 200, -200, 200, -100, 100, 0)
        self.canvas['projection_mat'] = proj
        self.canvas['modelviev_mat'] = Matrix()

#    def setup_scene(self):
#        Color(1, 1, 1, 1)
#        PushMatrix()
#        Translate(0, 0, -3)
#        self.rot = Rotate(1, 0, 1, 0)
#        m = list(self.scene.objects.values())[0]
#        UpdateNormalMatrix()
#        self.mesh = Mesh(
#            vertices=m.vertices,
#            indices=m.indices,
#            fmt=m.vertex_format,
#            mode='triangles',
#        )
#        PopMatrix()


class RendererApp(App):
    def build(self):
        return Renderer()


if __name__ == "__main__":
    RendererApp().run()
