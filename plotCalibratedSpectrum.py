from ROOT import * 
from DataProcessing import * 
import numpy


gROOT.LoadMacro('CLICdpStyle.C')
gROOT.LoadMacro("CalibrateSpectrum.C")
CLICdpStyle()


def FindPeaks(histo,exp_range):
	
	p=[]
	spectrum = TSpectrum()
	spectrum.Search(histo,2,"nodraw",0.05) #search peaks 	
	n = spectrum.GetNPeaks()	
	for z in xrange(n): 
		p.append(spectrum.GetPositionX()[z])	  #sort peaks 
	p.sort()
	return p


def GetBackground(histo,niter=12):
	
	spectrum = TSpectrum()
	
	back=spectrum.Background(histo,niter,"goff")

	return back
	



def ReadCalibrationConstants(filename) : 

	A =[[0 for x in range(256)] for x in range(256)]
	B =[[0 for x in range(256)] for x in range(256)]
	C =[[0 for x in range(256)] for x in range(256)]	
	T =[[0 for x in range(256)] for x in range(256)]
	
	
	f = open(filename)	
	lines = f.readlines()
	
	for line in lines : 
		data=line.split()
		x=int(data[0])		
		y=int(data[1])		
		A[x][y]=float(data[2])		
		B[x][y]=float(data[3])		
		C[x][y]=float(data[4])
		T[x][y]=float(data[5])
	
	
	return A,B,C,T


# def TOTtoE(TOT,a,b,c,t) : 
# 
# 	Energy=(t*a + TOT - b +TMath.Sqrt((b+t*a-TOT)**2 +4*a*c))/(2*a)			
# 	return Energy
# 
# 
# 
# def CalibrateSpectrum(filename,A,B,C,T,histo,offset=0) : 
# 	
# 	f=TFile(filename,"open")
# 	#pixels = f.Get("pixels")
# 	
# 	#histo = TH1D("CalibratedSpectrum","",500,0,70)
# 	
# 	reader = TTreeReader("pixels",f)
# 	col = TTreeReaderValue(int)(reader,"col")
# 	row = TTreeReaderValue(int)(reader,"row")
# 	tot = TTreeReaderValue(int)(reader,"tot")
# 	
# 	#print pixels.GetEntries()	
# 	#for i,pixel in enumerate(pixels) : 
# 	i=0
# 	while reader.Next():
# 		i+=1
#  		if(i==100000):
#  			break
# 		if(i%1000)==0 : 
# 			print "event %i"%i
# 		x=int(col)
# 		y=int(row)
# 		TOT=int(tot)-offset
# 		if(A[x][y]!=0):
# 			histo.Fill(TOTtoE(TOT,A[x][y],B[x][y],C[x][y],T[x][y]))
# 		else : 
# 			histo.Fill(TOTtoE(TOT,29.8,534.1,1817,0.7))
# 
# 	#return histo
# 
# def CalibrateSpectrumGlobal(filename,A,B,C,T,histo,offset=0) : 
# 	
# 	f=TFile(filename,"open")
# 	pixels = f.Get("pixels")
# 	
# 	#histo = TH1D("CalibratedSpectrum","",500,0,70)
# 	
# 	print pixels.GetEntries()	
# 	for i,pixel in enumerate(pixels) : 
#  		if(i==100000):
#  			break
# 		if(i%1000)==0 : 
# 			print "event %i"%i	
# 		x=pixel.col
# 		y=pixel.row
# 		TOT=pixel.tot-offset
# 		histo.Fill(TOTtoE(TOT,A,B,C,T))
		
	#return histo


#A,B,C,T = ReadCalibrationConstants("PixelParameters_A06-W0110_0_256_0_256.txt")
Ap,Bp,Cp,Tp = ReadCalibrationConstants("PixelParameters_A06-W0110_newfit3_0_256_0_256.txt")


A=numpy.matrix(Ap)
B=numpy.matrix(Bp)
C=numpy.matrix(Cp)
T=numpy.matrix(Tp)


# pixel-per-pixel
#hCo57 = TH1D("CalibratedSpectrum1","Co57",200,0,20)
hAm241 = TH1D("CalibratedSpectrum2","Am241",200,0,80)
hFe55 = TH1D("CalibratedSpectrum3","Fe55",80,3,9)
hCd109 = TH1D("CalibratedSpectrum4","Cd109",100,0,40)

