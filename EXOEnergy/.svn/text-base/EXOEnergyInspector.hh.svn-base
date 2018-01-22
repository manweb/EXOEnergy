#ifndef EXOEnergyInspector_hh
#define EXOEnergyInspector_hh

#include <iostream>
#include <vector>
#include <string>
#include <set>

#include "TROOT.h"
#include "TObject.h"
#include "TString.h"
#include "TGraph.h"
#include "TFile.h"
#include "TCanvas.h"

#include "EXOCalibUtilities/EXOFiducialVolume.hh"
#include "EXOCalibUtilities/EXOCalibManager.hh"
#include "EXOCalibUtilities/EXOEnergyMCBasedFit.hh"

#include "EXOUtilities/EXOEnergyMCBasedFit1D.hh"

#include "EXOSourceRunsPolishedInfo.hh"
#include "EXOEnergyUtils.hh"

class EXOEnergyInspector : public TObject
{
public:
  EXOEnergyInspector(const EXOSourceRunsPolishedInfo* sourceRunsInfo = 0, const char* flavorName = "");  
  virtual ~EXOEnergyInspector();

  void SetVerboseLevel(int verbose = 0);
  void SetSourceRunsInfo(const EXOSourceRunsPolishedInfo* sourceRunsInfo);
  void SetFlavorName(const char *flavorName);
  bool SetOutputFile(const char *filename, const char* mode);

  std::vector<TGraph> PlotWeeklyParameters(const std::string& channel, const std::string& parType);
  std::vector<TGraph> PlotWeeklyParametersForMultiplicity(int multInt, const std::string& channel, const std::string& parType);
  std::vector<TGraph> PlotWeeklyResolution(double energy, const std::string& channel, const std::string& parType);

  //std::vector<TCanvas> PlotSourceShapeAgreement();

protected:

  int fVerboseLevel;
  const EXOSourceRunsPolishedInfo* fSourceRunsInfo;
  std::string fFlavorName;
  TFile *rootFile;
  
  
  ClassDef(EXOEnergyInspector,1)

}; 

#endif
