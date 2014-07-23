#include "TFile.h"
#include "TTree.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TH1D.h"



double TOTtoE(double TOT,double a,double b,double c,double t) {

double Energy=(t*a + TOT - b +TMath::Sqrt((b+t*a-TOT)*(b+t*a-TOT) +4*a*c))/(2*a);
return Energy;

}


void CalibrateSpectrum(TString filename,double A[256][256],double B[256][256],double C[256][256],double T[256][256],TH1D *histo,double offset=0){

	TFile * file = TFile::Open(filename,"open");

	TTreeReader myReader("pixels", file);

	TTreeReaderValue<Int_t> col(myReader, "col");
	TTreeReaderValue<Int_t> row(myReader, "row");
	TTreeReaderValue<Int_t> tot(myReader, "tot");


	int cnt = 0 ;
	while (myReader.Next()) {
		cnt++;

		if (cnt%1000==0) cout << "Event " << cnt << endl;
		//if (cnt==1000000) break;

		if(A[*col][*row]!=0){
			histo->Fill(TOTtoE(*tot-offset,A[*col][*row],B[*col][*row],C[*col][*row],T[*col][*row]));
		}
		else {
			histo->Fill(TOTtoE(*tot-offset,29.8,534.1,1817,0.7));

		}
	}
}


void CalibrateSpectrumGlobal(TString filename,double A,double B,double C,double T,TH1D *histo,double offset=0){


	TFile * file = TFile::Open(filename,"open");

	TTreeReader myReader("pixels", file);

	TTreeReaderValue<Int_t> col(myReader, "col");
	TTreeReaderValue<Int_t> row(myReader, "row");
	TTreeReaderValue<Int_t> tot(myReader, "tot");


	int cnt = 0 ;
	while (myReader.Next()) {
		cnt++;
		if (cnt%1000==0) cout << "Event " << cnt << endl;
		//if (cnt==1000000) break;

		histo->Fill(TOTtoE(*tot-offset,A,B,C,T));

	}
}