#CalibrateSpectrum("Co57_B06-W0125_spc.root",A,B,C,T,hCo57)
CalibrateSpectrum("root_files/A06-W0110-25V_Am241_CalibTree.root",A,B,C,T,hAm241)
CalibrateSpectrum("root_files/A06-W0110-25V_Cd109_CalibTree.root",A,B,C,T,hCd109)
CalibrateSpectrum("root_files/A06-W0110-25V_Fe55_CalibTree.root",A,B,C,T,hFe55,42)


#global

#hCo57g = TH1D("CalibratedSpectrum1g","Co57",200,0,20)
hAm241g = TH1D("CalibratedSpectrum2g","Am241",200,0,80)
hFe55g =  TH1D("CalibratedSpectrum3g","Fe55",80,3,9)
hCd109g = TH1D("CalibratedSpectrum4g","Cd109",100,0,40)

Ag=11.87
Bg=423.1
Cg=2533
Tg=-2.596

#CalibrateSpectrumGlobal("Co57_B06-W0125_spc.root",Ag,Bg,Cg,Tg,hCo57g)
CalibrateSpectrumGlobal("root_files/A06-W0110-25V_Am241_CalibTree.root",Ag,Bg,Cg,Tg,hAm241g)
CalibrateSpectrumGlobal("root_files/A06-W0110-25V_Cd109_CalibTree.root",Ag,Bg,Cg,Tg,hCd109g)
CalibrateSpectrumGlobal("root_files/A06-W0110-25V_Fe55_CalibTree.root",Ag,Bg,Cg,Tg,hFe55g,42)


# #pixel per pixel clustered

fAm241 = TFile("root_files/Am241_clusters_calibrated_A06-W0110.root")
tAm241 = fAm241.Get("clusters")
tAm241.Draw("totalTOT >> hAm241clu(200,0,80)","","",1000000000)
hAm241clu=gROOT.FindObject("hAm241clu")
 
 
fFe55 = TFile("root_files/Fe55_clusters_calibrated_A06-W0110.root")
tFe55 = fFe55.Get("clusters")
tFe55.Draw("totalTOT/csize >> hFe55clu(80,3,9)","csize<5","",1000000000)
hFe55clu=gROOT.FindObject("hFe55clu")
 
fCd109 = TFile("root_files/Cd109_clusters_calibrated_A06-W0110.root")
tCd109 = fCd109.Get("clusters")
tCd109.Draw("totalTOT >> hCd109clu(100,0,40)","","",1000000000)
hCd109clu=gROOT.FindObject("hCd109clu")



#pixel per pixel

hAm241.SetLineColor(kRed)
hCd109.SetLineColor(kRed)
hFe55.SetLineColor(kRed)


hAm241.SetLineWidth(2)
hCd109.SetLineWidth(2)
hFe55.SetLineWidth(2)


hAm241.SetFillColor(kRed)
hCd109.SetFillColor(kRed)
hFe55.SetFillColor(kRed)


hAm241.SetFillStyle(3004)
hCd109.SetFillStyle(3004)
hFe55.SetFillStyle(3004)



#global

hAm241g.SetLineColor(kBlue)
hCd109g.SetLineColor(kBlue)
hFe55g.SetLineColor(kBlue)


hAm241g.SetLineWidth(2)
hCd109g.SetLineWidth(2)
hFe55g.SetLineWidth(2)


hAm241g.SetFillColor(4)
hCd109g.SetFillColor(4)
hFe55g.SetFillColor(4)

hAm241g.SetFillStyle(3005)
hCd109g.SetFillStyle(3005)
hFe55g.SetFillStyle(3005)


#clustered
 
hAm241clu.SetLineColor(kMagenta)
hCd109clu.SetLineColor(kMagenta)
hFe55clu.SetLineColor(kMagenta)
 
 
hAm241clu.SetLineWidth(2)
hCd109clu.SetLineWidth(2)
hFe55clu.SetLineWidth(2)
 
 
hAm241clu.SetFillColor(6)
hCd109clu.SetFillColor(6)
hFe55clu.SetFillColor(6)
 
hAm241clu.SetFillStyle(3003)
hCd109clu.SetFillStyle(3003)
hFe55clu.SetFillStyle(3003)



can1=TCanvas()

hAm241back=GetBackground(hAm241)
hAm241.Add(hAm241back,-1)
 
