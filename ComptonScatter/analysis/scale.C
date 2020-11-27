#include <iostream>
#include <fstream>
#include <vector>
using namespace std;
void scale(TString filename="../data/std.txt", TString outputFilename="../data/scaleEnergy.png", Int_t skiprow=11,Int_t linesNum=300)
{
    ifstream f(filename);
    vector<int> address(linesNum);
    vector<int> counts(linesNum);
    vector<double> peakIndex;
    vector<double> peak;
    char line[80];
    for(int i=0;i<skiprow;i++){
        f.getline(line, 80);
        //cout<<line<<endl;
    }
    for(int i=0;i<linesNum;i++){
        f>>address[i]>>counts[i];
    }
    for(int i=90;i<linesNum-100;i++){
        if(counts[i]>20&&counts[i]>1.5*counts[i-10]&&counts[i]>counts[i-1]&&counts[i]>counts[i+1]&&counts[i]>counts[i-2]&&counts[i]>counts[i+2]&&counts[i]>counts[i-3]&&counts[i]>counts[i+3]&&counts[i]>counts[i-4]&&counts[i]>counts[i+4]){
            peakIndex.push_back(address[i]);
            peak.push_back(counts[i]);
            cout<<address[i]<<" "<<counts[i]<<endl;
        }
    }
    TCanvas* c1=new TCanvas("c1","energy scale");

    TGraph* gr=new TGraph(linesNum, &address[0],&counts[0]);
    gr->SetTitle("energy spectrum and peak search");
    gr->SetMarkerColor(3);
    gr->SetMarkerStyle(8);
    gr->Draw("ALP");
    gr->GetXaxis()->SetTitle("address");
    gr->GetYaxis()->SetTitle("entries");

    TMarker* peakMarker = nullptr;
    for(int i=0; i<peakIndex.size();i++){
        peakMarker=new TMarker(peakIndex[i],peak[i],23);
        peakMarker->Draw();
    }
    peakMarker->Draw();
    TLegend *legend = new TLegend(0.6,0.65,0.88,0.85);
    legend->SetTextFont(72);
    legend->SetTextSize(0.04);
    legend->AddEntry(gr,"Data","lpe");
    legend->AddEntry(peakMarker,"peak","P");
    legend->Draw();
    c1->Update();
    c1->SaveAs(outputFilename);
    gStyle->SetOptFit(1011);
    TCanvas* c2=new TCanvas("c2","energy scale");
    double energy[] = {0.662,1.1732,1.3325};
    TGraph* gr2=new TGraph(peakIndex.size(), &peakIndex[0], energy);
    gr2->SetTitle("energyscale");
    gr2->SetMarkerColor(3);
    gr2->SetMarkerStyle(8);
    gr2->Draw("AP");
    gr2->GetXaxis()->SetTitle("address");
    gr2->GetYaxis()->SetTitle("enengy/MeV");
    // fit function
    TF1 *f1=new TF1("f1","[1]+[0]*x",0,500);
    f1->SetParameters(0,200);
    f1->SetParLimits(0,0,3000);
    f1->SetParameters(1,10);
    f1->SetParLimits(1,0,2000);
    gr2->Fit("f1","R");

    //gr->SetTitle("use Amplitudet mean");
    gr2->SetTitle("energy Scale");
    
    // draw the legend
    TLegend *legend2 = new TLegend();
    legend2->SetTextFont(72);
    legend2->SetTextSize(0.04);
    legend2->AddEntry(gr2,"Data","p");
    legend2->AddEntry(f1,"fit","l");
    legend2->Draw();
    c2->Update();
    c2->SaveAs("../data/scaleEnergyFit.png");
}
void fitCsv(TString title="epsilon-E", TString filename="../data/epsilon.csv", TString outputPng="../data/epsilon.png"){
    ifstream f(filename);
    vector<double> x;
    vector<double> y;
    double xT,yT;
    string xlabel;
    string ylabel;
    char line[80];
    f.getline(line, 80);
    stringstream ss(line);
    getline(ss,xlabel,',');
    getline(ss,ylabel,',');
    cout<<xlabel<<","<<ylabel<<endl;
    char sep;
    while(1)
    {
        f>>xT>>sep>>yT;
        cout<<xT<<","<<yT<<endl;
        if(!f.good())break;
        x.push_back(xT);
        y.push_back(yT);
    }
    gStyle->SetOptFit(1011);
    TCanvas* c2=new TCanvas("c2","fit");
    TGraph* gr2=new TGraph(x.size(), &x[0], &y[0]);
    gr2->SetTitle(title);
    gr2->SetMarkerColor(3);
    gr2->SetMarkerStyle(8);
    gr2->Draw("AP");
    gr2->GetXaxis()->SetTitle(xlabel.c_str());
    gr2->GetYaxis()->SetTitle(ylabel.c_str());
    // fit function
    TF1 *f1=new TF1("f1","[0]+[1]*x+[2]*x*x+[3]*x*x*x+[4]*x*x*x*x",0,1);
    f1->SetParameters(0,200);
    f1->SetParLimits(0,-300,300);
    f1->SetParameters(1,10);
    f1->SetParLimits(1,0,2000);
    gr2->Fit("f1","R");
    
    // draw the legend
    TLegend *legend2 = new TLegend();
    legend2->SetTextFont(72);
    legend2->SetTextSize(0.04);
    legend2->AddEntry(gr2,"Data","p");
    legend2->AddEntry(f1,"fit","l");
    legend2->Draw();
    c2->Update();
    c2->SaveAs(outputPng);
}
