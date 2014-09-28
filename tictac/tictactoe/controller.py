# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 14:19:14 2014

@author: kaiyang
"""

import pyglet
from pyglet.window import mouse
import numpy as np

gap = 30

# pyglet setup
#config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(300,300+gap)
# antialiasing stuff
pyglet.gl.glBlendFunc (pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)                             
pyglet.gl.glEnable (pyglet.gl.GL_BLEND)                                                            
pyglet.gl.glEnable (pyglet.gl.GL_LINE_SMOOTH);                                                     
pyglet.gl.glHint (pyglet.gl.GL_LINE_SMOOTH_HINT, pyglet.gl.GL_DONT_CARE)   
pyglet.gl.glClearColor(1,1,1,1)
pyglet.gl.glLineWidth(3)

main_batch = pyglet.graphics.Batch()
circ_res = 50 # 50 points per circle

title = pyglet.text.Label(text='TicTacToe',
                          x=window.width//2,y=window.height-gap,
                          anchor_x='center',color=(0,0,0,255),
                          anchor_y='bottom',batch=main_batch)
                          

vertex_list = main_batch.add(8, pyglet.gl.GL_LINES, None,
                             ('v2i',(window.width//3,0,
                                     window.width//3,window.height-gap,
                                     2*window.width//3,0,
                                     2*window.width//3,window.height-gap,
                                     0,(window.height-gap)//3,
                                     window.width,(window.height-gap)//3,
                                     0,2*(window.height-gap)//3,
                                     window.width,2*(window.height-gap)//3)),
                             ('c3B',(0,0,0)*8))

vertex_list_circ = None

x_turn = True
won = False
boxes = np.zeros((3,3),dtype=int)

@window.event
def on_draw():
    window.clear()
    
    # draw board    
    main_batch.draw()

count = 0
@window.event
def on_mouse_press(x,y,button,modifiers):
    global x_turn, circ_res, won, main_batch,count, vertex_list, vertex_list_circ
    if button != mouse.LEFT or won: return
    if y > window.height - gap: return    
    x_off = x//(window.width//3)
    y_off = 2-(y//((window.height-gap)//3))
    if boxes[x_off][y_off]: return
    #print x_off, y_off
    if x_turn:
        # draw x
        vertex_list.resize(vertex_list.get_size()+4)
        
        vertex_list.vertices[-8:] = [int((x_off+.1)*(window.width//3)),int((2-y_off+.9)*((window.height-gap)//3)),
                                     int((x_off+.9)*(window.width//3)),int((2-y_off+.1)*((window.height-gap)//3)),
                                     int((x_off+.1)*(window.width//3)),int((2-y_off+.1)*((window.height-gap)//3)),
                                     int((x_off+.9)*(window.width//3)),int((2-y_off+.9)*((window.height-gap)//3))]
                                     
        boxes[x_off][y_off] = 1 # X
        
        #print vertex_list.vertices[-8:]
    else:
        step = np.pi*2/circ_res
        points = [np.array(((x_off+.5)*(window.width//3),(2-y_off+.5)*((window.height-gap)//3))) + np.dot(np.array([[np.cos(step*i),-np.sin(step*i)],[np.sin(step*i),np.cos(step*i)]]),np.array(((window.width//6)-10,0))) for i in xrange(circ_res)]

        if vertex_list_circ is None:
            indices = [[i,(i+1)%circ_res] for i in xrange(circ_res)]
            vertex_list_circ = main_batch.add_indexed(circ_res, pyglet.gl.GL_LINES, None,
                                                      [index for sublist in indices for index in sublist],
                                                      ('v2i',tuple([int(item) for sublist in points for item in sublist])),
                                                      ('c3B',tuple([0]*(circ_res*3))))
        else:
            num_ver = vertex_list_circ.count
            vertex_list_circ.resize(vertex_list_circ.get_size()+circ_res,vertex_list_circ.index_count+(circ_res*2))
            vertex_list_circ.vertices[-(circ_res*2):] = [int(item) for sublist in points for item in sublist]
            vertex_list_circ.colors[-(circ_res*3):] = [0]*(circ_res*3)
            indices = [[i+num_ver,(i+1)%circ_res+num_ver] for i in xrange(circ_res)]
            vertex_list_circ.indices[-(circ_res*2):] = [index for sublist in indices for index in sublist]
        
        #print vertex_list_circ.vertices[:]
        #print vertex_list_circ.colors[:]
        #print vertex_list_circ.indices[:]
        boxes[x_off][y_off] = 2 # O
    
    # column
    for i in range(3):
        if boxes[x_off][i] != 2-x_turn:
            break
        if i == 2:
            won = True
        
    # row
    for i in range(3):
        if boxes[i][y_off] != 2-x_turn:
            break
        if i == 2:
            won = True
            
    # diag
    for i in range(3):
        if boxes[i][i] != 2-x_turn:
            break
        if i == 2:
            won = True
            
    # anti-diag
    for i in range(3):
        if boxes[i][2-i] != 2-x_turn:
            break
        if i == 2:
            won = True
            
    if won:
        if x_turn:
            #print 'X WON!'
            won_text = pyglet.text.Label(text='X Won!',
                                         x = window.width//2, y = (window.height-gap)//2,
                                         anchor_x='center',anchor_y='center',
                                         color=(255,0,0,255),batch=main_batch)
        else:
            #print 'O WON!'
            won_text = pyglet.text.Label(text='O Won!',
                                         x = window.width//2, y = (window.height-gap)//2,
                                         anchor_x='center',anchor_y='center',
                                         color=(0,0,255,255),batch=main_batch)
            
    x_turn = not x_turn
    count = count + 1
    
    if count == 9 and not won:
        won_text = pyglet.text.Label(text='Draw!',
                                         x = window.width//2, y = (window.height-gap)//2,
                                         anchor_x='center',anchor_y='center',
                                         color=(0,255,0,255),batch=main_batch)
    
    

class TicTacToeController:
    def run(self):
        pyglet.app.run()