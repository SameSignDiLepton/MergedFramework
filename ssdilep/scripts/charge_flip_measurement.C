#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "TRandom2.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "TF1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "Fit/ParameterSettings.h"
#include "TH2.h"
#include "TLegend.h"
#include "TText.h"
#include "./atlasstyle-00-03-05/AtlasStyle.h"
#include "./atlasstyle-00-03-05/AtlasLabels.h"
#include "./atlasstyle-00-03-05/AtlasUtils.h"

#include "./NumericalMinimizer.h"

#include <iostream>


//*****************************  Charge flip measurment macro   *****************************'


void charge_flip_measurement(){



  //****   Defining root file path    *******
  //std::string file_path_data = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_data.root";
  std::string file_path_data = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_data_exot19.root";
  
  
  std::string file_path_mc = "/afs/cern.ch/user/s/sarnling/MergedFramework/test/ntuple_mc.root";
  
    
  std::string OSCenterInputFile = file_path_data;
  std::string OSSidebandInputFile = file_path_data;
  std::string SSCenterInputFile = file_path_data;
  std::string SSSidebandInputFile = file_path_data;
  
  std::string OSCenterInputFileMC = file_path_mc;
  std::string OSSidebandInputFileMC = file_path_mc;
  std::string SSCenterInputFileMC = file_path_mc;
  std::string SSSidebandInputFileMC = file_path_mc;
  
  TFile* OSCenterFile   = new TFile(OSCenterInputFile.c_str());
  TFile* OSSidebandFile = new TFile(OSSidebandInputFile.c_str());
  TFile* SSCenterFile   = new TFile(SSCenterInputFile.c_str());
  TFile* SSSidebandFile = new TFile(SSSidebandInputFile.c_str());
  
  TFile* OSCenterFileMC   = new TFile(OSCenterInputFileMC.c_str());
  TFile* OSSidebandFileMC = new TFile(OSSidebandInputFileMC.c_str());
  TFile* SSCenterFileMC   = new TFile(SSCenterInputFileMC.c_str());
  TFile* SSSidebandFileMC = new TFile(SSSidebandInputFileMC.c_str());
  
  
    
  //****   Associating input histograms to macro objects    *******

  TH1F* hOSCenterData = (TH1F*) OSCenterFile->Get("/regions/ZWindowAS/ZMassWindowAS/event/h_electrons_chargeflip");
  TH1F* hOSCenterMC   = (TH1F*) OSCenterFileMC->Get("/regions/ZWindowAS/ZMassWindowAS/event/h_electrons_chargeflip");
  
  TH1F* hSSCenterData = (TH1F*) SSCenterFile->Get("/regions/ZWindowSS/TwoSSElectrons_ZMassWindowSS/event/h_electrons_chargeflip");
  TH1F* hSSCenterMC   = (TH1F*) SSCenterFileMC->Get("/regions/ZWindowSS/TwoSSElectrons_ZMassWindowSS/event/h_electrons_chargeflip");
  
  TH1F* hOSSidebandData = (TH1F*) OSSidebandFile->Get("/regions/ZWindowAS-Sideband/ZMassWindowASSideband/event/h_electrons_chargeflip");
  TH1F* hOSSidebandMC   = (TH1F*) OSSidebandFileMC->Get("/regions/ZWindowAS-Sideband/ZMassWindowASSideband/event/h_electrons_chargeflip");
  
  TH1F* hSSSidebandData = (TH1F*) SSSidebandFile->Get("/regions/ZWindowSS-Sideband/TwoSSElectrons_ZMassWindowSSSideband/event/h_electrons_chargeflip");
  TH1F* hSSSidebandMC   = (TH1F*) SSSidebandFileMC->Get("/regions/ZWindowSS-Sideband/TwoSSElectrons_ZMassWindowSSSideband/event/h_electrons_chargeflip");




//**********   Write out if the chargeflip histograms are found in the histogram files    ******************************

  if(hOSCenterData) std::cout << "h_ZWindowOS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_data not found" <<std::endl;
  if(hOSCenterMC) std::cout << "h_ZWindowOS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_Zee not found" <<std::endl;
  
  if(hSSCenterData) std::cout << "h_ZWindowSS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_data not found" <<std::endl;
  if(hSSCenterMC) std::cout << "h_ZWindowSS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_Zee not found" <<std::endl;
  
  if(hOSSidebandData) std::cout << "h_ZWindowOS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_data not found" <<std::endl;
  if(hOSSidebandMC) std::cout << "h_ZWindowOS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_Zee not found" <<std::endl;
  
  if(hSSSidebandData) std::cout << "h_ZWindowSS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_data not found" <<std::endl;
  if(hSSSidebandMC) std::cout << "h_ZWindowSS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_Zee not found" <<std::endl;



//********    Start the charge flip measurment plot proction    *************************************

  std::cout << " Data charge-flip measurement " << std::endl;
  
  NumericalMinimizer* NM1 = new NumericalMinimizer(hOSCenterData,hSSCenterData,hOSSidebandData,hSSSidebandData,1.1*1e6); //Here the actual likliehood minimization is done 
  
  std::cout << " MC charge-flip measurement " << std::endl;
  NumericalMinimizer* NM2 = new NumericalMinimizer(hOSCenterMC,hSSCenterMC,hOSSidebandMC,hSSSidebandMC,1.1*1e6);
  
  
//Clear the over and Underflow bins, as they should be empty  
  NM1->m_flipRatePt->ClearUnderflowAndOverflow();
  NM2->m_flipRatePt->ClearUnderflowAndOverflow();
  



//******    Plots are done here    ************************

  
  NM2->m_flipRateEta->SetLineColor(kRed);
  NM2->m_flipRateEta->SetMarkerColor(kRed);
  NM2->m_flipRatePt->SetLineColor(kRed);
  NM2->m_flipRatePt->SetMarkerColor(kRed);
  
  
  // Defining the legend of the plots 
  TLegend* leg = new TLegend(0.20,0.600,0.4,0.725);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  leg->SetFillStyle(0);
  leg->SetTextSize(0.045);
  leg->AddEntry(NM1->m_flipRateEta,"#font[42]{Data}","lpe0");
  leg->AddEntry(NM2->m_flipRateEta,"#font[42]{Sherpa 2.21 Z#rightarrow ee}","lpe0");



//****    f(eta) plot    ********

  TCanvas* c1 = new TCanvas("c1","c1",600,600);
  c1->cd();
  
  //Drawing the f(eta) flip rate
  NM1->m_flipRateEta->Draw();
  NM1->m_flipRateEta->GetXaxis()->SetTitle("#eta");
  NM1->m_flipRateEta->GetYaxis()->SetTitle("f(#eta)");
  NM1->m_flipRateEta->GetYaxis()->SetRangeUser(1e-2,2.5);
  
 	NM2->m_flipRateEta->Draw("same");
  NM2->m_flipRateEta->SetLineColor(kRed);
  NM2->m_flipRateEta->SetMarkerColor(kRed);
  

  //Comparison plot code
  //std::vector<TH1D*> c1h1vec;
  //c1h1vec.push_back(NM2.m_flipRateEta);
  //drawComparison2(c1,&c1h1vec,NM1.m_flipRateEta,"f(#eta)","abs(#eta)",1e-2,20,0,2.47);
  

  
  //Drawing everything else
  ATLASLabel(0.20,0.83,"Super-official",1);
  myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  myText(0.60,0.75,1,"P(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();

  
//*****   sigma(Pt) plot    **************  
  
  TCanvas* c2 = new TCanvas("c2","c2",600,600);
  c2->cd();

  
  
    
  NM1->m_flipRatePt->Draw();
  NM1->m_flipRatePt->GetXaxis()->SetTitle("p_{T} [GeV]");
  NM1->m_flipRatePt->GetYaxis()->SetTitle("#sigma(p_{T})");
  NM1->m_flipRatePt->GetYaxis()->SetRangeUser(1e-2,0.2);  
 

  //std::vector<TH1D*> c2h1vec;
  //c2h1vec.push_back(NM2.m_flipRatePt);
  //drawComparison2(c2,&c2h1vec,NM1.m_flipRatePt,"#sigma(p_{T})","p_{T} [GeV]",0,0.2,30,400,true);

	
  NM2->m_flipRatePt->Draw("same");
  NM2->m_flipRatePt->SetLineColor(kRed);
  NM2->m_flipRatePt->SetMarkerColor(kRed);
  
  //ATLAS_LABEL(0.20,0.88,1); myText(0.35,0.9,1,"internal",0.055);
  //myText(0.20,0.84,1,"#sqrt{s} = 13 TeV, 13.9 fb^{-1}",0.055);
  
  ATLASLabel(0.20,0.83,"Preliminary",1);
  myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  myText(0.60,0.75,1,"P(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();



  TH1D* etaRatio = (TH1D*) NM1->m_flipRateEta->Clone();
  TH1D* ptRatio = (TH1D*) NM1->m_flipRatePt->Clone();

  etaRatio->Divide(NM2->m_flipRateEta);
  ptRatio->Divide(NM2->m_flipRatePt);
/*
  TF1* ptFit = new TF1("ptFit","[0]*TMath::Log(log(x-[1]))",30,5000);
  ptRatio->Fit("ptFit","goff","",30,1000);

  gROOT->ProcessLine("pad_2->cd();");
  ptFit->Draw("same");
*/
  TFile *outfile = new TFile("chargeFlipRate.root","RECREATE");
  NM1->m_flipRateEta->SetName("dataEtaRate");
  NM1->m_flipRateEta->Write();
  NM1->m_flipRatePt->SetName("dataPtRate");
  NM1->m_flipRatePt->Write();
  
  NM2->m_flipRateEta->SetName("MCEtaRate");
  NM2->m_flipRateEta->Write();
  NM2->m_flipRatePt->SetName("MCPtRate");
  NM2->m_flipRatePt->Write();
  etaRatio->SetName("etaFunc");
  etaRatio->Write();
  ptRatio->SetName("ptFunc");
  ptRatio->Write();
  

  
  /*
  ROOT::Math::Minimizer* m_min1 = NM1.m_min;
  ROOT::Math::Minimizer* m_min2 = NM2.m_min;
  int nbinxcorr = NM1.m_flipRateEta->GetNbinsX()+NM1.m_flipRatePt->GetNbinsX();
  TH2F* corrMatrix1 = new TH2F("corrM1","corrM1",nbinxcorr,0,nbinxcorr,nbinxcorr,0,nbinxcorr);
  TH2F* corrMatrix2 = new TH2F("corrM2","corrM2",nbinxcorr,0,nbinxcorr,nbinxcorr,0,nbinxcorr);
  for (unsigned int i = 1; i <= nbinxcorr; i++){
    for (unsigned int j = 1; j <= nbinxcorr; j++){
      corrMatrix1->SetBinContent(i,j, m_min1->Correlation(i-1,j-1) );
      corrMatrix2->SetBinContent(i,j, m_min2->Correlation(i-1,j-1) );
    }
  }
  for (unsigned int i = 1; i <= NM1.m_flipRateEta->GetNbinsX(); i++){
    corrMatrix1->GetXaxis()->SetBinLabel(i,Form("eta%d",i));
    corrMatrix1->GetYaxis()->SetBinLabel(i,Form("eta%d",i));
    corrMatrix2->GetXaxis()->SetBinLabel(i,Form("eta%d",i));
    corrMatrix2->GetYaxis()->SetBinLabel(i,Form("eta%d",i));
  }
  for (unsigned int i = NM1.m_flipRateEta->GetNbinsX()+1; i <= nbinxcorr; i++){
    corrMatrix1->GetXaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
    corrMatrix1->GetYaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
    corrMatrix2->GetXaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
    corrMatrix2->GetYaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
  }
  corrMatrix1->Scale(100.);
  corrMatrix1->GetXaxis()->LabelsOption("v");
  corrMatrix2->Scale(100.);
  corrMatrix2->GetXaxis()->LabelsOption("v");

  gStyle->SetPaintTextFormat("3.0f");


  TCanvas c3("c3","c3",800,600);
  c3.SetRightMargin(0.2);
  c3.SetLeftMargin(0.12);
  corrMatrix1->Draw("colz text");
  corrMatrix1->GetYaxis()->SetTitle("parameter");
  corrMatrix1->GetYaxis()->SetTitleOffset(1.0);
  corrMatrix1->GetXaxis()->SetTitle("parameter");
  corrMatrix1->GetXaxis()->SetNoExponent();
  corrMatrix1->GetXaxis()->SetMoreLogLabels();
  corrMatrix1->GetZaxis()->SetTitle("Correlation [%]");
  corrMatrix1->GetZaxis()->SetTitleOffset(1.5);
  ATLASLabel(0.18,0.90,"internal",0);
  myText(0.18,0.85,0,"data flip-rate fit");


  TCanvas c4("c4","c4",800,600);
  c4.SetRightMargin(0.2);
  c4.SetLeftMargin(0.12);
  corrMatrix2->Draw("colz text");
  corrMatrix2->GetYaxis()->SetTitle("parameter");
  corrMatrix2->GetYaxis()->SetTitleOffset(1.0);
  corrMatrix2->GetXaxis()->SetTitle("parameter");
  corrMatrix2->GetXaxis()->SetNoExponent();
  corrMatrix2->GetXaxis()->SetMoreLogLabels();
  corrMatrix2->GetZaxis()->SetTitle("Correlation [%]");
  corrMatrix2->GetZaxis()->SetTitleOffset(1.5);
  ATLASLabel(0.18,0.90,"internal",0);
  myText(0.18,0.85,0,"MC flip-rate fit");
*/

  c1->Print("chargeFlipEta.eps");
  c2->Print("chargeFlipPt.eps");

 // c3.Print("chargeFlipCorrMatrixData.eps");
 // c4.Print("chargeFlipCorrMatrixMC.eps");

  outfile->Close();

}
