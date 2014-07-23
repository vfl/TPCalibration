import time,os,math,sys
from ROOT import *
from array import array
from math  import sqrt
from numpy import matrix,zeros

# gROOT.LoadMacro('/afs/cern.ch/work/d/dceleste/public/workspace/pyEudetAna/CLICdpStyle/rootstyle/CLICdpStyle.C')
# CLICdpStyle()
##################################################################################################################
#This script has all the *totperpixel.txt files as inputs. Then the range of columns and rows of pixels you want to analyse as arguments.
#It generates the calibration plots for each pixel and a .txt file for each column with the values of a,b,c,t and the threshold (TOT=0)
############################################################################################################################################


def ReadTOTMatrix(filename,npeaks_expected) :

    PeakPerPixel = open(filename,"r")
    lines = PeakPerPixel.readlines()
    
    peakMatrix = [[[0. for i in xrange(256)] for j in xrange(256)] for k in range(npeaks_expected)]
    

    
    
    
    for line in lines:
        data=line.split()
         
        npeaks_found = (len(data) - 2)/2
        
        #print "%i peak found, %i expected"%(npeaks_found,npeaks_expected)
        
         
        X=int(data[0])
        Y=int(data[1])
        if((X>=0 and X<256) and (Y>=0 and Y<256) ):
            if(npeaks_found>npeaks_expected) : 
                 
                peaks = []
                 
                for i in range(npeaks_found) : 
                    peaks.append(float(data[2*i+2]))
                 
                peaks.sort()
                
                #print peaks
                while(len(peaks)>npeaks_expected):
                    peaks.pop(0)
                #print peaks
                for i in range(npeaks_expected) : 
                    peakMatrix[i][X][Y]=peaks[i]
             
            elif(npeaks_found==npeaks_expected) :
                peaks = []
                 
                for i in range(npeaks_found) : 
                    peaks.append(float(data[2*i+2]))
                 
                peaks.sort()
                     
                for i in range(npeaks_expected) :                 
                    peakMatrix[i][X][Y]=peaks[i]
                    
       
             
            else : 
                peaks = [] 
                for i in range(npeaks_found) : 
                    peaks.append(float(data[2*i+2]))
                 
                peaks.sort()
                     
                for i in range(npeaks_found) : 
                    peakMatrix[i][X][Y]=peaks[i]
            
    return peakMatrix
        
#         mean = float(data[2]) 
#         Err  = float(data[3])                     
#         if meanFe>0 and ErrFe<300:
#             tot.append(mean)
#             muerror = Err/mean
#             print muerror
#             enerror = (1/(sqrt(5.899/0.00364)))
#             toterr = 0.00364/(5.899-3.64) + 0.01
#             Err = sqrt(muerror*muerror+enerror*enerror+toterr*toterr)*mean
#             err.append(Err)
#             ene.append(5.899)



def getStart(params):
     a = params[0]
     b = params[1]
     c = params[2]
     t = params[3]

     if (a**2 * t**2 + 2*a*b*t + 4*a*c + b**2) > 0:
         x = ( sqrt(a**2 * t**2 + 2*a*b*t + 4*a*c + b**2) + a*t - b ) / (2*a)
     else:
         x = 0
     return x*0.94
############################################################################################################################################

gStyle.SetOptFit(1)

colMin = int(sys.argv[1])
colMax = int(sys.argv[2])
rowMin = int(sys.argv[3])
rowMax = int(sys.argv[4])


# targets = ['Ti','V','Cr','Mn','Fe','Co','Ni']
# Energies = [[4.51],[4.95],[5.414],[5.89],[6.4],[6.93],[7.47]]

targets = ['VXRF','CrXRF','MnXRF','CoXRF','NiXRF','Cd109','Am241']
Energies = [[4.95],[5.414],[5.89],[6.93],[7.47],[22.9],[26.3,59.5]]



fe55data=ReadTOTMatrix("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_Fe55XRF/Fe55_A06-W0110_totperpixel_0_256_0_256.txt",1)

#print fe55data

dataset = []

for i,source in enumerate(targets) :    
    
    if source in ['bleh'] :
        dataset.append([Energies[i],ReadTOTMatrix("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/peakValue_data/%s_A06-W0110_totperpixel_0_256_0_256.txt"%(source),len(Energies[i]))])
    else:
        dataset.append([Energies[i],ReadTOTMatrix("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_%s/%s_A06-W0110_totperpixel_0_256_0_256.txt"%(source,source),len(Energies[i]))])


#print dataset


