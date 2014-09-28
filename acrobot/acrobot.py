import pyglet
#from pyglet.window import key
#from pyglet.window import mouse
import numpy as np

# pyglet setup
window = pyglet.window.Window(800,600)
main_batch = pyglet.graphics.Batch()

# physical variables
omega1 = 0.0
omega2 = 0.0
length1 = 100 # pixels. also 1 meter => I = 1
length2 = 100
tau = 0

d1 = d2 = phi2 = phi1 = alph2 = alph1 = 0
g = 9.81
thet1 = np.pi/2
thet2 = np.pi/2

end1 = np.array((0,-length1))
end2 = np.array((0,-length2))
anchor = np.array((window.width//2,window.height-length1-length2-75))

title = pyglet.text.Label(text='Acrobot',
                          x=window.width//2,y=window.height-10,
                          anchor_x='center',
                          anchor_y='top',batch=main_batch)

def update(dt):
    global end1,end2,tau,omega1,omega2,alph1,alph2,d1,d2,phi2,phi1,g,thet1,thet2
    
    d1 = 3.5 + np.cos(thet2)
    d2 = 1.25 + .5*np.cos(thet2)
    phi2 = g*np.cos(thet1+thet2-(np.pi/2.0))
    phi1 = -.5*omega2*omega2*np.sin(thet2) - omega2*omega1*np.sin(thet2) + 1.5*g*np.cos(thet1-(np.pi/2.0)) + phi2
    alph2 = (tau + (d2/d1)*phi1 - .5*omega1*omega1*np.sin(thet2)-phi2)/(1.25 - ((d2*d2)/d1))
    alph1 = -(d2*alph2 + phi1)/d1    
    
    omega1 = omega1 + alph1*dt
    omega2 = omega2 + alph2*dt    
    thet1 = thet1 + omega1*dt
    thet2 = thet2 + omega2*dt
    
    end1 = np.dot(np.array([[np.cos(thet1),-np.sin(thet1)],[np.sin(thet1),np.cos(thet1)]]),np.array((0,-length1)))
    end2 = np.dot(np.array([[np.cos(thet2+thet1),-np.sin(thet2+thet1)],[np.sin(thet2+thet1),np.cos(thet2+thet1)]]),np.array((0,-length2)))

@window.event
def on_draw():
    window.clear()
    
    main_batch.draw()
    pyglet.graphics.draw_indexed(3,pyglet.gl.GL_LINES,
                                 [0,1,1,2],
                                 ('v2i',tuple(anchor)+
                                        tuple((anchor+end1).astype(int))+
                                        tuple((anchor+end1+end2).astype(int))))
    
    
if __name__ == '__main__':
    pyglet.clock.schedule_interval(update,1/120.0)
    pyglet.app.run()