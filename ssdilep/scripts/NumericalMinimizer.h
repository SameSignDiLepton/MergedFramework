

#ifndef NumericalMinimizer_H
#define NumericalMinimizer_H

#include "TH1.h"
#include "Math/Minimizer.h"
#include "TFile.h"

//-------------------------------------------------
// Numerical Minimizer Class ----------------------
//-------------------------------------------------
class NumericalMinimizer {

public:

	//Constructors
  
  NumericalMinimizer(TH1F* hOSCenter=nullptr, TH1F* hSSCenter=nullptr, TH1F* hOSSideband=nullptr, TH1F* hSSSideband=nullptr, double aa=1e9);
  

	//Attributes
  TH1F* m_hOSCenter;
  TH1F* m_hSSCenter;
  TH1F* m_hOSSideband;
  TH1F* m_hSSSideband;

  
  double m_ptBins[15] = {30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200., 400.};
  double m_etaBins[19] = {0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};

  const double m_constraint = 1e9;

  int m_NetaBins = 18;
  int m_NptBins = 14;

  ROOT::Math::Minimizer* m_min = nullptr;
  
  TH1D* m_flipRatePt = nullptr;
  TH1D* m_flipRateEta = nullptr;

  TFile* m_outFile = nullptr;
  
  //Methods

  ROOT::Math::Minimizer* NumericalMinimization1D(const char* minName = "Minuit2", const char* algoName = "" , int randomSeed = -1);
  
  double LogLikelihood1D(const double*);
  double LogLikelihood1Dfull(const double*);

};


#endif