Chi2 = TH1D("chi2","chi2",200,0,10)
Threshold = TH1D("th","th",100,0,6)
Fe55Offset = TH1D("off","off",600,-100,500) 

outfile = open("PixelParameters_A06-W0110_noTi_%i_%i_%i_%i.txt"%(colMin,colMax,rowMin,rowMax),"w")
fe55offset_file = open("A06-W0110_Fe55Offset.txt","w")


can = TCanvas()

cnt = 0 
for i in xrange(colMin,colMax):                  

    for j in xrange(rowMin,rowMax):    
        cnt+=1
        
        if(cnt%1==0) : 
            print "event %i"%cnt
            

        tot = []
        ene = []
        errY = []
        errX = []
        for subdataset in dataset:
                        
            for k,point in enumerate(subdataset[1]) :        
                if point[i][j]>0:
                    tot.append(point[i][j])
                   
                    muerror = 0.25
                    enerror = (1/(sqrt(subdataset[0][k]/0.00364)))
                    toterr = 0.00364/(subdataset[0][k]-3.64) + 0.01
                    ErrFe = sqrt(muerror*muerror+enerror*enerror+toterr*toterr)*point[i][j]
                  
                    
                    errX.append(0.001)                   
                    errY.append(0.013*point[i][j]+0.15)
                    
                    
                    ene.append(subdataset[0][k])
                        
 
        

             
         
        #print tot
        #print ene
        try:
            
            isNotGood = True
            while isNotGood:
                goodness = []
                g = TGraphErrors(len(tot),array('f',ene),array('f',tot),array('f',errX),array('f',errY))
                
                surrogate = TF1("surrogate","[0]*x+[1]-([2]/(x-[3]))")#,P_start,60)
                surrogate.SetParName(0,'a')
                surrogate.SetParName(1,'b')
                surrogate.SetParName(2,'c')
                surrogate.SetParName(3,'t')    
                surrogate.SetParameter(0,31)
                surrogate.SetParameter(1,426)
                surrogate.SetParameter(2,477)
                surrogate.SetParameter(3,4)
                #surrogate.SetParLimits(3,-5,4)
                #surrogate.SetParLimits(2,0,2500)            
                #surrogate.SetParameters(P[0],P[1],P[2],P[3])
                g.Fit("surrogate","Q")
                g.GetXaxis().SetTitle("Energy[keV]")
                g.GetYaxis().SetTitle("TOT")
         
                 
                a = surrogate.GetParameter(0)
                b = surrogate.GetParameter(1)
                c = surrogate.GetParameter(2)
                t = surrogate.GetParameter(3)
                
                for k,energy in enumerate(ene) :
                    goodness.append(abs(tot[k]-surrogate.Eval(energy)))
                #print goodness
                #print max(goodness)
                if max(goodness)>100:
                    bad_index = goodness.index(max(goodness))
                    tot.pop(bad_index)
                    ene.pop(bad_index)
                    errX.pop(bad_index)
                    errY.pop(bad_index)
                    isNotGood=True
                else:
                    isNotGood=False
                    
                if (tot[0]>tot[1]):
                    tot.pop(0)
                    ene.pop(0)
                    errX.pop(0)
                    errY.pop(0)
                    isNotGood=True   
            
            #surrogate = TF1("surrogate","[0]*x+[1]+[4]*x*x-([2]/(x-[3]))")#,P_start,60)
            #g.Fit("surrogate","Q")
            #g.GetYaxis().SetRangeUser(0,2000)
            #g.Draw("AP*")
            #can.Print("anmimation.gif+")
            #bla = raw_input()
            #print "Fe55 offset : %f"%(fe55data[0][i][j]-surrogate.Eval(5.9))
            Fe55Offset.Fill((fe55data[0][i][j]-surrogate.Eval(5.9)))
            
            
            try :
                
                th = (t*a-b+sqrt((b+t*a)*(b+t*a)+4*a*c))/(2*a)
            except :
                th=0
            
            #print "Threshold is %f keV"%th
            
            Threshold.Fill(th)
            
            if(surrogate.GetNDF()>0):
                Chi2.Fill(surrogate.GetChisquare()/surrogate.GetNDF())
            
            outfile.write("%i    %i    %f    %f    %f    %f    %f\n"%(i,j,a,b,c,t,th))
    
        except : 
            outfile.write("%i    %i    %f    %f    %f    %f    %f\n"%(i,j,0,0,0,0,0))

can=TCanvas()
Chi2.Draw("")
can2=TCanvas()
Threshold.Draw("")
can3=TCanvas()
Fe55Offset.Draw("")
outfile.close()
