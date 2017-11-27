#####-----------#####
#plotAllInDirectory.py - Winnie Wang, Junior standing
#Original code: Refer to test.py --->>> Final working code
#Objective: To plot data without explicitly launching Anaconda
#####-----------#####

#---Packages---#
import sys
import math
import scipy
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
import re #---> 'regular expressions'
import glob, os #used to detect filepath
import ctypes #message boxes

#from pathlib import Path ---->to obtain the home folder in Windows
#home = str(Path.home())

import tkinter as tk
from tkinter import * #'toolkit interface' for GUI
from tkinter import filedialog
import linecache #some package to read number of a line
#---Packages---#

###-----Variables, Arrays-----###
xPlot = [] #x-axis data
yPlot = [] #y-axis data
yPlot2 = [] 
yPlot3 = []

yPlot_all=[]

channel_name=[] #name of each channel; selects the last word of each CH row

current = []
thickness = []
width = []
length = []
gain = []

fig = plt.figure()
axes = fig.add_subplot(111)

colors = ['r--','b--','g--']

x_lst = ['Temp. (K)','Field (T)','Position (theta)', 'Voltage (V)']
y_lst = ['nothing', 'Ch1 x (V)', 'Ch1 y (V)', 'Ch1 R (V)', 'Ch1 theta', 'Ch2 x (V)', 'Ch2 y (V)', 'Ch2 R (V)', 'Ch2 theta', 'Ch3 x (V)', 'Ch3 y (V)', 'Ch3 R (V)', 'Ch3 theta']

###-----Variables, Arrays-----###

