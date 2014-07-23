from ROOT import *
from array import array
from math import fsum,sqrt
from scipy.cluster.hierarchy import fclusterdata
from itertools import product
#import pyximport; pyximport.install(pyimport=True)
import fileinput,time
#from scipy.sparse import coo_matrix
from collections import defaultdict

from ROOT import TTree,TFile

class Cluster:

    col = []
    row = []
    tot = []
    sizeX = 0
    sizeY = 0
    size  = 0
    totalTOT =0
    aspectRatio = 0
    hasGlobals = False


    def __init__(self):
        self.sizeX = 0
        self.sizeY = 0
        self.size  = 0
        self.col = []
        self.row = []
        self.tot = []

    def addPixel(self,col,row,tot):
        self.col.append(col)
        self.row.append(row)
        self.tot.append(tot)

    def Statistics(self) :
        self.totalTOT=fsum(self.tot)
        self.size=len(self.col)
        self.sizeX=max(self.col)-min(self.col)+1
        self.sizeY=max(self.row)-min(self.row)+1
        self.aspectRatio=float(self.sizeY)/self.sizeX

    def Print(self):
        for i in range(len(self.col)):
            print "x:%d y%d tot:%.3f"%(self.col[i],self.row[i],self.tot[i])
        print "Cluster Total size = %d , in X = %d Y = %d , Aspect Ratio = %.3f , Total Energy (keV) = %.1f "%(self.size,self.sizeX,self.sizeY,self.aspectRatio,self.totalTOT)



def TOTtoE(TOT,a,b,c,t) :

    try :
        return (t*a + TOT - b +sqrt((b+t*a-TOT)**2 +4*a*c))/(2*a)
    except :
        return 0. 
    

def ReadFITPIX_File(filename) :


    print "Initializing frame tree"
    frameTree = TTree('frames','Timepix frame tree')
    maxn = 256*256
    size=array( 'i', 1*[ 0 ] )
    x = array( 'i', maxn*[ 0 ] )
    y = array( 'i', maxn*[ 0] )
    TOT = array( 'i', maxn*[ 0 ] )

    frameTree.Branch( 'size', size, 'size/I' )
    frameTree.Branch( 'X', x, 'X[size]/I' )
    frameTree.Branch( 'Y', y, 'Y[size]/I' )
    frameTree.Branch( 'TOT', TOT, 'TOT[size]/I' )

    print "Initializing cluster tree"
    clusterTree = TTree('clusters','Timepix cluster tree')

    hasGlobals=array( 'i', 1*[ 0 ] )
    csize=array( 'i', 1*[ 0 ] )   
    csizeX=array( 'i', 1*[ 0 ] )
    csizeY=array( 'i', 1*[ 0 ] )
    cTOT = array( 'f', 1*[ 0. ] )
    cX= array( 'i', 10*[ 0 ] )
    cY= array( 'i', 10*[ 0 ] )
    singleTOT= array( 'f', 10*[ 0. ] )

    clusterTree.Branch( 'csize', csize, 'csize/I' )
    clusterTree.Branch( 'sizeX', csizeX, 'csizeX/I' )
    clusterTree.Branch( 'sizeY', csizeY, 'csizeY/I' )
    clusterTree.Branch( 'totalTOT', cTOT, 'cTOT/F' )
    clusterTree.Branch( 'X', cX, 'cX[csize]/I' )
    clusterTree.Branch( 'Y', cY, 'cY[csize]/I' )
    clusterTree.Branch( 'singleTOT', singleTOT, 'singleTOT[csize]/F' )
    clusterTree.Branch( 'hasGlobals', hasGlobals, 'hasGlobals/I' )   

    #f = open(filename)
    #lines = f.readlines()

    frame = []
    frameCount =0
    last = time.time()
    print "Reading file %s"%filename
    for line in fileinput.input([filename]) :
        if '#' in line :
            frameCount+=1
            if(frameCount==10000):
                break
            if(frameCount%1000==0):
                print "Frame %i, %f s/100 frames"%(frameCount,time.time()-last)
                last =time.time()
                #break
            for i,hit in enumerate(frame) :
                x[i]=hit[0]
                y[i]=hit[1]
                TOT[i]=hit[2]
            size[0] = len(frame)

            clusters = SciPyClustering(x[0:size[0]],y[0:size[0]],TOT[0:size[0]])

            for cluster in clusters :
                cluster.Statistics()
                csize[0]= cluster.size
                csizeX[0]= cluster.sizeX
                csizeY[0]= cluster.sizeY
                cTOT[0]= cluster.totalTOT
                for i,hit in enumerate(cluster.col[0:10]) :
                    cX[i]=cluster.col[i]
                    cY[i]=cluster.row[i]
                    singleTOT[i]=cluster.tot[i]
                clusterTree.Fill()

            frameTree.Fill()

            frame = []
        else :
            data = line.split()
            #print data
            try :
                fX=int(data[0])
                fY=int(data[1])
                fTOT=int(data[2])
                frame.append([fX,fY,fTOT])
            except :
                pass

    return frameTree,clusterTree



