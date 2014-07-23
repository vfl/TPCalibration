'''
Created on Nov 4, 2013

@author: dcelest
'''
import time,os,math,sys
import numpy as n
from ROOT import *
from array import array
from math  import sqrt
from numpy import matrix
##################################################################################################################
#This script has the *root file as input. Then the range, no. of bins, sigma and threshold as arguments.
#It generates the spectrum of the selected source, fitting the detected peaks.
##################################################################################################################

gStyle.SetOptFit(1)

inputfile = sys.argv[1]
R = int(sys.argv[2])
bin = int(sys.argv[3])
s = int(sys.argv[4])
th = float(sys.argv[5])

x=[]
i=0

rootfile = TFile(inputfile)
treeFe = rootfile.Get("pixels")
treeFe.Draw("tot>>h(%i,0,%i)"%(bin,R),"","goff")

spectrum = TSpectrum()
spectrum.Search(h,s,"",th)
n = spectrum.GetNPeaks()
spectrum.Print("")

for i in xrange(n): 
	x.append(spectrum.GetPositionX()[i])

x.sort()

for i in xrange(n):
	globals()['fitpeak' + str(i)] = TF1("fitpeak%i"%i,"gaus",x[i]-30,x[i]+30)

for i in xrange(n):
	h.Fit("fitpeak%i"%i,"R+")
	



#fun = TF1("fun","gaus",150,280)
#func = TF1("func","gaus",500,660)
#func1 = TF1("func1","gaus",x[1]+100,x[1]-100)
#func2 = TF1("func2","gaus",1150,1400)
#func4 = TF1("func4","gaus",500,660)
#h.Fit("fun","R")
#h.Fit("func1","R")
#h.Fit("func2","R+")
#h.Fit("func4","R+")



	

