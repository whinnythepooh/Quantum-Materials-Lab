#####-----------#####
#interpolateAll.py - Winnie Wang, Junior standing
#Objective: To interpolate data and print, plot it out
#Completes a coarse interpolation from N_avg; then computes a finer interpolation based from the number of points user inputed
#####-----------#####

#---Packages---#
import sys
import scipy
from scipy import interpolate
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
import re #---> 'regular expressions'
import glob, os #used to detect filepath

import tkinter as tk
from tkinter import * #'toolkit interface' for GUI
from tkinter import filedialog
import linecache #some package to read number of a line
#---Packages---#

###---Variables, Arrays---###
save_path = "interpolated.txt" #---> saves at where the file is being run

xPlot = [] #x-axis data
yPlot = [] #y-axis data ---> only doing one data set

x_lst = ['Temp. (K)','Field (T)','Position (theta)', 'Voltage (V)']
y_lst = ['nothing', 'Ch1 x (V)', 'Ch1 y (V)', 'Ch1 R (V)', 'Ch1 theta', 'Ch2 x (V)', 'Ch2 y (V)', 'Ch2 R (V)', 'Ch2 theta', 'Ch3 x (V)', 'Ch3 y (V)', 'Ch3 R (V)', 'Ch3 theta']
###---Variables, Arrays---###

###---GUI, Code---###
if __name__ == "__main__": #the instance of 'tk' runs through this loop
    
    ###-----Widget Layout-----###
    root = tk.Tk()
    root.var = tk.StringVar() #x-axis
    root.var2 = tk.StringVar() #ch1
    root.varN = tk.DoubleVar() #for entry box; coarse interpolation
    root.varN2 = tk.DoubleVar() #for entry box 2; fine interpolation
    root.varCheckbox = tk.IntVar() #for checkbox ch1
    
    #.grid instead of .pack so that we have more freedom to choose where to put widgets    
    app_label = tk.Label(root, text='InterpolateAll.py Ver1.3 running. ').grid(row=0,column=0)
    app_label2 = tk.Label(root, text='Interpolated data in the folder of the scanned file. (x is first column, y is second column)').grid(row=1,column=0)
    
    x_label = tk.Label(root, text="x-axis:").grid(row=7,column=0)  
    x_axis = tk.OptionMenu(root, root.var, *x_lst).grid(row=7,column=1)
   
    y_label = tk.Label(root, text="y-axis:").grid(row=8,column=0)      
    y_axis = tk.OptionMenu(root, root.var2, *y_lst).grid(row=8,column=1)
    
    avg_number_label = tk.Label(root, text="N_avg for coarse interpolation (box on right): ").grid(row=2,column=0)
    avg_number_label2 = tk.Label(root, text="Determines the # of intervals for coarse interpolation by dividing the number of data points by this number.").grid(row=3,column=0)
    avg_number = tk.Entry(root, bd=2, width=5, textvariable = root.varN).grid(row=2,column=1)
    
    total_number_label = tk.Label(root, text="Total points for fine interpolation (box on right): ").grid(row=4,column=0)
    total_number_label2 = tk.Label(root, text="Determines the total # of intervals that will be in the fine interpolation, based the coarse interpolation data set.").grid(row=5,column=0)
    total_number = tk.Entry(root, bd=2, width=5, textvariable = root.varN2).grid(row=4,column=1)
    
    resist_bridge = tk.Checkbutton(root, text="Res. Bridge (check if used)", variable=root.varCheckbox).grid(row=1,column=3)
    resist_bridge_label = tk.Label(root, text='The box has no utility yet, but it will soon!').grid(row=2,column=3)
    ###-----Widget Layout-----###
    
    ###-----Functions-----###     
    def interpolation(): #keep working on this part for integrating plotting function
        
        #''' File directory path; de-comment this when ready to try using the right-click on mouse
        filename = sys.argv[1]
        file = open(filename, 'r')
        filedir = filename[0:filename.rfind("\\")]
        os.chdir(filedir)
        #'''
        
        ''' testing mode
        filename = filedialog.askopenfilename() #de-comment this for testing purposes; asks to find a file instead
        file = open(filename, 'r')
        '''
        
        def file_len(fname): #prints out numbers of lines in file
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
                return i + 1   
        
        file_length = file_len(filename) #number of lines in file

        xplotchoice = x_lst.index(root.var.get())+1 
        yplotchoice = y_lst.index(root.var2.get())+4
            
        for i in range (0, file_length): #iterating through the first 20 lines to find "Timestamp" ---> returns the x-axis, y-axis data and title
            readLine = file.readline()
            if (bool('AM' in readLine) | bool('PM' in readLine)): #finds AM and PM
                s = re.split(r'\t+', readLine)
                xPlot.append(float(re.split('E',s[xplotchoice])[0])*10**float(re.split('E',s[xplotchoice])[1])) #this line split the each string element into 2: one into a number and the other by the exponent (base 10)
                yPlot.append(float(re.split('E',s[yplotchoice])[0])*10**float(re.split('E',s[yplotchoice])[1])) #this line split the each string element into 2: one into a number and the other by the exponent (base 10)
            else:
                pass
            
        xPlot_array = np.asarray(xPlot) #changes xPlot into np.array
        yPlot_array = np.asarray(yPlot) #changes yPlot into np.array
        
        #interpolation for 1st time; coarse
        coarse_samples = file_length/(root.varN.get()) #number of data points divided by the number typed in box; to decrease interpoaltion accuracy
        xNew = np.linspace(xPlot_array[0], xPlot_array[-1], num=coarse_samples, endpoint=True) #linspace for catered to first and last element of xPlot_array
        f = interp1d(xPlot_array, yPlot_array)
        
        #interpolation for 2nd time; fine
        fine_samples = root.varN2.get()
        xNew2 = np.linspace(xNew[0], xNew[-1], num=fine_samples, endpoint=True)
        f2 = interp1d(xNew, f(xNew))
        
        ###-----Plotting-----###
        plt.xlabel(x_lst[xplotchoice-1]) #sets x-axis
        plt.ylabel("Voltage (V)") #sets y-axis

        if (xplotchoice==1): #changes plot title based on what the x-axis is
            titleName = "Interpolated RvT Plot"
        elif (xplotchoice==2):
            titleName= "Interpolated RvB Plot"
        elif (xplotchoice==4):
            titleName = "Interpolated RvTheta Plot"
        else:
            pass
        
        plt.title(titleName) #makes title
        plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) #set axis to sci. notation
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0)) #set axis to sci. notation
        
        plt.plot(xPlot,yPlot, 'b.') #normal plot (using lists)
        plt.plot(xNew, f(xNew), 'r.') #coarse interpolated data
        plt.plot(xNew2, f2(xNew2), 'g.') #fine interpolated data
        
        plt.legend(['original','coarse interp.','fine interp.'],loc='best') #legend

        plt.show()
        ###-----Plotting-----###
        
        np.savetxt(save_path,np.c_[xNew2,f2(xNew2)]) #prints out interpolated data for Shua
                            
        print("It's working!") #print whatever; plotting has no use of this
        
    ###-----Functions-----###
        
    plot_button = tk.Button(root, text="Run!", command=interpolation) #plotting command button; change command to match function!
    plot_button.grid(row=4,column=3)
    
    root.mainloop()
    
###---GUI, Code---###
