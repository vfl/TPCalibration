void CLICdpStyle()
{
  gROOT->SetStyle("Plain"); /*Default white background for all plots*/
  /* set bkg color of all to kWhite: white, but not 0*/
  gStyle->SetCanvasColor(kWhite);
  gStyle->SetFrameFillColor(kWhite);
  gStyle->SetStatColor(kWhite);
  gStyle->SetPadColor(kWhite);
  gStyle->SetFillColor(10);
  gStyle->SetTitleFillColor(kWhite);
  
  
   /* SetPaperSize wants width & height in cm: A4 is 20,26 & US is 20,24*/
   gStyle->SetPaperSize(20, 26); 
   /* No yellow border around histogram*/
   gStyle->SetDrawBorder(0);
   /* remove border of canvas*/
   gStyle->SetCanvasBorderMode(0);
   /* remove border of pads*/
   gStyle->SetPadBorderMode(0);
   gStyle->SetFrameBorderMode(0);
   gStyle->SetLegendBorderSize(0);
  
   /* default text size*/
   gStyle->SetTextSize(0.05);
   gStyle->SetTitleSize(0.07,"xyz");
   gStyle->SetLabelSize(0.06,"xyz");
   /* title offset: distance between given text and axis, here x,y,z*/
   gStyle->SetLabelOffset(0.015,"xyz");
   gStyle->SetTitleOffset(1.1,"yz");
   gStyle->SetTitleOffset(1.0,"x");

   /* Use visible font for all text*/
   int font = 42; 
   gStyle->SetTitleFont(font);
   gStyle->SetTitleFontSize(0.06);
   gStyle->SetStatFont(font);
   gStyle->SetStatFontSize(0.07);
   gStyle->SetTextFont(font);
   gStyle->SetLabelFont(font,"xyz");
   gStyle->SetTitleFont(font,"xyz");
   gStyle->SetTitleBorderSize(0);
   gStyle->SetStatBorderSize(1);

   /* big marker points*/
   gStyle->SetMarkerStyle(1);
   gStyle->SetLineWidth(2);  
   gStyle->SetMarkerSize(1.2);
   /*set palette in 2d histogram to nice and colorful one*/
   gStyle->SetPalette(1,0); 

   /*No title for histograms*/
   gStyle->SetOptTitle(0);
   /* show the errors on the stat box */
   gStyle->SetOptStat(0); 
   /* show errors on fitted parameters*/
   gStyle->SetOptFit(0); 
   /* number of decimals used for errors*/
   gStyle->SetEndErrorSize(5);   

   /* set line width to 2 by default so that histograms are visible when printed small
      idea: emphasize the data, not the frame around*/
   gStyle->SetHistLineWidth(2);
   gStyle->SetFrameLineWidth(2);
   gStyle->SetFuncWidth(2);
   gStyle->SetHistLineColor(kBlack);
   gStyle->SetFuncColor(kRed);
   gStyle->SetLabelColor(kBlack,"xyz");

   //set the margins
   gStyle->SetPadBottomMargin(0.18);
   gStyle->SetPadTopMargin(0.08);
   gStyle->SetPadRightMargin(0.08);
   gStyle->SetPadLeftMargin(0.17);
   
   //set the number of divisions to show
   gStyle->SetNdivisions(506, "xy");
   
   //turn off xy grids
   gStyle->SetPadGridX(0);
   gStyle->SetPadGridY(0);
   
   //set the tick mark style
//   gStyle->SetPadTickX(1);
   gStyle->SetPadTickY(1);

   gStyle->SetCanvasDefW(800);
   gStyle->SetCanvasDefH(700);

   gROOT->ForceStyle();
}
/***********************************************************************/
/*                                                                     */
/*       draw legend for 2 histos on the same plot                     */
/*                                                                     */
/***********************************************************************/
void Draw2Legend(TH1 *histo1, 
                 TH1 *histo2,
                 const Char_t *label1, 
                 const Char_t *label2,
                 const Char_t *header="")
{

  Float_t max1 = histo1->GetMaximum();
  Float_t max2 = histo2->GetMaximum();
  if (max1 >= max2) histo1->SetMaximum(max1 * 1.3);
  else histo1->SetMaximum(max2 * 1.3);

  TLegend *legend = new TLegend(0.1436782,0.8072034,0.6408046,0.9851695,NULL,"brNDC");
  legend->SetTextAlign(22);
  legend->SetTextSize(0.1);
  legend->SetTextSize(0.06);
  legend->SetTextFont(42);
  
  TLegendEntry* entry1 = legend->AddEntry(histo1,label1,"LPF");  
  entry1->SetTextColor(histo1->GetLineColor());
  
  TLegendEntry* entry2 = legend->AddEntry(histo2,label2,"LPF");
  entry2->SetTextColor(histo2->GetLineColor());

  if (strncmp(header,"",10))  legend->SetHeader(header);

  legend->SetFillColor(kWhite); 
  legend->Draw();

  gPad->Update();
}

