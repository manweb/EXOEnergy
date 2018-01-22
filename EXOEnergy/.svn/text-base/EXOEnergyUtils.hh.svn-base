#ifndef EXOEnergyUtils_hh
#define EXOEnergyUtils_hh

#include <iostream>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <algorithm>

#include "unistd.h"
#include "sys/stat.h"

#include "TROOT.h"
#include "TObject.h"
#include "TString.h"
#include "TChain.h"
#include "TEntryList.h"

#include "EXOCalibUtilities/EXOFiducialVolume.hh"
#include "EXOUtilities/EXOEnergyMCBasedFit1D.hh"
#include "EXOSourceRunsPolishedInfo.hh"

class EXOEnergyUtils : public TObject
{
public:

  static bool AddMCToFitterForMultiplicity(EXOEnergyMCBasedFit1D& energyFitter, const EXOSourceRunsPolishedInfo& runsInfo, const int multInt);

  static bool CreateSourceDataTree(const EXOSourceRunsPolishedInfo& runsInfo, const char* setupFileName, const char* pythonName, bool applyZCorrection, bool isDenoised, const char* ZCorrectionDBFlavor, const char* calibDBFlavor0, const char* calibDBFlavor1, const char* calibDBFlavor2, const char* libEXOFittingScriptDir, const char* submitCommand, const char* scriptWildCard, bool submitJobs = false);
  static bool CutSourceDataTree(const EXOSourceRunsPolishedInfo& runsInfo, const char* setupFileName, const char* pythonName, bool useRandomTrigger, const char* diagonalCutFlavor, double fiducialCut0, double fiducialCut1, double fiducialCut2, double fiducialCut3, const char* libEXOFittingScriptDir, const char* submitCommand, const char* scriptWildCard, bool isMC = false, bool submitJobs = false);
  static bool FriendSourceDataTree(const EXOSourceRunsPolishedInfo& runsInfo, const char* setupFileName, const char* pythonName, const char* prepDir, const char* prepName, const char* weightDir, const char* factoryName, const char* libEXOFittingScriptDir, const char* submitCommand, const char* scriptWildCard, bool isMC = false, bool submitJobs = false);
  static bool CutTreeForMCBasedFit(const EXOSourceRunsPolishedInfo& runsInfo, const char* setupFileName, const char* pythonName, const char* scriptDir, const char* submitCommand, const char* scriptWildCard, bool cutMC = true, bool cutData = true, bool submitJobs = false);

  static const std::string GetDefaultCut(bool isDataOrMC, int multInt);
  
  static const std::string GetSourceName(int sourceZ, int sourceA);
  static int GetAtomicNumber(const char* sourceName);
  static int GetIsotopeNumber(const char* sourceName);

  static const std::vector<int>* GetAllLJRunsForSource();
  static const std::vector<int>* GetLJSourceRuns(int week, int sourceZ, int sourceA);
  static const std::vector<int>* GetLJSourceRuns(int week, const char* sourceName);

  static std::string fRatioFlavor;
  static std::string fPeakFlavor;
  static std::string fBiasFlavor;

  static double fFVCut[3];

  static std::string fCutType;
  static std::string fDiagonalCutDBFlavor;

protected:

  EXOEnergyUtils(){}
  virtual ~EXOEnergyUtils(){}
  
  static bool CutTreeForMCBasedFitIn(TString type, const EXOSourceRunsPolishedInfo& runsInfo, std::string shellScriptBodyPat, const char* submitCommand, const char* scriptWildCard, bool submitJobs = false);

  ClassDef(EXOEnergyUtils,1)

};

#endif