def SplitClusters(clusters,splitTh):
    
    newClusters = []

    for cluster in clusters :
        if(cluster.size==2) :
            
            ratio = min(cluster.tot)/max(cluster.tot)

            if(ratio>0.4) :
                c1=Cluster()
                c2=Cluster()
                c1.addPixel(cluster.col[0], cluster.row[0], cluster.tot[0])
                c2.addPixel(cluster.col[0], cluster.row[0], cluster.tot[0])
                c1.Statistics()
                c2.Statistics()
                newClusters.append(c1)
                newClusters.append(c2)
            else :
                newClusters.append(cluster)
        else :
            newClusters.append(cluster)              
    return newClusters
    



def ReadFITPIX_File_Calibrated(filename,A,B,C,T,offset=0,splitTh=7.) :


    print "Initializing frame tree"
    frameTree = TTree('frames','Timepix frame tree')
    maxn = 256*256
    size=array( 'i', 1*[ 0 ] )
    x = array( 'i', maxn*[ 0 ] )
    y = array( 'i', maxn*[ 0] )
    TOT = array( 'i', maxn*[ 0 ] )

    frameTree.Branch( 'size', size, 'size/I' )
    frameTree.Branch( 'X', x, 'X[size]/I' )
    frameTree.Branch( 'Y', y, 'Y[size]/I' )
    frameTree.Branch( 'TOT', TOT, 'TOT[size]/I' )

    print "Initializing cluster tree"
    clusterTree = TTree('clusters','Timepix cluster tree')

    hasGlobals=array( 'i', 1*[ 0 ] )
    csize=array( 'i', 1*[ 0 ] )
    csizeX=array( 'i', 1*[ 0 ] )
    csizeY=array( 'i', 1*[ 0 ] )
    cTOT = array( 'f', 1*[ 0. ] )
    cX= array( 'i', 10*[ 0 ] )
    cY= array( 'i', 10*[ 0 ] )
    singleTOT= array( 'f', 10*[ 0. ] )

    clusterTree.Branch( 'csize', csize, 'csize/I' )
    clusterTree.Branch( 'sizeX', csizeX, 'csizeX/I' )
    clusterTree.Branch( 'sizeY', csizeY, 'csizeY/I' )
    clusterTree.Branch( 'totalTOT', cTOT, 'cTOT/F' )
    clusterTree.Branch( 'X', cX, 'cX[csize]/I' )
    clusterTree.Branch( 'Y', cY, 'cY[csize]/I' )
    clusterTree.Branch( 'singleTOT', singleTOT, 'singleTOT[csize]/I' )
    clusterTree.Branch( 'hasGlobals', hasGlobals, 'hasGlobals/I' )   

    #f = open(filename)
    #lines = f.readlines()

    frame = []
    frameCount =0
    last = time.time()
    print "Reading file %s"%filename
    finput =fileinput.input([filename])
    for line in finput :
        if '#' in line :
            
            
            frameCount+=1
            
            
