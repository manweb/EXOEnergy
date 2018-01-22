#ifndef EXORotationAngleFitter_hh
#define EXORotationAngleFitter_hh

#include <iostream>
#include <algorithm>
#include <string>

#include "TROOT.h"
#include "TObject.h"
#include "TFitter.h"
#include "TGraphErrors.h"
#include "Math/Functor.h"
#include "TMinuit.h"
#include "TNtuple.h"
#include "TMath.h"
#include "RooDataHist.h"
#include "RooRealVar.h"
#include "RooGaussian.h"
#include "RooGenericPdf.h"
#include "RooAddPdf.h"
#include "RooPlot.h"

#include "EXOUtilities/EXOEnergyMCBasedFit1D.hh"
#include "EXOSourceRunsPolishedInfo.hh"
#include "EXOEnergyUtils.hh"

class EXORotationAngleFitter : public TObject
{
public:
  EXORotationAngleFitter(const std::string week = "", const std::string mult = "", const double ene = 2458, const EXOSourceRunsPolishedInfo* sourceRunsInfo = 0);
  virtual ~EXORotationAngleFitter();

  void Print(bool printRuns = false);

  void SetVerboseLevel(int verbose = 0){fVerboseLevel = verbose;};
  void SetSourceRunsInfo(const EXOSourceRunsPolishedInfo* sourceRunsInfo){fSourceRunsInfo = sourceRunsInfo;};
  void SetWeekIndex(const std::string week);
  void SetMultiplicity(std::string mult);
  void SetMinimizationEnergy(double energy);
  void SetDenoisedLight(bool isDenoised = true) {fDenoisedLight = isDenoised;};
  void SaveAllAnglesResults(bool save){fSaveAllAnglesResults = save;};
  void UseGaussErrfc(bool use = false) {fUseGaussErrfc = use;}

  void SetCalibEnergyBins(int binSize, double lowEne, double upEne);
  void SetFitPars(bool firstFit = false, double calibP0 = 0, double calibP1 = 0, double resolP0 = 0, double resolP1 = 0, double trigP0 = 0, double trigP1 = 0);

  void SetOutputFileName(const char* name){fOutputFileName = name;};
  void SaveOutputFile(std::string name = "", bool saveBestResolFit = false, int rebin = 1);

  bool ExecuteFit(const char* minimizer = "MINIMIZE", Float_t fitPrecision = 1.);
  bool RunScanAndFit();
  bool RunFitForAngle(double angle);
  
  
protected:

  int fVerboseLevel;
  std::string fOutputFileName;
  
  const EXOSourceRunsPolishedInfo* fSourceRunsInfo;
  EXOSourceRunsPolishedInfo* fWeekRunsInfo;
  std::string fWeekIndex;
  int fWeekIndexInt;
  std::string fMultiplicity;
  int fMultiplicityInt;
  double fMinimizationEnergyValue;
  bool fDenoisedLight;

  EXOEnergyMCBasedFit1D* fEnergyMCBasedFitter;
  std::map<std::string, std::vector<double> > fEnergyMC;
  std::map<std::string, std::vector<double> > fEnergyWeight;
  std::map<std::string, std::vector<double> > fEnergyCharge;
  std::map<std::string, std::vector<double> > fEnergyScint;

  bool PrepareEnergyVectors();
  bool PrepareEnergyMC();
  bool PrepareEnergyData();
  
  bool RunEnergyFitterWithAngle(double angle, bool allCalcs = false, std::string option = "");
  bool AddMC();
  bool AddData(double angle);
  void AdjustHistoRanges(double angle, bool incCs137 = false, bool hasWeek5or6or7 = false);
  bool SetHisto(double angle);
  bool SetFitFunctions();
  bool FitHistoGaussErrfc();
  TH1F *GetFitFunctionHisto();
  bool SaveFitResults(double angle, double resol, bool bestFit = false);
  double FitRooHisto();

  bool FitChannelsCalibPars();
  bool Scanner(double start, double stop, double step, TGraphErrors*& graph, int early = 0, bool setInitialGuess = false);

  double fCalibPars[2];
  double fResolPars[2];
  double fTrigEffPars[2];
  int fNbinsFit;
  double fLowEnergyFit;
  double fUpEnergyFit;
  double fInitialThPeak;
  bool fSaveAllAnglesResults;
  double fAvgAgree;
  
  double fBestAngle;
  double fBestResol;
  double fBestCalibPars[2];
  double fBestResolPars[2];
  double fBestTrigEffPars[2];
  
  int fCalibBinSize;
  double fCalibLowEnergyFit;
  double fCalibUpEnergyFit;
  TF1 *fChargeCalib;
  TF1 *fLightCalib;
  
  TH1F *fFitHisto;
  TF1 *fFitFunctionGaussErrfc;
  bool fUseGaussErrfc;
  RooPlot *fPlotFrame;

  TFitter *fFitter;
  ROOT::Math::Functor *fFitFunction;
  static void Fcn(int &, double *, double& f, double *, int);
  static ROOT::Math::IMultiGenFunction *fFCN;
  double FitFunction(const double* x);

  TGraphErrors* fResolVsAngle1;
  TGraphErrors* fResolVsAngle2;
  TGraphErrors* fResolVsAngle3;
  TGraphErrors* fResolVsAngle4;

  ClassDef(EXORotationAngleFitter,1)

}; 

#endif
