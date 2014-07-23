TPCalibration
=============

Calibration code for Timepix assemblies


Hi guys ! 


So this is the sum of the code  

Here is a short description of the different scripts


CLICdpStyle.C
CLICdp preffered style for plots 

CalibTreeMaker.py
This file read the X Y C txt file produced by pixelman and create a tree with the data 

MatrixTOTAllInOne.py
This script produce text files containing the peak position of each pixek for various sources, take the tree from previous file as input.

GenericPixelParameters.py
This file make the final surrogate fit for each pixel and output a txt file with the ABCD parameters for the surrogate fit

plotCalibratedClusterSpectrum.py
This script apply the calibration to data and produce a calibrated cluster tree 

plotCalibratedSpectrum.py
This script produce calibrated spectrum plots for 3 methods : Global calibration (one surrogate fit for all the pixels together) , pixel-per-pixel calibration and pixel-per-pixel+clustered calibration

DataProcessing.py
This is a library with all the core function for reading and writing trees, clustering, cluster class etc ....

MatrixTOTAllInOne.C
C++ implementation of the script to fill the single pixel spectrum histogram for each pixel for each sources 

CalibrateSpectrum.C
C++ implementation of the algo applying Calibration to the trees, speed-up a lot the code 

plotABCD.py
Short script to inspect and plot parameters of the final calibration files 

plotTOTMatrix.py
plot the TOT peak value for a given source for the matrix 

TotalFitSpectrum.py
plot the global calibration fit + data 

setup_CERN_ROOT6_gcc48_PYTHON2.7.sh
Setup to run the scripts on lxplus 

batch/ 
script to submit the analysis to the batch 




Dataset 

the dataset can be found on lxplus at : 
Fluorescence  -> /afs/cern.ch/work/m/mbenoit/public/LNLS_May2014_Data/16-05-14_MX1_Fluo
Sources (CalibTree root files) -> /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/root_files





 













