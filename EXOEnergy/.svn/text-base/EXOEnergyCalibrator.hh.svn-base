#ifndef EXOEnergyCalibrator_hh
#define EXOEnergyCalibrator_hh

#include <iostream>
#include <vector>
#include <string>
#include <set>

#include "TROOT.h"
#include "TObject.h"
#include "TString.h"

#include "EXOCalibUtilities/EXOFiducialVolume.hh"
#include "EXOCalibUtilities/EXOCalibManager.hh"
#include "EXOCalibUtilities/EXOThoriumPeak.hh"
#include "EXOCalibUtilities/EXOEnergyMCBasedFit.hh"
#include "EXOSourceRunsPolishedInfo.hh"
#include "EXOEnergyUtils.hh"

class EXOEnergyCalibrator : public TObject
{
public:
  EXOEnergyCalibrator(const EXOSourceRunsPolishedInfo* sourceRunsInfo = 0);
  virtual ~EXOEnergyCalibrator();

  void SetVerboseLevel(int verbose = 0);
  void SetCalibrationChannel(std::string channel = "Rotated");
  void SetSourceRunsInfo(const EXOSourceRunsPolishedInfo* sourceRunsInfo);
  void SetIsFitOrAgreement(bool isFit);
  void SetInitialCalibPars(double par0, double par1);
  void SetInitialResPars(double par0, double par1);
  void SetHistoRanges(double energyLow_ss, double energyHigh_ss, double energyLow_ms, double energyHigh_ms);
  void SetUseAngleFromFile(bool use = false) {fUseAngleFromFile = use;}
  void SetAngleFile(const char *AngleFile) {fAngleFile = AngleFile;}
  void SetCalibFlavor(const char *CalibFlavor) {fCalibFlavor = CalibFlavor;}
  void SetIsCalibrated(bool calibrated = false) {fIsCalibrated = calibrated;}
  void SetIgnoreLimits(double min, double max) {if(fIgnoreLimits) delete fIgnoreLimits; fIgnoreLimits = new std::pair<double,double>(min,max);}
  void FitOnlyPeaks(bool peaks=true){fFitOnlyPeaks=peaks;}

  bool FitCalibrationCampaigns(const char* outputFileName, const char* weeklyOutputFileName, const char* weekWildCard);
  bool FitNoisePeriods(const char* outputFileName, const char* weeklyOutputFileName, const char* weekWildCard);
  bool FitSpatialDistributions(const char* outputFileName, const char* weeklyOutputFileName, const char* weekWildCard);
  bool FitWeeklyTh(const char* weeklyOutputFileName, const char* weekWildCard);
  bool FitWeeklySources(const char* weeklyOutputFileName, const char* weekWildCard);
  bool FitForWeek(const std::string& week, const EXOSourceRunsPolishedInfo& runsInfo);
  bool FitForMultiplicity(const int multInt, const EXOSourceRunsPolishedInfo& runsInfo);

  static int fNbins[3];
  static double fLowEnergy[3];
  static double fUpEnergy[3];
  
protected:

  int fVerboseLevel;
  double fCalibFitPars[2];
  double fResFitPars[2];
  bool fUseAngleFromFile;
  const char *fAngleFile;
  const char *fCalibFlavor;
  bool fIsCalibrated;
  std::pair<double,double>* fIgnoreLimits;
  bool fFitOnlyPeaks;
  
  std::string fCalibrationChannel;
  
  const EXOSourceRunsPolishedInfo* fSourceRunsInfo;
  std::string fFitCalibrationType;
  std::string fFitFunctionType;
  TString fOutputName;
  TString fWeeklyOutputName;
  TString fWeekWildCard;
  std::map<std::string, TF1> fWeeklyCalibFunc;
                          
  bool AddMC(EXOEnergyMCBasedFit1D& energyFitter, const EXOSourceRunsPolishedInfo& runsInfo, const int multInt);
  bool AddData(EXOEnergyMCBasedFit1D& energyFitter, const EXOSourceRunsPolishedInfo& runsInfo, const int multInt);
  bool SetWeightedHisto(const char* histoName, EXOEnergyMCBasedFit1D& energyFitter, const EXOSourceRunsPolishedInfo& runsInfo, const int multInt, const std::string keyDivision = "", const std::string keyWeight = "");
  bool SetHisto(const char* histoName, EXOEnergyMCBasedFit1D& energyFitter, const EXOSourceRunsPolishedInfo& runsInfo, const int multInt, const double weight = 1.);
  bool SetFitFunctions(EXOEnergyMCBasedFit1D& energyFitter);
  double GetWeekAngle(long time, int multInt, int week);
  bool SetWeeklyCalibrationFunctions(const std::set<std::string>& weeks);
  bool GetCalibrationFunctionForWeek(TF1& calibFunc, const std::string& week, const std::string& multStr);
  void AdjustHistoRanges(bool incCs137 = false, bool hasWeek5or6or7 = false);

  ClassDef(EXOEnergyCalibrator,1)

}; 

#endif