/***********************************************************************/
/*                                                                     */
/*       draw legend for 7 histos on the same plot                     */
/*                                                                     */
/***********************************************************************/
void Draw7Legend(TGraph *histo1, 
                 TGraph *histo2,
                 TGraph *histo3,
                 TGraph *histo4,
                 TGraph *histo5,
                 TGraph *histo6,
                 TGraph *histo7,
		 const Char_t *label1, 
                 const Char_t *label2,
		 const Char_t *label3, 
                 const Char_t *label4,
		 const Char_t *label5, 
                 const Char_t *label6,
		 const Char_t *label7, 
                 const Char_t *header="")
{

  TLegend *legend = new TLegend(0.006231824,0.3648567,0.8683008,0.9190962,NULL,"brNDC");
  legend->SetTextAlign(12);
  legend->SetTextSize(0.1);
  legend->SetTextSize(0.1);
  legend->SetTextFont(42);
  
  TLegendEntry* entry1 = legend->AddEntry(histo1,label1,"L");  
  entry1->SetTextColor(histo1->GetLineColor());
  
  TLegendEntry* entry2 = legend->AddEntry(histo2,label2,"L");
  entry2->SetTextColor(histo2->GetLineColor());

  TLegendEntry* entry3 = legend->AddEntry(histo3,label3,"L");
  entry3->SetTextColor(histo3->GetLineColor());

  TLegendEntry* entry4 = legend->AddEntry(histo4,label4,"L");
  entry4->SetTextColor(histo4->GetLineColor());

  TLegendEntry* entry5 = legend->AddEntry(histo5,label5,"L");
  entry5->SetTextColor(histo5->GetLineColor());

  TLegendEntry* entry6 = legend->AddEntry(histo6,label6,"L");
  entry6->SetTextColor(histo6->GetLineColor());

  TLegendEntry* entry7 = legend->AddEntry(histo7,label7,"L");
  entry7->SetTextColor(histo7->GetLineColor());

//if (header != "") legend->SetHeader(header);
  if (strncmp(header,"",10)) legend->SetHeader(header);

  legend->SetFillColor(kWhite); 
  legend->Draw();

  gPad->Update();
}

/***********************************************************************/
/*                                                                     */
/*       draw statistics boxes for 2 histos                            */
/*       (needs h2->Draw("sames"))                                     */
/*                                                                     */
/***********************************************************************/
bool Draw2StatsBoxes(TH1 *histo1, TH1 *histo2)
{
  /*Get the stats box and set the right colors*/
  TPaveStats *statsh1 =(TPaveStats*) histo1->GetListOfFunctions()->FindObject("stats");
  if (statsh1 == NULL)
    {
      cout<<"\n Could not find statistics box for histo " << histo1->GetName()<<endl;
      return false;
    }
  statsh1->SetLineColor(histo1->GetLineColor());
  statsh1->SetTextColor(histo1->GetLineColor());
  statsh1->SetX1NDC(0.72);
  statsh1->SetY1NDC(0.68);
  statsh1->SetX2NDC(0.92);
  statsh1->SetY2NDC(0.92);

  TPaveStats *statsh2 = (TPaveStats*)histo2->GetListOfFunctions()->FindObject("stats");
  if (statsh2 == NULL)
    {
      cout<<"\n Could not find statistics box for histo " << histo2->GetName()<<endl;
      cout<<"You need to call: histo->Draw(\"sames\")"<<endl;
      return false;
    }
  statsh2->SetLineColor(histo2->GetLineColor());
  statsh2->SetTextColor(histo2->GetLineColor());

  /*need to move the stats box below the previous one, as by default they are stacked*/
  statsh2->SetX1NDC(0.72);
  statsh2->SetY1NDC(0.44);
  statsh2->SetX2NDC(0.92);
  statsh2->SetY2NDC(0.67);
  statsh2->Draw();
  
  return true;
}


