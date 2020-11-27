#include <iostream>
#include <fstream>
#include <vector>
#include "TH1.h"
#include "TCanvas.h"
#include "RooRealVar.h"
#include "RooConstVar.h"
#include "RooPolynomial.h"
#include "RooGaussian.h"
#include "RooArgusBG.h"
#include "RooAddPdf.h"
#include "RooDataHist.h"
#include "RooPlot.h"
#include "RooFit.h"
using namespace RooFit;
using namespace std;

void compton(TString filename="../data/%d.txt", TString outputFilename="../data/%d.png", Int_t skiprow=11,Int_t linesNum=200)
{
    Double_t rm;
    Double_t rs;
    Double_t ra;
    Double_t rb;
    Double_t sigNum;
    Double_t energy;
    Int_t theta;
    TTree* t1 = new TTree("compton","compton");
    t1->Branch("mean",&rm,"mean/D");
    t1->Branch("energy",&energy,"energy/D");
    t1->Branch("sigma",&rs,"sigma/D");
    t1->Branch("number",&sigNum,"number/D");
    t1->Branch("a",&ra,"ra/D");
    t1->Branch("b",&rb,"rb/D");
    t1->Branch("theta",&theta,"theta/I");
    TFile *outFile = TFile::Open("../data/compton.root","RECREATE");
    vector<int> thetas = {20, 40, 60, 80, 100, 120};
    ifstream* f; 
    TH1* dataC;
    vector<int> counts(linesNum);
    char line[80];
    TCanvas* c1;
    RooPlot* xframe;
    for(int j=0;j<thetas.size();j++){
        theta = thetas[j];
        f= new ifstream(Form(filename,theta));
        vector<int> address(linesNum);
        dataC = new TH1D("data",Form("theta %d", theta), linesNum, 0, linesNum);
        for(int i=0;i<skiprow;i++){
            f->getline(line, 80);
            //cout<<line<<endl;
        }
        Int_t sumT =0;
        for(int i=0;i<linesNum;i++){
            (*f)>>address[i]>>counts[i];
            dataC->SetBinContent(i,counts[i]);
            if(i>(87-25)&i<(87+25))sumT+=counts[i];
        }
        Int_t maxIndex = dataC->GetMaximumBin();
        Int_t lowLimit = 0;
        if((maxIndex-15)>0)
            lowLimit=maxIndex-15;
        RooRealVar x("x","x",0,linesNum);
        RooRealVar mean("mean","mean",maxIndex,lowLimit,maxIndex+15);
        RooRealVar sigma("sigma", "sigma",10,0,50);
        RooGaussian sig("sig", "signalPdf",x,mean,sigma);
        RooRealVar a("a","a",0,-100,100);
        RooRealVar b("b","b",0,-100,100);
        RooPolynomial bkg("bkg","bkgPdf",x,RooArgList(a,b));
        RooRealVar nsig("nsig","#signal events",200,0.,10000);
        RooRealVar nbkg("nbkg","#background events",800,0.,10000);
        RooAddPdf model("model","g+a",RooArgList(sig,bkg),RooArgList(nsig,nbkg));
        RooDataHist data("data","dataset with x", x, dataC);
        model.fitTo(data,Range(lowLimit,maxIndex+15));
        rm = mean.getVal();
        rs = sigma.getVal();
        ra = a.getVal();
        rb = b.getVal();
        sigNum = nsig.getVal();
        energy = 0.00697*rm;
        RooAbsReal* intSig = model.createIntegral(x);
        Double_t rn = intSig->getVal();
        cout<<rn<<" "<<sumT<<endl;
        c1=new TCanvas("c1","energy scale");
        xframe = x.frame();
        data.plotOn(xframe);
        model.plotOn(xframe);
        model.plotOn(xframe, Components("bkg"), LineStyle(ELineStyle::kDashed),LineColor(2));
        model.plotOn(xframe, Components("sig"), LineStyle(ELineStyle::kDashed),LineColor(3));
        xframe->Draw();
        xframe->SetTitle(Form("#theta %d",theta));
        t1->Fill();
        c1->Update();
        c1->SaveAs(Form(outputFilename,theta));
        c1->Clear();
    }
    t1->Write();
    outFile->Close();
}