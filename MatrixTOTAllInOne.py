'''
Created on Nov 4, 2013

@author: dcelest
'''
import time,os,math,sys
from ROOT import *
gROOT.LoadMacro("MatrixTOTAllInOne.C")
##################################################################################################################
#This script has the *root file as input. Then the range of columns and rows of pixels you want to analyse as arguments.
#It generates a *totperpixel.txt and *totperpixelFailedFit.txt files with tot and sigma values per pixel for the selected source.
##################################################################################################################

colMin = int(sys.argv[1])
colMax = int(sys.argv[2])
rowMin = int(sys.argv[3])
rowMax = int(sys.argv[4])
sourcenumber = int(sys.argv[5]) 


#targets = ['TiXRF','VXRF','CrXRF','MnXRF','FeXRF','CoXRF','NiXRF']
targets = ["Am241","Cd109","Fe55"]
source = targets[sourcenumber]

print "processing : " + source

#open file .root and get tree
rootfile = TFile("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/root_files/A06-W0110-25V_%s_CalibTree.root"%source)	
#FillHistos(rootfile,"/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/root_files/A06-W0110-25V_%s_histos.root"%source);


#create file with TOT avarage per pixel 
os.system("mkdir /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_%sXRF"%source)
outfile = open("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_%sXRF/%s_A06-W0110_totperpixel_%i_%i_%i_%i.txt"%(source,source,colMin,colMax,rowMin,rowMax),"w")
#create file with failed pixels 
outfile1 = open("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_%sXRF/%s_A06-W0110_totperpixelFailedFit_%i_%i_%i_%i.txt"%(source,source,colMin,colMax,rowMin,rowMax),"w")

	
i=0
j=0
k=0
l=0
z=0
w=0

X=[]
Y=[]
TOT=[]
ERR=[]





histo_file = TFile("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/root_files/A06-W0110-25V_%s_histos.root"%source,"open")
histos =[[histo_file.Get("%i %i"%(i,j)) for i in xrange(256)] for j in xrange(256)]
# histos =[[TH1D("%i %i"%(i,j),"%i %i"%(i,j),70,0,800) for i in xrange(256)] for j in xrange(256)]
# #tree = rootfile.Get("pixels")
# 
# 
# reader = TTreeReader("pixels",rootfile)
# 
# col = TTreeReaderValue(int)(reader,"col") 
# row = TTreeReaderValue(int)(reader,"row") 
# tot = TTreeReaderValue(int)(reader,"tot") 


#cnt = 0

# while (reader.Next()) :
# #for event in tree : 
# 	i = int(col)
# 	j = int(row)
# 	histos[i][j].Fill(int(tot))
# 	
# 	cnt+=1
# 	if cnt%100000==0:
# 		print "event %i "%cnt
# 	if cnt==5000000 : 
# 		break

for i in xrange(colMin,colMax):                  #select column
	for j in xrange(rowMin,rowMax):          #select row 
		print "col: %i && row: %i"%(i,j) #draw spectrum per pixel
		p=[]
		X.append(i)
		Y.append(j)
		#tree = rootfile.Get("pixels")
		#tree.Draw("tot>>h%i(70,0,800)"%(k),"col==%i && row==%i"%(i,j),"")
		
		#histos[i][j].Draw("")
		
		
		spectrum = TSpectrum()
  		#spectrum.Search(globals()['h' + str(k)],2,"",0.5) #search peaks 	
		spectrum.Search(histos[i][j],2,"",0.3) #search peaks 	
		
		#a= raw_input()
		
		n = spectrum.GetNPeaks()	
		for z in xrange(n): 
			p.append(spectrum.GetPositionX()[z])	  #sort peaks 
		p.sort()
		z=0
		for z in xrange(n):				  #fit peaks and record mean values
			globals()['fitpeak' + str(z)] = TF1("fitpeak%i"%z,"gaus",p[z]-100,p[z]+100)
			histos[i][j].Fit("fitpeak%i"%z,"QR+")		             
			pixelmean =globals()['fitpeak' + str(z)].GetParameter(1)
			pixelerr = globals()['fitpeak' + str(z)].GetParameter(0)			
			TOT.append(pixelmean)
			#TOT.append(p[z])
			
			ERR.append(pixelerr)
		#print TOT
		a=w
		outfile.write("%i	%i	"%(X[l],Y[j]))    #write file with TOT values per pixel
		if n==0:					  #write 0.0 if masked
			outfile.write("0.0	0.0	0.0	0.0")
		elif n==2 or n==1:		
			for a in range(w,w+n):
				outfile.write("%f	%f	"%(TOT[a],ERR[a])) #write TOT and ERR values if number of found peaks as expected
		else:
			outfile1.write("%i	%i	"%(X[l],Y[j]))
			for a in range(w,w+n):					   #write in a new file pixel coordinates (X,Y), TOT and ERR values if fit fails
				outfile.write("%f	%f	"%(TOT[a],ERR[a]))
				outfile1.write("%f	%f	"%(TOT[a],ERR[a]))
			outfile1.write("\n") 
		outfile.write("\n")
		w+=n
		k+=1		
		l+=1
			
outfile1.close()
outfile.close()
histo_file.Close()




