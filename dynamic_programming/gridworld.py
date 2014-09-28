# -*- coding: utf-8 -*-
"""
Created on Sat Sep 20 16:46:37 2014

@author: kaiyang
"""

import numpy as np
import argparse
import matplotlib.pyplot as plt

np.set_printoptions(precision=2)

parser = argparse.ArgumentParser(description="Gridworld w/ jumps")
parser.add_argument('dimension', metavar='N', type=int, help='dimension of grid', nargs='?', default=20)
parser.add_argument('--jump', dest='jumps_str', action='append', help='append jump to a list of jumps. each jump of form: x1,y1,x2,y2,reward (indexed from 0, starting from top-left)', default=['1,0,1,4,10','3,0,3,2,5'])
parser.add_argument('--rand_jumps', help='generate N random jumps with a reward from min to max. of form N,min,max', nargs='?', default='5,0,20')
parser.add_argument('--thresh', type=float, nargs='?', default=.0001, help='smallest change between max change in V(s) before value iteration ends')
parser.add_argument('--curve', action='store_true', help='plot learning curves')
parser.add_argument('--disc', nargs='?', default=.9)

args = parser.parse_args()
# print args
dim = args.dimension
thresh = args.thresh
disc = args.disc
jumps_str = args.jumps_str
show_curves = args.curve
rand_jumps = args.rand_jumps

print 'parsing jumps...'
jumps = []
for jump in jumps_str:
    params = jump.split(',')
    if len(params) != 5:
        raise StandardError('Invalid jump definition')
    jumps.append({'start':(int(params[0]),int(params[1])),
                  'end':(int(params[2]),int(params[3])),
                  'reward':int(params[4])
                  })

print 'generating random jumps...'
params = rand_jumps.split(',')
num_jumps = int(params[0])
min_reward = int(params[1])
max_reward = int(params[2])

for i in range(num_jumps):
    jumps.append({'start':tuple(np.random.randint(0,dim,2)),
                  'end':tuple(np.random.randint(0,dim,2)),
                  'reward':np.random.randint(min_reward,max_reward+1)})

for jump in jumps:
    print jump

print 'beginning calculation...'
values = np.zeros((dim,dim),dtype=float)
# 0: right 1: down 2: left 3: up
d_V = thresh
changes = []

while d_V >= thresh:
    d_V = 0
    for i in range(dim):
        for j in range(dim):
            v0 = values[i][j]
            found_jump = False
            for jump in jumps:
                if jump['start'] == (i,j):
                    values[i][j] = jump['reward'] + disc * values[jump['end'][0],jump['end'][1]]
                    found_jump = True
                    break
            if found_jump:
                continue
            vals = []

            if i < dim - 1:
                vals.append(disc * values[i+1][j])

            if j > 0:
                vals.append(disc * values[i][j-1])

            if i > 0:
                vals.append(disc * values[i-1][j])

            if j < dim - 1:
                vals.append(disc * values[i][j+1])
                
            values[i][j] = max(vals)
            if np.abs(values[i][j] - v0) > d_V:
                d_V = np.abs(v0 - values[i][j])
    changes.append(d_V)  

print 'determining optimal policy...'
coords = []
policy = []
for i in range(dim):
    for j in range(dim):
        found_jump = False
        for jump in jumps:
            if jump['start'] == (i,j):
                found_jump = True
                break
        if found_jump:
            coords.extend([(i+.5,dim-(j+.5))]*4)
            policy.extend([(.5,0),(0,-.5),(-.5,0),(0,.5)])
            continue
        vals = []

        # Right
        if i < dim - 1:
            vals.append(disc * values[i+1][j])
        else:
            vals.append(0)

        # Down
        if j < dim-1:
            vals.append(disc * values[i][j+1])
        else:
            vals.append(0)

        # Left
        if i > 0:
            vals.append(disc * values[i-1][j])
        else:
            vals.append(0)

        # Up
        if j > 0:
            vals.append(disc * values[i][j-1])
        else:
            vals.append(0)
            
        max_val = max(vals)
        for k in range(len(vals)): # 4
            if vals[k] <= max_val + thresh and vals[k] >= max_val - thresh:
                coords.append((i+.5,dim-(j+.5)))
                policy.append([
                        (.5,0),
                        (0,-.5),
                        (-.5,0),
                        (0,.5)][k])

print 'plotting..'

# plot value function 
# plot optimal policy as vector field

#print np.transpose(values)

plt.figure(0)
plt.plot(changes)

plt.figure(1)
plt.set_cmap('hot')
plt.imshow(np.transpose(values),interpolation='nearest')

X,Y = zip(*coords)
U,V = zip(*policy)
plt.figure(2)
plt.quiver(X,Y,U,V)
plt.axis([0,dim,0,dim])
plt.show()

if show_curves:
    plt.plot(changes)
    plt.show()