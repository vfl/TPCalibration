from ROOT import *



f= open("PixelParameters_A06-W0110_0_256_0_256.txt","r")

lines = f.readlines()

h=TH2D("","",256,0,256,256,0,256)


for line in lines :
	data=line.split()	
	h.Fill(int(data[0]),int(data[1]),float(data[5]))
	
	
h.Draw("colz")