hAm241gback=GetBackground(hAm241g,20)
hAm241g.Add(hAm241gback,-1)
 
hAm241cluback=GetBackground(hAm241clu)
hAm241clu.Add(hAm241cluback,-1)

h1=hAm241.DrawNormalized("")
h1g=hAm241g.DrawNormalized("same")
h1clu=hAm241clu.DrawNormalized("same")

h1.SetTitle("^{241}Am, Single pixel spectrum, pixel-per-pixel calibration")
h1g.SetTitle("^{241}Am, Single pixel spectrum, global calibration")
h1clu.SetTitle("^{241}Am, Cluster spectrum, pixel-per-pixel calibration")



can2=TCanvas()

hCd109back=GetBackground(hCd109)
hCd109.Add(hCd109back,-1)
 
hCd109gback=GetBackground(hCd109g,20)
hCd109g.Add(hCd109gback,-1)
 
hCd109cluback=GetBackground(hCd109clu)
hCd109clu.Add(hCd109cluback,-1)


h2=hCd109.DrawNormalized("")
h2g=hCd109g.DrawNormalized("same")
h2clu=hCd109clu.DrawNormalized("same")

h2.SetTitle("^{109}Cd, Single pixel spectrum, pixel-per-pixel calibration")
h2g.SetTitle("^{109}Cd, Single pixel spectrum, global calibration")
h2clu.SetTitle("^{109}Cd, Cluster spectrum, pixel-per-pixel calibration")

can3=TCanvas()

hFe55back=GetBackground(hFe55)
hFe55.Add(hFe55back,-1)
 
hFe55gback=GetBackground(hFe55g,20)
hFe55g.Add(hFe55gback,-1)
 
hFe55cluback=GetBackground(hFe55clu)
hFe55clu.Add(hFe55cluback,-1)

h3=hFe55.DrawNormalized("")
h3g=hFe55g.DrawNormalized("same")
h3clu=hFe55clu.DrawNormalized("same")

h3.SetTitle("^{55}Fe, Single pixel spectrum, pixel-per-pixel calibration")
h3g.SetTitle("^{55}Fe, Single pixel spectrum, global calibration")
h3clu.SetTitle("^{55}Fe, Cluster spectrum, pixel-per-pixel calibration")

can1.BuildLegend(0.2,0.7,0.9,0.9)
can2.BuildLegend(0.2,0.7,0.9,0.9)
can3.BuildLegend(0.2,0.7,0.9,0.9)



h1.SetMaximum(0.08)
h2.SetMaximum(0.08)
h3.SetMaximum(0.08)


h=[h1,h2,h3]
for histo in h: 
	histo.GetXaxis().SetTitle("Energy [keV]")
	histo.GetYaxis().SetTitle("A.U.")
	histo.GetYaxis().SetTitleOffset(1.2)


Fe=[h3,h3g,h3clu]
Cd109=[h2,h2g,h2clu]
Am241=[h1,h1g,h1clu]



can3.cd()
peaks_Fe = []
sigma_Fe = []
fits_Fe = []

peakfile = open("peaks_fit3.txt","w")
for i,plot in enumerate(Fe) :
	
	p=FindPeaks(plot,[5,7])
	
	sig=1.5
	Range = 3
	center=p[0]
	while(abs(3*sig-2*Range)>0.05):		
		Range=1.5*sig
		func = TF1("func_Fe_%i"%i,"gaus",center-Range,center+Range)
		result=plot.Fit("func_Fe_%i"%i,"RSQ","") 
		sig=func.GetParameter(2)
		center= func.GetParameter(1)
	
	
	peaks_Fe.append(func.GetParameter(1))
	sigma_Fe.append(func.GetParameter(2))
	
	if i==0 :
		func.SetLineColor(kRed+1)
	elif i==1 : 
		func.SetLineColor(kBlue+1)
	else : 
		func.SetLineColor(kMagenta+1)

	
	fits_Fe.append(func)
	func.Draw("same")