###---GUI, Code---###
if __name__ == "__main__": #the instance of 'tk' runs through this loop
    
    ###-----Widget Layout-----###
    root = tk.Tk()
    root.var = tk.StringVar() #x-axis
    root.var2 = tk.StringVar() #ch1
    root.var3 = tk.StringVar() #ch2
    root.var4 = tk.StringVar() #ch3
    root.varCheckbox = tk.IntVar() #for checkbox ch1
    root.varCheckbox2 = tk.IntVar() 
    root.varCheckbox3 = tk.IntVar()
    app_label = tk.Label(root, text='Python_Plotting_App Ver.2.055 running. Please make sure the dimensions are correct.').grid(row=0,column=1)
        
    x_label = tk.Label(root, text="x:").grid(row=1,column=0)#.grid instead of .pack so that we have more freedom to choose where to put widgets  
    x_axis = tk.OptionMenu(root, root.var, *x_lst).grid(row=1,column=1)
   
    y_label = tk.Label(root, text="y1 (Ch1):").grid(row=2,column=0)      
    y_axis = tk.OptionMenu(root, root.var2, *y_lst).grid(row=2,column=1)
    
    y_label2 = tk.Label(root, text="y2 (Ch2):").grid(row=3,column=0)    
    y_axis2 = tk.OptionMenu(root, root.var3, *y_lst).grid(row=3,column=1)
        
    y_label3 = tk.Label(root, text="y3 (Ch3):").grid(row=4,column=0)   
    y_axis3 = tk.OptionMenu(root, root.var4, *y_lst).grid(row=4,column=1)
    
    #temp labels
    resist_bridge_label = tk.Label(root, text='The boxes will eventually have utility implemented.').grid(row=2,column=3)
    resist_bridge_label = tk.Label(root, text='But! You can definitely check them for fun.').grid(row=3,column=3)
    
    resist_bridge = tk.Checkbutton(root, text="Res. Bridge (check if used)", variable=root.varCheckbox).grid(row=1,column=2)
    resist_bridge2 = tk.Checkbutton(root, text="Res. Bridge", variable=root.varCheckbox2).grid(row=2,column=2)
    resist_bridge3 = tk.Checkbutton(root, text="Res. Bridge", variable=root.varCheckbox3).grid(row=3,column=2) #check if res. bridge is used so that data analysis will be changed accordingly
    ###-----Widget Layout-----###
    
    ###-----Functions-----###
    '''
    ###---testing functions---###
    def allstates():
        x_index = x_lst.index(root.var.get())+1
        y_index = y_lst.index(root.var2.get())+4
        y2_index = y_lst.index(root.var3.get())+4
        y3_index = y_lst.index(root.var4.get())+4
        print(x_index, y_index, y2_index, y3_index)
        
    def checking():
        print(root.varCheckbox.get(), root.varCheckbox2.get(), root.varCheckbox3.get())
    ###---testing functions---###
    '''
        
    def plotting(): #keep working on this part for integrating plotting function
        
        #File directory path; de-comment this when ready to try using the right-click on mouse
        filename = sys.argv[1]
        file = open(filename, 'r')
        filedir = filename[0:filename.rfind("\\")]
        os.chdir(filedir)
        
        ''' testing mode
        filename = filedialog.askopenfilename()
        file = open(filename, 'r')
        '''
        
        def file_len(fname): #prints out numbers of lines in file
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
                return i + 1   
        
        file_length = file_len(filename) #number of lines in file

        xplotchoice = x_lst.index(root.var.get())+1 #obtains index from OptionMenu, etc.
        yplotchoice = y_lst.index(root.var2.get())+4
        yplotchoice2 = y_lst.index(root.var3.get())+4
        yplotchoice3 = y_lst.index(root.var4.get())+4
         
        yplotchoices = [yplotchoice, yplotchoice2, yplotchoice3]
        yplotchoices_final = [] #empty list to exclude choices that show "nothing"
        
        #yPlot_all = [] #list where data is appended
        
        for a in range (0, len(yplotchoices)): #for-loop that gets rid of choices that shows "nothing" (or element=4)
            if (yplotchoices[a] != 4):
                yplotchoices_final.append(yplotchoices[a]) #append choices that are != 4 ('nothing')
                yPlot_all.append([]) #yPlot_all appends an empty list
            else:
                pass
            
        parseThrough = len(yPlot_all) #int to implement in for-loops; so that for-loops will only iterate for as long as the yPlot_all array is
            
        for bb in range (2,5): #parses through all channel to obtain their names
            sentence = re.split(' ', linecache.getline(filename, bb))
            channel_name.append(sentence[-1])
            
        for i in range (0, file_length): #iterating through the first 20 lines to find "Timestamp" ---> returns the x-axis, y-axis data and title
            readLine = file.readline()
            if (bool('AM' in readLine) | bool('PM' in readLine)): #finds AM and PM
                s = re.split(r'\t+', readLine)
                xPlot.append(float(re.split('E',s[xplotchoice])[0])*10**float(re.split('E',s[xplotchoice])[1])) #this line split the each string element into 2: one into a number and the other by the exponent (base 10)
                for ii in range (0, parseThrough):
                    yPlot_all[ii].append(float(re.split('E',s[yplotchoices_final[ii]])[0])*10**float(re.split('E',s[yplotchoices_final[ii]])[1]))
            else:
                pass

        ###-----Plotting-----###
        plt.xlabel(x_lst[xplotchoice-1]) #sets x-axis
        plt.ylabel("Voltage (V)") #sets y-axis

        if (xplotchoice==1): #changes plot title based on what the x-axis is
            titleName = "RvT Plot"
        elif (xplotchoice==2):
            titleName= "RvB Plot"
        elif (xplotchoice==4):
            titleName = "RvTheta Plot"
        else:
            pass
            
        for d in range (0, parseThrough): #plots as many channels are appended onto yPlot_all
            axes.plot(xPlot,yPlot_all[d],colors[d], label='SG '+channel_name[d])

        handles, labels = axes.get_legend_handles_labels() #obtains labels on the 'axes'
        axes.legend(handles,labels) #appends legend
        
        plt.title(titleName) #makes title
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) #set axis to sci. notation
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) #set axis to sci. notation

        plt.show()
        ###-----Plotting-----###
                            
        print("It's working! Restart this to plot another.") #print whatever; plotting has no use of this

###-----Functions-----###
        
    plot_button = tk.Button(root, text="Plot", command=plotting) #plotting command button; change command to match function!
    plot_button.grid(row=4,column=2)
    root.mainloop()
    
###---GUI, Code---###