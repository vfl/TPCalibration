from ROOT import * 
from DataProcessing import * 



#gROOT.LoadMacro('/afs/cern.ch/work/d/dceleste/public/workspace/pyEudetAna/CLICdpStyle/rootstyle/CLICdpStyle.C')
#CLICdpStyle()

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



#A,B,C,T = ReadCalibrationConstants("/VertexScratch/workspace/mbenoit/TB_Calibration_Data/B06-W0125/B06_SinglePixelCalibration/ResultsPixelB06/PixelParametersCorrected_FinalResults_B06.txt")
A,B,C,T = ReadCalibrationConstants("PixelParameters_A06-W0110_noTi_0_256_0_256.txt")


sources=["Fe55","Cd109","Am241"]


# for source in sources[0:1]: 
# 	f=TFile("root_files/%s_clusters_calibrated_A06-W0110.root"%source,"recreate")
# 	Frame,Clusters = ReadFITPIX_File_Calibrated("/afs/cern.ch/work/d/dceleste/public/workspace/pyEudetAna/%s_A06-W0110.txt"%source,A,B,C,T,42)
# 	Frame.Write()
# 	Clusters.Write()
# 	f.Close()


for source in sources: 
	f=TFile("Validation_Calibration_A06-W0110/%s_A06-W0110_24-06-2014_25V_clusters.root"%source,"recreate")
	Frame,Clusters = ReadFITPIX_File_Calibrated("Validation_Calibration_A06-W0110/%s_A06-W0110_24-06-2014_25V"%source,A,B,C,T)
	Frame.Write()
	Clusters.Write()
	f.Close()
