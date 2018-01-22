#ifndef EXOSourceRunsPolishedInfo_hh
#define EXOSourceRunsPolishedInfo_hh

#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <vector>
#include <set>
#include <cmath>
#include <algorithm>

#include "TROOT.h"
#include "TObject.h"
#include "TString.h"
#include "TRandom3.h"

#include "EXOUtilities/EXORunInfo.hh"

class EXOSourceRunsPolishedInfo : public TObject
{
public:
  EXOSourceRunsPolishedInfo(const char* sourceRunsInfoFileName = "");
  virtual ~EXOSourceRunsPolishedInfo();
  
  bool SetSourceRunsInfoFile(const char* sourceRunsInfoFileName);
  const char* GetSourceRunsInfoFileName();
  void Print(Int_t runNo = 0) const;
  void PrintRunList(Int_t runNo = 0, TString outputRunsInfoFileName = "") const;

  const EXOMetadata* FindMetadata(const std::string& key, const std::vector<EXOMetadata> & vecMD) const;
  const std::vector<std::string> GetListOf(const char* key) const;
  const std::set<std::string> GetSetOf(const char* key) const;

  void ClearExceptRuns();
  void AddExactCondition(const std::string& key, const std::string& value, bool toKeepOrDiscard = true); 
  bool CutDoubleComparison(const std::string& key, double value, bool greaterOrSmaller);
  bool CutExact(const std::string& key, const std::string& value, bool toKeepOrDiscard = true);
  bool CutExactList(const std::string& key, const std::vector<std::string>& values, bool toKeepOrDiscard = true);

  bool SelectDefaultRuns();
  bool CutDefaultRuns();
  bool SelectMaxPurity(double value = 2.0, bool greaterOrSmaller = true);
    
  void SetMetadata(const std::string& key, const std::string& patData);
  void SetRecoFileNames(const char* patName, const char* runWildcard, const char* dirFiles);
  void SetDataTreeFileNames(const char* nameOption, const char* dirFiles);
  void SetDataSelectionFileNames(const char* dataMCname, const char* cutDatadir, const char* multWildcard);
  void SetMCTreeFileNames(const char* mcDir);
  void SetMCSelectionFileNames(const char* cutMCname, const char* cutMCdir, const char* multWildcard = "[MULTIPLICITY]");

  void SetNoiseLevelPeriods(bool apdOrWire = true, bool splitMed = false, bool splitPos = false);  
  void SetAPDNoiseLevelPeriods(bool splitMed = false, bool splitPos = false);
  void SetWiresNoiseLevelPeriods();
  void SetSpatialDistribution();
  
  size_t GetNRuns() const;
  

protected:

  TString fSourceRunsInfoFileName;
  std::map<Int_t, std::vector<EXOMetadata> > fAllMD;
  std::vector<Int_t> fForceKeep;
  std::vector<Int_t> fForceDiscard;

  bool ReadSourceRunsInfoFromFile(const char* sourceRunsInfoFileName);
  const std::string GetMCTreeFileName(TString sourceName, int positionS, double positionX, double positionY, double positionZ);

  ClassDef(EXOSourceRunsPolishedInfo,1)

}; 

#endif
