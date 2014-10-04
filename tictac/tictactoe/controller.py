# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 14:19:14 2014

@author: kaiyang
"""

import pyglet
from pyglet.window import mouse
import numpy as np
from game import TicTacToeGame

class TicTacToeController:
    
    def updateUI(self):
        for x in range(3):
            for y in range(3):  
                if self.game.boxes[x][y] and not self.drawn[x][y]:
                    # draw value
                    if self.game.boxes[x][y] == 1:
                        # draw X
                        self.vertex_list.resize(self.vertex_list.get_size()+4)
                    
                        self.vertex_list.vertices[-8:] = [int((x+.1)*(self.window.width//3)),int((2-y+.9)*((self.window.height-self.gap)//3)),
                                                 int((x+.9)*(self.window.width//3)),int((2-y+.1)*((self.window.height-self.gap)//3)),
                                                 int((x+.1)*(self.window.width//3)),int((2-y+.1)*((self.window.height-self.gap)//3)),
                                                 int((x+.9)*(self.window.width//3)),int((2-y+.9)*((self.window.height-self.gap)//3))]
                    else:
                        # draw O
                        step = np.pi*2/self.circ_res
                        points = [np.array(((x+.5)*(self.window.width//3),(2-y+.5)*((self.window.height-self.gap)//3))) + np.dot(np.array([[np.cos(step*i),-np.sin(step*i)],[np.sin(step*i),np.cos(step*i)]]),np.array(((self.window.width//6)-10,0))) for i in xrange(self.circ_res)]
            
                        if self.vertex_list_circ is None:
                            indices = [[i,(i+1)%self.circ_res] for i in xrange(self.circ_res)]
                            self.vertex_list_circ = self.main_batch.add_indexed(self.circ_res, pyglet.gl.GL_LINES, None,
                                                                  [index for sublist in indices for index in sublist],
                                                                  ('v2i',tuple([int(item) for sublist in points for item in sublist])),
                                                                  ('c3B',tuple([0]*(self.circ_res*3))))
                        else:
                            num_ver = self.vertex_list_circ.count
                            self.vertex_list_circ.resize(self.vertex_list_circ.get_size()+self.circ_res,self.vertex_list_circ.index_count+(self.circ_res*2))
                            self.vertex_list_circ.vertices[-(self.circ_res*2):] = [int(item) for sublist in points for item in sublist]
                            self.vertex_list_circ.colors[-(self.circ_res*3):] = [0]*(self.circ_res*3)
                            indices = [[i+num_ver,(i+1)%self.circ_res+num_ver] for i in xrange(self.circ_res)]
                            self.vertex_list_circ.indices[-(self.circ_res*2):] = [index for sublist in indices for index in sublist]
                    self.drawn[x][y] = True

        if self.game.won:
            if self.game.x_turn:
                #print 'X WON!'
                self.won_text = pyglet.text.Label(text='X Won!',
                                         x = self.window.width//2, y = (self.window.height-self.gap)//2,
                                         anchor_x='center',anchor_y='center',
                                         color=(255,0,0,255),batch=self.main_batch)
            else:
                #print 'O WON!'
                self.won_text = pyglet.text.Label(text='O Won!',
                                         x = self.window.width//2, y = (self.window.height-self.gap)//2,
                                         anchor_x='center',anchor_y='center',
                                         color=(0,0,255,255),batch=self.main_batch)

        if self.game.draw():
            self.won_text = pyglet.text.Label(text='Draw!',
                                         x = self.window.width//2, y = (self.window.height-self.gap)//2,
                                         anchor_x='center',anchor_y='center',
                                         color=(0,255,0,255),batch=self.main_batch)
 

    def __init__(self, mode, td_file):
        self.gap = 30
        self.circ_res = 50
            
        self.game = TicTacToeGame(mode, td_file)
        self.window = pyglet.window.Window(300,300+self.gap)
        
        # pyglet configuration (antialiasing)
        pyglet.gl.glBlendFunc (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)                             
        pyglet.gl.glEnable (pyglet.gl.GL_BLEND)                                                            
        pyglet.gl.glEnable (pyglet.gl.GL_LINE_SMOOTH);                                                     
        pyglet.gl.glHint (pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)   
        pyglet.gl.glClearColor(1,1,1,1)
        pyglet.gl.glLineWidth(3)
        
        self.main_batch = pyglet.graphics.Batch()
        
        self.title = pyglet.text.Label(text='TicTacToe',
                                       x=self.window.width//2,y=self.window.height-self.gap,
                                       anchor_x='center',color=(0,0,0,255),
                                       anchor_y='bottom',batch=self.main_batch)
        
        self.vertex_list = self.main_batch.add(8, pyglet.gl.GL_LINES, None,
          ('v2i',(self.window.width//3,0,
             self.window.width//3,self.window.height-self.gap,
             2*self.window.width//3,0,
             2*self.window.width//3,self.window.height-self.gap,
             0,(self.window.height-self.gap)//3,
             self.window.width,(self.window.height-self.gap)//3,
             0,2*(self.window.height-self.gap)//3,
             self.window.width,2*(self.window.height-self.gap)//3)),
          ('c3B',(0,0,0)*8))

        self.vertex_list_circ = None

        self.window.on_draw = self.on_draw
        self.window.on_mouse_press = self.on_mouse_press
        
        self.drawn = np.zeros((3,3),dtype=bool)

    def on_draw(self):
        self.window.clear()

        # draw board
        self.main_batch.draw()

    def on_mouse_press(self,x,y,button,modifiers):
        if button != mouse.LEFT or self.game.won: return
        if y > self.window.height - self.gap: return

        x_off = x//(self.window.width//3)
        y_off = 2-(y//((self.window.height-self.gap)//3))
    
        self.game.select(x_off, y_off)

        self.updateUI()

    def run(self):
        pyglet.app.run()