print "---- fit results : Fe55 ----"
peakfile.write("---- fit results : Fe55 ----")
for i,peak in enumerate(peaks_Fe) :
	if i==0 :
		print "Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Fe[i].GetParameter(2))
		peakfile.write("Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Fe[i].GetParameter(2)))
	elif i==1 : 
		print "Global calibration, E=%f +- %f"%(peak,fits_Fe[i].GetParameter(2))
		peakfile.write("Global calibration, E=%f +- %f"%(peak,fits_Fe[i].GetParameter(2)))
	else : 
		print "Clustered Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Fe[i].GetParameter(2))
		peakfile.write("Clustered Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Fe[i].GetParameter(2)))




can2.cd()
peaks_Cd109 = []
sigma_Cd109 = []
fits_Cd109 = []
for i,plot in enumerate(Cd109) :
	
	p=FindPeaks(plot,[5,7])
	sig=1.5
	Range = 3
	center=max(p)
	while(abs(3*sig-2*Range)>0.05):		
		Range=1.5*sig
		func = TF1("func_Cd109_%i"%i,"gaus",center-Range,center+Range)
		result=plot.Fit("func_Cd109_%i"%i,"RSQ","") 
		sig=func.GetParameter(2)
		center= func.GetParameter(1)
		
	peaks_Cd109.append(func.GetParameter(1))
	sigma_Cd109.append(func.GetParameter(2))
	
	if i==0 :
		func.SetLineColor(kRed+1)
	elif i==1 : 
		func.SetLineColor(kBlue+1)
	else : 
		func.SetLineColor(kMagenta+1)


	
	fits_Cd109.append(func)
	func.Draw("same")

print "---- fit results : Cd109 ----"
peakfile.write("---- fit results : Cd109 ----")
for i,peak in enumerate(peaks_Cd109) :
	if i==0 :
		print "Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Cd109[i].GetParameter(2))
		peakfile.write("Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Cd109[i].GetParameter(2)))
	elif i==1 : 
		print "Global calibration, E=%f +- %f"%(peak,fits_Cd109[i].GetParameter(2))
		peakfile.write("Global calibration, E=%f +- %f"%(peak,fits_Cd109[i].GetParameter(2)))

	else : 
		print "Clustered Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Cd109[i].GetParameter(2))
		peakfile.write("Clustered Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Cd109[i].GetParameter(2)))





can1.cd()
peaks_Am241 = []
sigma_Am241 = []
fits_Am241 = []
for i,plot in enumerate(Am241) :
	p=FindPeaks(plot,[5,7])
	sig=1.5
	Range = 3
	center=max(p)
	niter=0
	while(abs(3*sig-2*Range)>0.1 and niter<100):		
		Range=1.5*sig
		func = TF1("func_Am241_%i"%i,"gaus",center-Range,center+Range)
		result=plot.Fit("func_Am241_%i"%i,"RSQ","") 
		sig=func.GetParameter(2)
		center= func.GetParameter(1)
		niter+=1
		
	
	peaks_Am241.append(func.GetParameter(1))
	sigma_Am241.append(func.GetParameter(2))
	
	if i==0 :
		func.SetLineColor(kRed+1)
	elif i==1 : 
		func.SetLineColor(kBlue+1)
	else : 
		func.SetLineColor(kMagenta+1)


	
	fits_Am241.append(func)
	func.Draw("same")

print "---- fit results : Am241 ----"
peakfile.write("---- fit results : Am241 ----")
for i,peak in enumerate(peaks_Am241) :
	if i==0 :
		print "Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Am241[i].GetParameter(2))
		peakfile.write("Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Am241[i].GetParameter(2)))

	elif i==1 : 
		print "Global calibration, E=%f +- %f"%(peak,fits_Am241[i].GetParameter(2))
		peakfile.write("Global calibration, E=%f +- %f"%(peak,fits_Am241[i].GetParameter(2)))

	else : 
		print "Clustered Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Am241[i].GetParameter(2))
		peakfile.write("Clustered Pixel per pixel calibration, E=%f +- %f"%(peak,fits_Am241[i].GetParameter(2)))

	

	

can1.SaveAs("Am241_Calibrated.png")
can2.SaveAs("Cd109_Calibrated.png")
can3.SaveAs("Fe55_Calibrated.png")
can1.SaveAs("Am241_Calibrated.root")
can2.SaveAs("Cd109_Calibrated.root")
can3.SaveAs("Fe55_Calibrated.root")
#can4.SaveAs("Co57_Calibrated.png")


plotfile=TFile("spectrums.root","recreate")
plotfile.cd()


for plot in Am241+Fe+Cd109 : 
	plot.Write()
can1.Write()
can2.Write()
can3.Write()


plotfile.Close()
peakfile.close()



