#!/bin/bash

#BSUB -J FitPixelNew[1-3]
#BSUB -q 8nh
#BSUB -o /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_CuXRF/jobs/out.%J_%I
#BSUB -e /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/results_CuXRF/jobs/err.%J_%I
#BSUB -R "type==SLC6_64"

#for LSB_JOBINDEX in {1..3}
#do
XMIN=$(( $LSB_JOBINDEX - 1 ))
#echo $XMIN
#done



# source environment
. /afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/setup_CERN_ROOT6_gcc48_PYTHON2.7.sh

# get program and input root file
cp /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/MatrixTOTAllInOne.py .
cp /afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/MatrixTOTAllInOne.C .

# execute script
python MatrixTOTAllInOne.py 0 256 0 256 $XMIN
