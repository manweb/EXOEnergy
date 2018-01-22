#ifndef EXOSourceAgreementManager1D_hh
#define EXOSourceAgreementManager1D_hh

#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "TString.h"
#include "TChain.h"
#include "TEntryList.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "TList.h"

#include "RooArgList.h"
#include "RooRealVar.h"

#include "EXOFitInfo.hh"
#include "EXOFittingUtil.hh"

#include "EXOSourceRunsPolishedInfo.hh"
#include "EXOSourceAgreement.hh"
#include "EXOSourceAgreement1D.hh"

typedef struct DataMCProduction {
  TString fName;
  TString fResolFlavor;
  TString fResolTable;
  Bool_t fResolWeekly;

  TString fDataFiles;
  TString fPreMCLocation;
  TString fCutMCLocation;
  TString fCutMCname;

  DataMCProduction(const char* name = 0, const char* resol = 0, const char* table = 0, bool weekly = false){
    fName = name;
    fResolFlavor = resol;
    fResolTable = table;
    fResolWeekly = weekly;
  }

  void SetFilesLocation(const char* files, const char* preDir, const char* cutDir, const char* cutName){
    fDataFiles = files;
    fPreMCLocation= preDir;
    fCutMCLocation = cutDir;
    fCutMCname = cutName;
  }
  
} DataMCProduction;


class EXOSourceAgreementManager1D : public TObject
{
public:
  EXOSourceAgreementManager1D(const char* sourceRunsInfoFileName = "../data/UpdatedLivetimeSourceRunsInfo.txt", const char* filename = 0, const char* wspname = 0, const char* productionfile = 0);
  EXOSourceAgreementManager1D(EXOSourceRunsPolishedInfo& sourceRunsInfo, const char* filename = 0, const char* wspname = 0, const char* productionfile = 0);
  virtual ~EXOSourceAgreementManager1D();

  EXOSourceRunsPolishedInfo* GetRunInfo(){return &fRunsInfo;};
  //void SetRunInfo(EXOSourceRunsPolishedInfo RunsInfo){fRunsInfo = RunsInfo;};

  bool AddLBWspPdf(const char* pdfname);
  bool SetProduction(TString name); // set data and MC production by name, return false if production is not found
  bool LimitObs(std::vector<std::string> limitTo);// limit observables to variables with names in limitTo
  bool RunAgreement(TString dir = "./"); // main action
  void SaveToFile(const char* name);
  bool SetStats(Byte_t stats); // legend plotting options
  void SetUseNoisePeriods(bool useNoise);
  bool GetUseNoisePeriods(void);
  void SetExtraCalib(double aSSval, double bSSval, double aMSval, double bMSval) {aSS=aSSval; bSS=bSSval; aMS=aMSval; bMS=bMSval;};

  const char* GetSourceKey(const char* name, const char* position);
  std::pair<TString, TString> BreakKey(const char* key);

  bool UsrCutExact(std::string ucut); // user cut options a:b:c passed to fRunsInfo.CutExact(a,b,c)
  bool UsrCutDoubleComparison(std::string ucut); // user cut options a:b:c passed to fRunsInfo.CutDoubleComparison(a,b,c)

  void InteractivePrep(TString dir){
    // preload source agreements to check things like runlists -> use option --interactive on python script to run this there
    CreateAvailableSourceAgreements();
    AddRequestedLBAgreements();
    fResultDir = dir;
  }

  EXOSourceRunsPolishedInfo fRunsInfo;


protected:

  virtual void Init();
  bool ReadWspObservables();

  TString fWspFileName;
  TString fWspName;
  std::set<TString> fPdfNames;
  RooArgList fObsList; // master list of observables
  std::vector<std::pair<int ,TString> > fObsSepPairs ; // may not actually be used here
  std::set<int> limObs; // set to limit
  TString fProduction;
  TString fResultDir;
  int fSepType;
  Byte_t fStats;
  TString fProductionFilename;
  bool fUseNoisePeriods;

  //Energy Correction for S2/S8 data
  double aSS;
  double aMS;
  double bSS;
  double bMS;

  std::map<TString, DataMCProduction> fProductions;
  std::map<TString, EXOSourceAgreement1D> fSrcAgrees;

  bool CreateAvailableSourceAgreements();
  bool AddRequestedLBAgreements();
  bool DigestInfoForAll(TString ref);
  TLegend *GetLegendOfAverages(TLegend *legend);
  TLegend *GetLegendOfCorrelations(TLegend *legend);
  TLegend* GetLegendOfWeightedCorrelations(TLegend* legend);

  int GetSourceColor(const char* key);
  int GetSourceMarker(const char* key);
  void CreateAvailableProductions();
  bool ReadAvailableProductions();

  ClassDef(EXOSourceAgreementManager1D,1)

};

#endif
