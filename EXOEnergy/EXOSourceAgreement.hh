#ifndef EXOSourceAgreement_hh
#define EXOSourceAgreement_hh

#include <iostream>
#include <map>
#include <set>

#include "TObject.h"
#include "TNamed.h"
#include "TString.h"
#include "TChain.h"
#include "TEntryList.h"
#include "TFile.h"
#include "TParameter.h"
#include "TClonesArray.h"

#include "RooWorkspace.h"
#include "RooArgList.h"
#include "RooRealVar.h"
#include "RooAbsData.h"
#include "RooAbsPdf.h"
//#include "RooAddPdf.h"
#include "RooFitResult.h"

#include "EXOCalibUtilities/EXOCalibManager.hh"
#include "EXOCalibUtilities/EXOEnergyResol.hh"

#include "EXOSourceRunsPolishedInfo.hh"
#include "EXOFittingUtil.hh"

class EXOSourceAgreement : public TObject
{
public:
  virtual ~EXOSourceAgreement();

  enum EXOAgreementType_t {kSource, kLB};
  
  void Print();
  void Print(TString meta);
  EXOSourceRunsPolishedInfo* GetRunInfo(){return &fRunsInfo;};
  void SetResolution(const char* flavor, const char* table, bool weekly = false);
  bool AddObservable(RooRealVar& obs, bool forceAdd = false);
  void SetHistogramWeights(TString group, TString weight);
  void SetSepType(int sep);

  bool PairObsToSeps(std::set<int> limiter ); // if set nonempty only use fobslist incides in set
  bool PairObsToSeps(){ // default uses empty filter set
    std::set<int> s ; s.clear(); return PairObsToSeps(s);
  }

  const std::set<TString>* GetSeparation() const{return &fSeparation;}
  const std::map<TString, std::vector<TString> >* GetAgreements() const{return &fAgreements;}
  const std::set<TString>* GetComparisons() const{return &fComparisons;}

  TH1* GetResultHisto(const char* agreement, const char* name, const char* data, const char* comparison = 0);
  
  void SaveToFile(const char* name);

  int fRebinX;

protected:
  EXOSourceAgreement(const char* sourceRunsInfoFileName = "../data/UpdatedLivetimeSourceRunsInfo.txt" );
  EXOSourceAgreement(EXOSourceRunsPolishedInfo& sourceRunsInfo);
  EXOSourceAgreement(const char* filename, const char* wspname, const char* pdfname, bool readObs = true);

  virtual void Init();

  EXOSourceRunsPolishedInfo fRunsInfo;
  TString fWspFileName;
  TString fWspName;
  TString fPdfName;
  const EXOAgreementType_t fAgreeType;
  
  bool AddResultHisto(TH1* histo);
  bool ReadWspObservables();
  
  EXOEnergyResol* fResolution;
  bool fUseWeeklyResol;

  int fDimension;
  std::set<TString> fSeparation;
  TString fGroupName;
  TString fGroupWeight;


  RooArgList fObsList; // list of cloned observables
  std::vector<std::pair<int ,TString> > fObsSepPairs ; // pair obs and seps, so as to stop doing energy_ss data_ms etc.

  std::map<TString, Double_t> fWeightedActivity;
  std::map<TString, TH1*> fDataHisto;
  std::map<TString, TH1*> fMCHisto;
  std::map<TString, TH1*> fResultHisto;

  std::set<TString> fComparisons;
  std::map<TString, std::vector<TString> > fAgreements;

  bool SetResultWspPars(RooFitResult* result, RooWorkspace* wsp, bool pdfOn);
  
  RooArgList GetObservablesIn(RooArgList& obsList, TString sep, TString data);
  RooRealVar* GetEnergyObservableIn(RooArgList obsList);
  TString GetObservableLimitsCut(RooArgList obsList);
  bool MakeComparisonHistos(TH1* data, TH1* mc, TString agree, TString id);

  void DeleteHistos(std::map<TString, TH1*>& histos);
  void SaveHistosToFile(std::map<TString, TH1*>& histos, TFile& file);

  ClassDef(EXOSourceAgreement,1)

};

#endif
