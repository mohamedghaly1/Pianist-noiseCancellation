# -*- coding: utf-8 -*-
"""
Created on Thu May  4 03:17:34 2023

@author: mido_
"""

import matplotlib.pyplot as plt 
import numpy as np 
import sounddevice as sd 
from scipy.fftpack import fft


t = np.linspace(0, 3, 12 * 1024)

c3 = 130.81
d3 = 146.83
e3 = 164.81
f3 = 174.61
g3 = 196
a3 = 220
b3 = 246.93

c4 = 261.63
d4 = 293.66
e4 = 329.63
f4 = 349.23
g4 = 392
a4 = 440
b4 = 493.88

# play pirates of the caribbean theme song
left_hand = [c3, d3, d3, d3, e3, f3, f3, f3, g3, e3, e3, d3, c3, c3, d3]
right_hand = []
for i in left_hand:
    if i == c3:
        right_hand.append(c4)
    elif i == d3:
        right_hand.append(d4)
    elif i == e3:
        right_hand.append(e4)
    elif i == f3:
        right_hand.append(f4)
    elif i == g3:
        right_hand.append(g4)
    elif i == a3:
        right_hand.append(a4)
    elif i == b3:
        right_hand.append(b4)

starting_time = [i/5 for i in range(len(left_hand))]
how_long = [0.1] * len(left_hand)


#unit step function
def u(t):
    return 1 * (t >= 0)

#add notes to x
x = 0
for note in range(len(left_hand)):
    x += (np.sin(2 * np.pi * left_hand[note] * t) + np.sin(2 * np.pi * right_hand[note] * t)) * (
        u(t - starting_time[note]) - u(t - starting_time[note] - how_long[note]))

#sd.play(x,3*1024)
#plt.plot(t,x)
#plt.show()


#Start of milestone 2
N = 3*1024
f = np. linspace(0 , 512 , int(N/2))

#Fft of original time signal
x_f = fft(x)
x_f = 2/N * np.abs(x_f [0:np.int(N/2)])

#Adding noise to the original signal
fn1, fn2 = np.random.randint(0,512,2)
xn = x + (np.sin(2*np.pi*fn1*t)+np.sin(2*np.pi*fn2*t))

#Fft of noise signal
xn_f = fft(xn)
xn_f = 2/N * np.abs(xn_f [0:np.int(N/2)])

randomFrequencies = []
maxPeak = np.max(x_f)

for i in range (len(xn_f)):
    if(round(xn_f[i])>round(maxPeak)):
        randomFrequencies.append(round(f[i]))

xfiltered = xn - ( np.sin(2*np.pi*t*randomFrequencies[0]) + np.sin(2*np.pi*t*randomFrequencies[1]) )

xfiltered_f = fft(xfiltered)
xfiltered_f = 2/N * np.abs(xfiltered_f [0:np.int(N/2)])

plt.figure(0)
plt.plot(t,x)

plt.figure(1)
plt.subplot(3,1,1)
plt.plot(t,x)
plt.subplot(3,1,2)
plt.plot(t,xn)
plt.subplot(3,1,3)
plt.plot(t,xfiltered)

plt.figure(2)
plt.subplot(3,1,1)
plt.plot(f,x_f)
plt.subplot(3,1,2)
plt.plot(f,xn_f)
plt.subplot(3,1,3)
plt.plot(f,xfiltered_f)

#sd.play(x,3*1024)
sd.play(xfiltered,3*1024)

plt.show()