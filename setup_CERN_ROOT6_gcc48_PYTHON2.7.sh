#gcc4.8
source /afs/cern.ch/sw/lcg/external/gcc/4.8/x86_64-slc6/setup.sh


#python2.7.4
export PATH="/afs/cern.ch/sw/lcg/external/Python/2.7.4/x86_64-slc6-gcc48-opt/bin:$PATH"
export LD_LIBRARY_PATH="/afs/cern.ch/sw/lcg/external/Python/2.7.4/x86_64-slc6-gcc48-opt/lib:$LD_LIBRARY_PATH" 

#The /eng/clic/TBData/ location is not acessible by me (z5). The ROOT6 can be used with:
# source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6/setup.sh
# source /afs/cern.ch/sw/lcg/app/releases/ROOT/6.00.02/x86_64-slc6-gcc48-opt/root/bin/thisroot.sh
#But the python libraries cant be found.

#numpy/scipy/sympy

export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/pytools/numpy/lib/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/pytools/scipy/lib/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/pytools/sympy/lib/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/pytools/cython/lib/python2.7/site-packages
export PYTHONPATH=$PYTHONPATH:/afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/pytools/fastcluster/lib/python2.7/site-packages


#root6
source /afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/root/bin/thisroot.sh


#xerces 

export LD_LIBRARY_PATH=/afs/cern.ch/eng/clic/software/Pixel_TestBeam_Software/xerces/lib:$LD_LIBRARY_PATH
source /afs/cern.ch/eng/clic/TBData/software/ROOT6_gcc48_python2.7/geant4/geant4-install/share/Geant4-10.0.2/geant4make/geant4make.sh


