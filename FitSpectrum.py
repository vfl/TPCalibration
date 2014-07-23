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



#gROOT.LoadMacro('/afs/cern.ch/work/d/dceleste/public/workspace/pyEudetAna/CLICdpStyle/rootstyle/CLICdpStyle.C')
#CLICdpStyle()

##################################################################################################################
#This script has the *totperpixel.txt as input. Then the range, the no. of bins, the pixel coordinates, the sigma and the threshold are asked as arguments.
#It generates the source spectrum of the selected pixel, trying to fit all detected peaks.
##################################################################################################################

#gStyle.SetOptFit(1)

inputfile = sys.argv[1]
R = int(sys.argv[2])
bin = int(sys.argv[3])
c = int(sys.argv[4])
r = int(sys.argv[5])
s = int(sys.argv[6])
th = float(sys.argv[7])

x=[]
i=0

rootfile = TFile(inputfile)
treeFe = rootfile.Get("pixels")
treeFe.Draw("tot>>Cd109_Pixel_20_130(%i,0,%i)"%(bin,R),"col==%i && row==%i"%(c,r),"goff")

spectrum = TSpectrum()
spectrum.Search(Cd109_Pixel_20_130,s,"",th)
n = spectrum.GetNPeaks()
spectrum.Print("")

for i in xrange(n): 
	x.append(spectrum.GetPositionX()[i])

x.sort()

for i in xrange(n):
	globals()['fitpeak' + str(i)] = TF1("fitpeak%i"%i,"gaus",x[i]-150,x[i]+150)

for i in xrange(n):
	Cd109_Pixel_20_130.Fit("fitpeak%i"%i,"R+")
	
Cd109_Pixel_20_130.GetXaxis().SetTitle("TOT")
Cd109_Pixel_20_130.GetYaxis().SetTitle("# events")

#fun = TF1("fun","gaus",150,280)
#func = TF1("func","gaus",500,660)
#func1 = TF1("func1","gaus",x[1]+100,x[1]-100)
#func2 = TF1("func2","gaus",1150,1400)
#func4 = TF1("func4","gaus",500,660)
#h.Fit("fun","R")
#h.Fit("func1","R")
#h.Fit("func2","R+")
#h.Fit("func4","R+")



	

