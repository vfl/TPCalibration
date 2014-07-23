#include "TFile.h"
#include "TTree.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TH1D.h"




void FillHistos(TFile *file,TString outfile){


	TH1D *histos[256][256];
	for(int i=0;i<256;i++){
	 	  for(int j=0;j<256;j++){
	 		 TString name = TString::Format("%i %i",i,j);
	 		 histos[i][j] = new TH1D(name,name,80,0,1600);
	 	  };
	};

//	for (int i=0;i<256;i++){
//		for (int j=0;j<256;j++){
//			TString name = TString::Format("%i %i",i,j);
//			histos[i][j] =  TH1D(name,name,70,0,800);
//		};
//	};

	TTreeReader myReader("pixels", file);

	TTreeReaderValue<Int_t> col(myReader, "col");
	TTreeReaderValue<Int_t> row(myReader, "row");
	TTreeReaderValue<Int_t> tot(myReader, "tot");


	int cnt = 0 ;
	while (myReader.Next()) {
		cnt++;


		histos[*col][*row]->Fill(*tot);


		if(cnt%100000==0){
			cout << "event " << cnt << endl;
		}
	};

	TFile *out_rootfile = new TFile(outfile,"recreate");
	for (int i=0;i<256;i++){
		for (int j=0;j<256;j++){
			TString name = TString::Format("%i %i",i,j);
			histos[i][j]->Write();
		};
	};
	out_rootfile->Close();

}



void MatrixTOTAllInOne(){

	TFile *file=TFile::Open("/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/root_files/temp/A06-W0110-25V_VXRF_CalibTree.root");
	FillHistos(file,"/afs/cern.ch/work/m/mbenoit/public/LNLS_Analysis/SinglePixelAnalysis/root_files/temp/A06-W0110-25V_VXRF_histos.root");

}



