from ROOT import *
from array import array


f = open("PixelParameters_A06-W0110_newfit3_0_256_0_256.txt","r")



rootfile = TFile("PixelParameters_A06-W0110_0_256_0_256_v2.root","recreate")


rootfile.cd()
tree = TTree("fitPara","fitPara")


a=array( 'f', [ 0. ] )
b=array( 'f', [ 0. ] )
c=array( 'f', [ 0. ] )
d=array( 'f', [ 0. ] )
pixx=array( 'i', [ 0 ] )
pixy=array( 'i', [ 0 ] )


tree.Branch( 'pixx', pixx, 'pixx/I' )
tree.Branch( 'pixy', pixy, 'pixy/I' )
tree.Branch( 'a', a, 'a/F' )
tree.Branch( 'b', b, 'b/F' )
tree.Branch( 'c', c, 'c/F' )
tree.Branch( 'd', d, 'd/F' )


lines = f.readlines()


for line in lines : 
    
    data = line.split()
    
 
    
    pixx[0] = int(data[0])
    pixy[0] = int(data[1])
    
    
    a[0]=float(data[2])
    b[0]=float(data[3])
    c[0]=float(data[4])
    d[0]=float(data[5]) 
    
    print pixx,pixy,a,b,c,d
    
    
    tree.Fill()
tree.Write()

rootfile.Close()   
