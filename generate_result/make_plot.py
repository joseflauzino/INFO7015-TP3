#!/usr/bin/python
# coding=UTF-8
import json
import os
import sys
import matplotlib.pyplot as plot
from matplotlib import colors as mcolors

def make_plot(data):
    print "Generating plot"
    durations = [22.54]
    for j in range(1,5):
        scenario = 'scenario%s' % j
        durations.append(data[scenario]['duration'])

    x = [1, 2, 3, 4, 5]
    
    fig = plot.figure()

    axes = plot.subplot(111)
    w = 0.5
    axes.bar(1, 22.54, width=w, edgecolor='White', color='lightskyblue',label="Tempo de Referencia",align="center")
    axes.bar(2, data['scenario1']['duration'], width=w, edgecolor='White', color='cadetblue',label="Com VNF (Chrome)", align="center")
    axes.bar(3, data['scenario2']['duration'], width=w, edgecolor='White', color='lightseagreen',label="Sem VNF (Chrome)", align="center")
    axes.bar(4, data['scenario3']['duration'], width=w, edgecolor='White', color='teal',label="Com VNF (Firefox)",align="center")
    axes.bar(5, data['scenario4']['duration'], width=w, edgecolor='White', color='darkslategrey',label="Sem VNF (Firefox)", align="center")
    for i in range(len(x)):
        axes.text(x[i] - 0.2, durations[i] + 1, truncate(durations[i], 2), fontsize=11, color='darkslategrey')
	
    axes.set_xlabel("Cenarios")
    axes.tick_params(labelbottom=False)
    plot.axis((0,6,0,165))
    axes.set_ylabel("Tempo (em segundos)")
    axes.legend(loc=9,bbox_to_anchor=(0.5,-0.06),ncol=2,fontsize=12)
    #axes.legend(loc="upper right", bbox_to_anchor=(0.5, -0.1), ncol=2)
    # left, bottom, right, top
    plot.tight_layout(rect=[0, 0.15, 1, 1])
    plot.savefig("fig3.png")

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