#             if(frameCount==2000000):
#                 break

            if(frameCount%1000==0):
                print "Frame %i, %f s/1000 frames"%(frameCount,time.time()-last)
                last =time.time()
            
            for i,hit in enumerate(frame) :
                x[i]=hit[0]
                y[i]=hit[1]
                TOT[i]=hit[2]
            size[0] = len(frame)

            clusters = FixedFrameClustering(x[0:size[0]],y[0:size[0]],TOT[0:size[0]])

            for j,cluster in enumerate(clusters) : 
                cluster.Statistics()
                #print cluster.tot,cluster.size
                for i in range(cluster.size) :
                    
                    col=cluster.col[i]
                    row=cluster.row[i]
                  
                    if(A[col][row]==0):
                        a,b,c,t=11.87,423.1,2533,-2.596
                        cluster.hasGlobals=True
                    else :
                        a,b,c,t= A[col][row],B[col][row],C[col][row],T[col][row]     
                    
                    clusters[j].tot[i]=TOTtoE(cluster.tot[i]-offset,a,b,c,t)
            
            #clusters=SplitClusters(clusters,splitTh)
            
            for cluster in clusters :
                cluster.Statistics()
                csize[0]= cluster.size
                csizeX[0]= cluster.sizeX
                csizeY[0]= cluster.sizeY
                cTOT[0]= cluster.totalTOT
                hasGlobals[0]=cluster.hasGlobals

                
                singleTOT= array( 'f', csize[0]*[ 0. ] )
                cX= array( 'i', csize[0]*[ 0 ] )
                cY= array( 'i', csize[0]*[ 0 ] )

                
                for i in range(cluster.size) :
                    if i<10:
                        cX[i]=cluster.col[i]
                        cY[i]=cluster.row[i]
                        singleTOT[i]=cluster.tot[i]


                cTOT[0]= sum(singleTOT)
                
                if cTOT[0]<100. and cTOT[0]>0.:
                    clusterTree.Fill()

            frameTree.Fill()
            frame = []
 
        else :
            data = line.split()
            #print data
            try :
                fX=int(data[0])
                fY=int(data[1])
                fTOT=int(data[2])
                frame.append([fX,fY,fTOT])

            except :
                pass

    finput.close()
    return frameTree,clusterTree



def addNeighbor(cluster,col,row,tot):
    counter =0
    i=0
    j=0
    len_col=len(col)
    len_clu_col=len(cluster.col)
    while(i<len_col):
        j=0
        while(j<len_clu_col):

            if((col[i]-cluster.col[j])**2>1) :
                j+=1
                continue

            if((row[i]-cluster.row[j])**2>1) :
                j+=1
                continue

            cluster.addPixel(col[i],row[i],tot[i])

        #print "[DEBUG] after adding pixel col=%d row=%d to existing cluster as neighbor to x=%d y=%d "%(col[i],row[i],cluster.col[j],cluster.row[j])

            col.pop(i)
            row.pop(i)
            tot.pop(i)
            counter+=1
            i+=-1
            len_col=len(col)
            len_clu_col=len(cluster.col)
            break
        i+=1
    return counter



def RecursiveClustering(row,col,tot) :
    clusters = []
    while(len(row)!=0) :
        cluster = Cluster()
        cluster.addPixel(col[0], row[0], tot[0])
        #print "[DEBUG] adding pixel col=%d row=%d as seed"%(col_tmp[0],row_tmp[0])
        row.pop(0)
        col.pop(0)
        tot.pop(0)
        while(addNeighbor(cluster, col,row, tot)>0):
            pass

        cluster.Statistics()
        clusters.append(cluster)
    return clusters

def SciPyClustering(col,row,tot):

    pixels = [[col[i],row[i]] for i,x in enumerate(col)]
    if(len(pixels)>1):
        result=fclusterdata(pixels,sqrt(2.),criterion="distance")
        clusters=[Cluster() for i in range(max(result))]
        [clusters[x-1].addPixel(col[j],row[j],tot[j]) for j,x in enumerate(result)]
    else:
        if(len(pixels)==1):
            c=Cluster()
            c.addPixel(col[0],row[0],tot[0])
            clusters=[c]

    return clusters


def FixedFrameClustering(X,Y,TOT):

    #frame = [[0 for i in xrange(256)] for j in xrange(256)]
    #totframe = [[0 for i in xrange(256)] for j in xrange(256)]

    def zero():
        return 0

    frame = defaultdict(zero)
    totframe = defaultdict(zero)



    for i,x in enumerate(X) :
        frame[X[i],Y[i]]=-1
        totframe[X[i],Y[i]]=TOT[i]

    cluster_number = 1

    for i,j in [[i,j] for i,j in [[X[i],Y[i]] for i in range(len(X))]] :
        for u,v in [[u,v] for u,v in [[0,1],[1,0],[1,1]] if (((i+u>=0 and i+u<=255) and (j+v>=0 and j+v<=255)) and (u!=0 or v!=0)) ] :
            if(frame[i+u,j+v]==-1) :
                frame[i,j]=cluster_number
                frame[i+u,j+v]=cluster_number
                cluster_number+=1
            elif (frame[i+u,j+v]>0) :
                frame[i,j]= frame[i+u,j+v]

    clusters = {}
#        for i,j in [[i,j] for i,j in product(xrange(256),xrange(256)) if frame[i,j]>0] :

    for i,j in [[X[ind],Y[ind]] for ind in range(len(X))]  :

        try :
            clusters[frame[i,j]].addPixel(i,j,totframe[i,j])
        except KeyError :
            clusters[frame[i,j]]=Cluster()
            clusters[frame[i,j]].addPixel(i,j,totframe[i,j])

    del frame
    del totframe
    #print clusters.ite
    return clusters.values()

