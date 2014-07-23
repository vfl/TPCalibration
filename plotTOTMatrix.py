from ROOT import  * 


gStyle.SetOptStat(0)



targets = ['CuXRF','TiXRF','VXRF','CrXRF','MnXRF','FeXRF','CoXRF','NiXRF']
targets = ["Am241","Cd109","Fe55"]
cans = []

histos = []
for target in targets : 
    
    can = TCanvas()
    cans.append(can)
    can.SetWindowSize(800,800)

    f = open("results_%s/%s_A06-W0110_totperpixel_0_256_0_256.txt"%(target,target))
    lines = f.readlines()
    hist = TH2D("%s"%target,"%s"%target,256,0,255,256,0,255)



    for line in lines : 
        data=line.split()
        if target == 'Am241' and len(data)>4 :
            x,y,tot=int(data[0]),int(data[1]),float(data[4])
        else :
            x,y,tot=int(data[0]),int(data[1]),float(data[2])            
        hist.Fill(x,y,tot)
    


    hist.Draw("colz")
    histos.append(hist)
    
    hist.SetMinimum(50)
    hist.SetMaximum(1500)
    
    can.SaveAs("%s_map.png"%target)