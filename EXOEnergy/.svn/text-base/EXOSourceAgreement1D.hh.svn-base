#ifndef EXOSourceAgreement1D_hh
#define EXOSourceAgreement1D_hh

#include <iostream>

#include "RooRealVar.h"
#include "RooAbsBinning.h"
#include "TString.h"

#include "EXOSourceAgreement.hh"

class EXOSourceAgreement1D : public EXOSourceAgreement
{
public:
  EXOSourceAgreement1D(const char* sourceRunsInfoFileName = "../data/UpdatedLivetimeSourceRunsInfo.txt");
  EXOSourceAgreement1D(EXOSourceRunsPolishedInfo& sourceRunsInfo);
  EXOSourceAgreement1D(const char* filename, const char* wspname, const char* pdfname, bool readObs = true);
  virtual ~EXOSourceAgreement1D();

  const char* GetName(RooRealVar& var, TString sep);
  TH1D* CreateHisto(RooAbsBinning& binning, TString name, TString suffix);

  bool FillHistos(); // loop over fobsseppairs
  
  bool EvalShape();
  bool EvalShapeFor(RooRealVar& var, TString sep);
  bool EvalSSFractions(); // pair names and separations eg energy_ss/energy_ms/energy_all or for others
  bool EvalSSFractionsFor(TString nameSS, TString nameMS, TString name); // evaluate for named variables
  void SetExtraCalib(double aSSval, double bSSval, double aMSval, double bMSval) {aSS=aSSval; bSS=bSSval; aMS=aMSval; bMS=bMSval; };

protected:

  void Init();

  bool FillHistos(RooRealVar& var, TString sep); // per var sep do source or lb
  bool FillLBHistos(RooRealVar& var, TString sep);
  bool FillSourceHistos(RooRealVar& var, TString sep);
    
  bool FillSmearedMCHisto1D(TH1D& histo, double* vars, RooRealVar* energy, const std::string& channel, double* energies, double* weights, int length, int multiplicity, long int seconds, int nano, int binMC = 1);

  void DeleteHistos1D(std::map<TString, TH1D*>& histos);

  double aSS;
  double aMS;
  double bSS;
  double bMS;

  ClassDef(EXOSourceAgreement1D,1)

};

#endif