#def FixedFrameClustering2(X,Y,TOT):
#
#        frame = [[0 for i in xrange(256)] for j in xrange(256)]
#        totframe = [[0 for i in xrange(256)] for j in xrange(256)]
#        for i,x in enumerate(X) :
#            frame[X[i]][Y[i]]=-1
#            totframe[X[i]][Y[i]]=TOT[i]
#
#        cluster_number = 1
#
#        for i,j in [[i,j] for i,j in product(xrange(256),xrange(256)) if frame[i][j]==-1] :
#            for u,v in [[u,v] for u,v in product([-1,0,1],[-1,0,1]) if (((i+u>=0 and i+u<=255) and (j+v>=0 and j+v<=255)) and (u!=0 or v!=0)) ] :
#                if(frame[i+u][j+v]==-1) :
#                    frame[i][j]=cluster_number
#                    frame[i+u][j+v]=cluster_number
#                    cluster_number+=1
#                elif (frame[i+u][j+v]>0) :
#                    frame[i][j]= frame[i+u][j+v]
#
#        clusters = {}
#        for i,j in [[i,j] for i,j in product(xrange(256),xrange(256)) if frame[i][j]>0] :
#            try :
#                clusters[frame[i][j]].addPixel(i,j,totframe[i][j])
#            except KeyError :
#                clusters[frame[i][j]]=Cluster()
#                clusters[frame[i][j]].addPixel(i,j,totframe[i][j])
#
#        del frame
#        del totframe
#        return clusters.values()

def GetClusters(dataset) :

    AllClusters = []
    for i,frame in enumerate(dataset) :
        if (i%1000==0):
            print "processing event %i"%i
        X = []
        Y = []
        TOT = []
        for hit in frame :
            X.append(hit[0])
            Y.append(hit[1])
            TOT.append(hit[2])
        clusters= RecursiveClustering(X,Y,TOT)
        AllClusters.append( clusters )

    return AllClusters



def MakeTree(dataset) :

    frameTree = TTree('frames','Timepix frame tree')
    maxn = 256*256
    size=array( 'i', 1*[ 0 ] )
    x = array( 'i', maxn*[ 0 ] )
    y = array( 'i', maxn*[ 0] )
    TOT = array( 'i', maxn*[ 0 ] )

    frameTree.Branch( 'size', size, 'size/I' )
    frameTree.Branch( 'X', x, 'X[size]/I' )
    frameTree.Branch( 'Y', y, 'Y[size]/I' )
    frameTree.Branch( 'TOT', TOT, 'TOT[size]/I' )

    for frame in dataset :
        for i,hit in enumerate(frame) :
            x[i]=hit[0]
            y[i]=hit[1]
            TOT[i]=hit[2]
        size[0] = len(frame)
        frameTree.Fill()
    return frameTree



def MakeClusterTree(allClusters) :

    clusterTree = TTree('clusters','Timepix cluster tree')

    size=array( 'i', 1*[ 0 ] )
    sizeX=array( 'i', 1*[ 0 ] )
    sizeY=array( 'i', 1*[ 0 ] )
    TOT = array( 'f', 1*[ 0. ] )

    clusterTree.Branch( 'size', size, 'size/I' )
    clusterTree.Branch( 'sizeX', sizeX, 'sizeX/I' )
    clusterTree.Branch( 'sizeY', sizeY, 'sizeY/I' )
    clusterTree.Branch( 'TOT', TOT, 'TOT/F' )

    for i,clusters in enumerate(allClusters) :
        if(i%1000==0):
            print "processing clusters from event %i"%i
        for cluster in clusters :
            size[0]= cluster.size
            sizeX[0]= cluster.sizeX
            sizeY[0]= cluster.sizeY
            TOT[0]= cluster.totalTOT
            clusterTree.Fill()
    return clusterTree


def MakeTreeFullFrame(dataset) :

    frameTree = TTree('frames','Timepix frame tree')
    maxn = 256*256
    size=array( 'i', 1*[ 0 ] )
    frame = array( 'i', 256*array( 'i', 256*[ 0] ) )

    frameTree.Branch( 'frame', frame, 'frame[256][256]/I' )

    for framedata in dataset :
        frame = array( 'i', 256*array( 'i', 256*[0] ) )
        for i,hit in enumerate(framedata) :
            frame[hit[0]][hit[1]]=hit[2]
        frameTree.Fill()
    return frameTree
