#include <iostream>
#include <fstream>
#include <vector>
using namespace std;
void scatterPhoton(TString filename="../data/compton.root", TString outputFilename="../data/scatterPhoton.png")
{
    TFile* f=new TFile(filename);
    TTree* t1=(TTree*)f->Get("compton");
    Int_t entries = t1->GetEntries();
    Double_t energy;
    Int_t theta;
    t1->SetBranchAddress("energy",&energy);
    t1->SetBranchAddress("theta",&theta);
    vector<double> thetas(entries);
    vector<double> energys(entries);
    for(int i=0;i<entries;i++){
        t1->GetEntry(i);
        thetas[i]=theta;
        energys[i]=energy;
        cout<<theta<<" "<<energy<<endl;
    }

    TCanvas* c1=new TCanvas("c1","energy scale");

    TGraph* gr=new TGraph(entries, &thetas[0],&energys[0]);
    gr->SetTitle("energy~theta");
    gr->SetMarkerColor(3);
    gr->SetMarkerStyle(8);
    gr->Draw("AP");
    gr->GetXaxis()->SetTitle("#theta");
    gr->GetYaxis()->SetTitle("energy/MeV");

    gStyle->SetOptFit(1111);
    // fit function
    TF1 *f1=new TF1("f1","1/(1/[0]+(1-cos(x/180*3.14159))/0.511)",15,125);
    f1->SetParameters(0,1);
    f1->SetParLimits(0,0,2);
    gr->Fit("f1","R");
    TF1 *f2=new TF1("f2","1/(1/0.662+(1-cos(x/180*3.14159))/0.511)",15,125);
    f2->SetLineStyle(ELineStyle::kDashed);
    f2->Draw("SAME");
    Double_t chisquareTest = gr->Chisquare(f2);
    cout<<"chisquare test"<<chisquareTest<<endl;
    cout<<"chisquare cdf"<<ROOT::Math::chisquared_cdf(chisquareTest,4)<<endl;
    // draw the legend
    TLegend *legend2 = new TLegend();
    legend2->SetTextFont(72);
    legend2->SetTextSize(0.04);
    legend2->AddEntry(gr,"Data","p");
    legend2->AddEntry(f1,"fit","l");
    legend2->AddEntry(f2,"theory distibution","l");
    legend2->Draw();
    c1->Update();
    c1->SaveAs(outputFilename);
}

void scatterBarn(TString filename="../data/compton.root", TString outputFilename="../data/scatterPBarn.png")
{
    TFile* f=new TFile(filename);
    TTree* t1=(TTree*)f->Get("compton");
    Int_t entries = t1->GetEntries();
    Double_t number;
    Double_t energy;
    Int_t theta;
    t1->SetBranchAddress("number",&number);
    t1->SetBranchAddress("theta",&theta);
    t1->SetBranchAddress("energy", &energy);
    vector<double> thetas(entries);
    vector<double> numbers(entries);
    vector<double> energys(entries);
    for(int i=0;i<entries;i++){
        t1->GetEntry(i);
        thetas[i]=theta;
        numbers[i]=number;
        energys[i]=energy;
        cout<<theta<<" "<<number<<endl;
    }
    TF1 epsilon("epsilon","10.13+17.58*x-117.5*x*x+193.2*x*x*x-101.8*x*x*x*x");
    TF1 R("R","1.023+0.52*x-8.935*x*x+15.65*x*x*x-8.29*x*x*x*x");
    cout<<epsilon.Eval(0.6)<<" "<<R.Eval(0.6)<<endl;
    Double_t Egamma = 0.662;
    Double_t m0c2 = 0.511;
    TF1 crossSectionPart("crossSectionPart","1+[0]*(1-cos(x/180*3.1415926))/[1]",15,125);
    crossSectionPart.SetParameters(Egamma,m0c2);
    //TF1 crossSection("crossSection","(1/crossSectionPart+crossSectionPart+sin(x/180*3.14159)*sin(x/180*3.14159))/crossSectionPart/crossSectionPart",15,125);
    auto crossSection_f=[&](double *x,double*p){Double_t temp = crossSectionPart.Eval(x[0]);return (1/temp+temp+sin(x[0]/180*3.14159)*sin(x[0]/180*3.14159))/temp/temp;};
    TF1* crossSection=new TF1("crossSection",crossSection_f,15,125,0);
    Double_t crossSectionRefer = crossSection->Eval(thetas[2]);
    auto crossSectionR_f=[&](double *x,double*p){return (crossSection->Eval(x[0]))/p[0];};
    TF1 crossSectionR("crossSectionR",crossSectionR_f,15,125,1);
    crossSectionR.SetParameter(0,crossSectionRefer);
    cout<<crossSectionRefer<<" "<<crossSectionR.Eval(60)<<" "<<crossSectionPart.Eval(60)<<endl;
    //caculate the relative value
    Double_t referEpsilon = epsilon.Eval(energys[2]);
    Double_t referR = R.Eval(energys[2]);
    Double_t referN = numbers[2];
    for(int i=0;i<entries;i++){
        numbers[i] = numbers[i]/referN*referEpsilon/epsilon.Eval(energys[i])*referR/(R.Eval(energys[i]));
    }
    TCanvas* c1=new TCanvas("c1","number scale");

    TGraph* gr=new TGraph(entries, &thetas[0],&numbers[0]);
    gr->SetTitle("relativeCrossSection~#theta");
    gr->SetMarkerColor(3);
    gr->SetMarkerStyle(8);
    gr->Draw("AP");
    gr->GetXaxis()->SetTitle("#theta");
    gr->GetYaxis()->SetTitle("relativeCrossSection");

    gStyle->SetOptFit(1111);
    // fit function
    /*
    TF1 *f1=new TF1("f1","1/(1/[1]+(1-cos(x/180*3.14159))/[0])",15,125);
    f1->SetParameters(0,1);
    f1->SetParLimits(0,0,2);
    f1->SetParameters(1,1);
    f1->SetParLimits(1,0,2);
    gr->Fit("f1","R");
    */
    crossSectionR.SetLineStyle(ELineStyle::kDashed);
    crossSectionR.Draw("SAME");
    Double_t chisquareTest = gr->Chisquare(&crossSectionR);
    cout<<"chisquare test"<<chisquareTest<<endl;
    cout<<"chisquare cdf"<<ROOT::Math::chisquared_cdf(chisquareTest,4)<<endl;
    // draw the legend
    TLegend *legend2 = new TLegend();
    legend2->SetTextFont(72);
    legend2->SetTextSize(0.04);
    legend2->AddEntry(gr,"Data","p");
    legend2->AddEntry(&crossSectionR,"theory","l");
    legend2->Draw();
    c1->Update();
    c1->SaveAs(outputFilename);
}