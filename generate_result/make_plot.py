#!/usr/bin/python
import json
import os
import sys
import matplotlib.pyplot as plot
from matplotlib import colors as mcolors

def make_plot(data):

    durations = [40]
    for j in range(1,5):
        scenario = 'scenario%s' % j
        print scenario
        durations.append(data[scenario]['duration'])

    x = [1, 2, 3, 4, 5]
    
    fig = plot.figure(figsize=(8,5))

    axes = fig.add_subplot(111)
    #axes.bar(x, durations, width=0.6, edgecolor='White', alpha=0.6, color='#086A87')
    w = 0.5
    axes.bar(1, 40, width=w, edgecolor='White', color='lightskyblue',label="Tempo de Referencia",align="center")
    axes.bar(2, data['scenario1']['duration'], width=w, edgecolor='White', color='cadetblue',label="Sem NFV (Firefox)", align="center")
    axes.bar(3, data['scenario2']['duration'], width=w, edgecolor='White', color='lightseagreen',label="Sem NFV (Chrome)", align="center")
    axes.bar(4, data['scenario3']['duration'], width=w, edgecolor='White', color='teal',label="Com NFV (Firefox)",align="center")
    axes.bar(5, data['scenario4']['duration'], width=w, edgecolor='White', color='darkslategrey',label="Com NFV (Chrome)", align="center")
    for i in range(len(x)):
        axes.text(x[i] - 0.2, durations[i] + 1, truncate(durations[i], 2), fontsize=11, color='darkslategrey')
	
    axes.set_xlabel("Cenarios")
    axes.tick_params(labelbottom=False)
    plot.axis((0,6,0,100))
    axes.set_ylabel("Tempo (em segundos)")
    axes.legend(loc="upper left", fontsize=11)
    #axes.legend(loc=8, bbox_to_anchor=(0.5, -0.1), fontsize=9)
    plot.savefig("plot_zoom.png")

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

