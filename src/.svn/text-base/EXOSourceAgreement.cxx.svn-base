#include "EXOSourceAgreement.hh"

ClassImp(EXOSourceAgreement)

EXOSourceAgreement::EXOSourceAgreement(const char* sourceRunsInfoFileName)
: fRunsInfo(sourceRunsInfoFileName), fAgreeType(kSource)
{
  Init();
}

EXOSourceAgreement::EXOSourceAgreement(EXOSourceRunsPolishedInfo& sourceRunsInfo)
  : fRunsInfo(sourceRunsInfo), fAgreeType(kSource)
{
  Init();
}

EXOSourceAgreement::EXOSourceAgreement(const char* filename, const char* wspname, const char* pdfname, bool readObs)
  : fWspFileName(filename), fWspName(wspname), fPdfName(pdfname), fAgreeType(kLB)
{
  Init();
  if(readObs)
    ReadWspObservables();
}

void EXOSourceAgreement::Init()
{
  fResolution = 0;
  fUseWeeklyResol = false;
  fDimension = 0;

  fRebinX = 1;

  fGroupName = "WeekIndex";
  fGroupWeight = "WeekLivetime";

  fSeparation.insert("SS");
  fSeparation.insert("MS");

  fComparisons.insert("data");
  fComparisons.insert("mc");
  fComparisons.insert("ratio");
  fComparisons.insert("resid");
  fComparisons.insert("absrd");
  
  fComparisons.insert("ratio_no_low");

}

EXOSourceAgreement::~EXOSourceAgreement()
{
  fResolution = 0;

  DeleteHistos(fDataHisto);
  DeleteHistos(fMCHisto);
  DeleteHistos(fResultHisto);
}

void EXOSourceAgreement::SetSepType(int sep)
{
    fSeparation.clear();
    if(sep == EXOFittingUtil::kSSMS)
    {
        std::cout << "********************* SS/MS **********************" << std::endl;
        fSeparation.insert("SS");
        fSeparation.insert("MS");
    }
    else if(sep == EXOFittingUtil::kNone)
    {
        std::cout << "********************* all **********************" << std::endl;
        fSeparation.insert("ALL");
    }
    else
    {
        std::cout << "********************* Fail SS/MS **********************" << std::endl;
        //Defaulting to SS/MS since not a valid arguement
        fSeparation.insert("SS");
        fSeparation.insert("MS");
    }

}

void EXOSourceAgreement::DeleteHistos(std::map<TString, TH1*>& histos)
{
  if(not histos.empty())
  {
    for(std::map<TString, TH1*>::iterator histo = histos.begin(); histo != histos.end(); histo++)
    {
      if(histo->second)
        delete histo->second;
    }
    histos.clear();
  }
}

void EXOSourceAgreement::Print(TString meta)
{
  std::set<std::string> datas = fRunsInfo.GetSetOf(meta.Data());
  std::cout << meta << " :";
  for(std::set<std::string>::iterator data = datas.begin(); data != datas.end(); data++)
    std::cout << " " << *data;
  std::cout << "\n";
}

void EXOSourceAgreement::Print()
{
  //fRunsInfo.Print();

  Print("RunNumber");
  Print("SourceName");
  std::cout << "Observables: ";
  fObsList.Print();
  std::cout << "Separation:";
  for(std::set<TString>::iterator sep = fSeparation.begin(); sep != fSeparation.end(); sep++)
    std::cout << " " << *sep;
  std::cout << "\n";
}

bool EXOSourceAgreement::PairObsToSeps(std::set<int> limiter){
  fObsSepPairs.clear();
  bool dolimit = (limiter.size() > 0 ) ; // prep
  //  std::cout << dolimit << std::endl;

  // excludes energy_ss from ms and vice-versa
  for(int i = 0; i < fObsList.getSize(); i++) {
    if ( ( limiter.count(i) == 0 ) and dolimit ) continue;

    RooRealVar* obs = dynamic_cast<RooRealVar*>(fObsList.at(i));
    if(not obs) continue;
    TString name(obs->GetName());
    name.ToUpper();
    //    TString* testee  = ((TString*) name.Tokenize("_")->Last() ) ;
    int issep =
      fSeparation.count( ((TObjString *)(name.Tokenize("_")->Last() ))->String() ); 
    for(std::set<TString>::iterator sep = fSeparation.begin();
	sep != fSeparation.end(); sep++){
      //std::cout << name.Data() << " " << (*sep).Data() << " " << issep << std::endl;
      if ((name.Contains( Form("_%s", (*sep).Data() ) ) ) or (issep == 0 )) {
	fObsSepPairs.push_back(std::pair<int, TString>( i , (*sep) ) ) ;
      }
    }
  }
  //  std::cout << "size " << fObsSepPairs.size() << std::endl;
  return true;
}

bool EXOSourceAgreement::AddObservable(RooRealVar& obs, bool forceAdd)
{
  if(fAgreeType == kLB and not forceAdd)
    return false;
  return fObsList.addClone(obs);
}

bool EXOSourceAgreement::ReadWspObservables()
{
  TFile wspFile(fWspFileName.Data(),"read");
  if(wspFile.IsZombie())
  {
    fWspFileName = "";
    fWspName = "";
    fPdfName = "";
    return false;
  }
  RooWorkspace* wsp = dynamic_cast<RooWorkspace*>(wspFile.Get(fWspName.Data()));
  if(not wsp)
  {
    fWspFileName = "";
    fWspName = "";
    fPdfName = "";
    return false;
  }
  RooRealVar* num_pdf = dynamic_cast<RooRealVar*>(wsp->var(Form("num_%s",fPdfName.Data())));
  if(not num_pdf)
  {
    fWspFileName = "";
    fWspName = "";
    fPdfName = "";
    return false;
  }
  
  std::set<TString> allObs;
  std::list<RooAbsData*> allData = wsp->allData();
  for(std::list<RooAbsData*>::iterator data = allData.begin(); data != allData.end(); data++)
  {
    const RooArgSet* obsSet = (*data)->get();
    TIterator *obsIter = obsSet->createIterator();
    RooRealVar *obs = NULL;
    while((obs = dynamic_cast<RooRealVar*>(obsIter->Next())))
    {
      allObs.insert(obs->GetName());
    }
    delete obsIter;
  }

  fObsList.removeAll();
  for(std::set<TString>::iterator obsName = allObs.begin(); obsName != allObs.end(); obsName++)
  {
    fObsList.addClone(*wsp->var(obsName->Data()));
  }

  std::cout << "New obs list: ";
  fObsList.Print();

  PairObsToSeps();

  wspFile.Close();
  return true;
}

bool EXOSourceAgreement::SetResultWspPars(RooFitResult* result, RooWorkspace* wsp, bool pdfOn)
{
  if(not result)
    return false;

  TString numName(Form("num_%s",fPdfName.Data()));
  
  const RooArgList& finals = result->floatParsFinal();
  for(int i = 0; i < finals.getSize(); i++)
    {
    RooRealVar* par = dynamic_cast<RooRealVar*>(finals.at(i));
    if(par)
    {
      TString parName(par->GetName());
      if(parName.BeginsWith("num_"))
      {
        RooRealVar* wPar = wsp->var(parName.Data());
        if(parName == numName)
          wPar->setVal(pdfOn ? par->getVal(): 0.);
        else
          wPar->setVal(pdfOn ? 0. : par->getVal());
      }
    }
  }
  
  return true;
}

void EXOSourceAgreement::SetResolution(const char* flavor, const char* table, bool weekly)
{
  if(fResolution)
    delete fResolution;
  fResolution = EXOEnergyResol::GetInstanceForFlavor(flavor,table);
  fUseWeeklyResol = weekly;
}

void EXOSourceAgreement::SetHistogramWeights(TString group, TString weight)
{
  fGroupName = group;
  fGroupWeight = weight;
}

bool EXOSourceAgreement::AddResultHisto(TH1* histo)
{
  if(not histo)
    return false;

  histo->SetStats(0);
  if(fResultHisto.count(histo->GetName()))
    delete fResultHisto[histo->GetName()];
  fResultHisto.insert(std::make_pair(histo->GetName(),histo));
  return true;
}

bool EXOSourceAgreement::MakeComparisonHistos(TH1* data, TH1* mc, TString agree, TString id)
{
  //  std::cout << "Making some comparisons" << std::endl;
  if(not (data and mc))
    return false;

  fAgreements[agree].push_back(id);
  
  if(fComparisons.count("data") > 0)
  {
    if(not AddResultHisto(data))
      return false;
  }
  if(fComparisons.count("mc") > 0)
  {
    if(not AddResultHisto(mc))
      return false;
  }

  TString name(Form("%s_%s",id.Data(),agree.Data()));
  
  if(fComparisons.count("ratio") > 0)
  {
    TH1* ratio = dynamic_cast<TH1*>(data->Clone(Form("%s_ratio",name.Data())));
    ratio->Divide(mc);
    if(not AddResultHisto(ratio))
      return false;
  }

  if (fComparisons.count("ratio_no_low") ) {
    // ratio filtering out any points where insufficient statistics are projected
    TH1* no_low = dynamic_cast<TH1*>(data->Clone(Form("%s_ratio_no_low",name.Data())));
    no_low->Divide(mc); // so far the same as ratio. now ignore some
    double minfrac = 9.0 /data->GetEntries(); // need to predict at least 9 counts for data rate to consider skew ratio here --> as at <9 one expects ~33% skew from statistics.
    for (int bx = 0 ; bx < no_low->GetNbinsX() ; bx++ ){ // check all bins
      if (mc->GetBinContent(bx) < minfrac ){ // squelch ratio there
	no_low->SetBinContent(bx,1.);
	no_low->SetBinError(bx,0.);
      }else if (mc->GetBinContent(bx) < minfrac * 2){ // distrust some the next region, use factor of 10
	double bc = no_low->GetBinContent(bx);
	bc = (bc - 1.0)/10.0 + 1;
	no_low->SetBinContent(bx,bc);
      }
    }

    if(not AddResultHisto(no_low))
      return false;
  }

  if(fComparisons.count("resid") > 0)
  {
    TH1* resid = dynamic_cast<TH1*>(data->Clone(Form("%s_resid",name.Data())));
    resid->Add(mc,-1);
    resid->Divide(mc);
    if(not AddResultHisto(resid))
      return false;
  }

  if(fComparisons.count("absrd") > 0)
  {
    TH1* absrd = dynamic_cast<TH1*>(data->Clone(Form("%s_absrd",name.Data())));
    absrd->Add(mc,-1);
    absrd->Divide(mc);
    for(int b = 0; b <= absrd->GetNbinsX()+absrd->GetNbinsY()+absrd->GetNbinsZ(); b++)
      absrd->SetBinContent(b,fabs(absrd->GetBinContent(b)));
    if(not AddResultHisto(absrd))
      return false;
  }
  
  return true;
}

TH1* EXOSourceAgreement::GetResultHisto(const char* agreement, const char* name, const char* data, const char* comparison)
{
  TString id = Form("%s_%s_%s",name,agreement,data);
  if(comparison)
    id = Form("%s_%s",id.Data(),comparison);

  if(fResultHisto.count(id.Data()) > 0)
    return fResultHisto.at(id.Data());

  return 0;
}


void EXOSourceAgreement::SaveHistosToFile(std::map<TString, TH1*>& histos, TFile& file)
{
  for(std::map<TString, TH1*>::iterator histo = histos.begin(); histo != histos.end(); histo++)
  {
    if(histo->second)
    {
      file.cd(); // ok to keep doing this
      // canvas issues were making it seem like code was failing : so standardize saving in a way that is viewable
      double big   = 1.1 * ( histo->second->GetMaximum() ) ;
      double small = 1.1 * ( histo->second->GetMinimum() ) ;
      if (small > 0. ) small = 0. ;
      histo->second->SetMaximum( big );
      histo->second->SetMinimum(small);
      histo->second->Write();
    }
  }
}

void EXOSourceAgreement::SaveToFile(const char* name)
{
  TFile file(name,"recreate");
  SaveHistosToFile(fMCHisto,file);
  SaveHistosToFile(fDataHisto,file);
  SaveHistosToFile(fResultHisto,file);

  for(std::map<TString, Double_t>::iterator iter = fWeightedActivity.begin(); iter != fWeightedActivity.end(); iter++)
  {
    TParameter<Double_t> activity(Form("weighted_activity_%s",iter->first.Data()),iter->second);
    file.cd();
    activity.Write();
  }
  file.Close();
}

RooArgList EXOSourceAgreement::GetObservablesIn(RooArgList& obsList, TString sep, TString data)
{
  data.ToLower();
  sep.ToLower();
  
  RooArgList result;
  
  if(data == "data")
  {
    // excludes energy_ss from ms and vice-versa
    for(int i = 0; i < obsList.getSize(); i++)
    {
      RooRealVar* obs = dynamic_cast<RooRealVar*>(obsList.at(i));
      if(not obs)
        continue;
      TString obsName(obs->GetName());
      if(obsName.Contains("_ss") && sep.Contains("ms"))
        continue;
      if(obsName.Contains("_ms") && sep.Contains("ss"))
        continue;
      result.add(*obs);
    }
  }

  if(data == "mc")
  {
    // no cuts in energy_mc
    for(int i = 0; i < obsList.getSize(); i++)
    {
      RooRealVar* obs = dynamic_cast<RooRealVar*>(obsList.at(i));
      if(not obs)
        continue;
      TString obsName(obs->GetName());
      if(obsName.Contains("energy"))
        continue;
      result.add(*obs);
    }
  }
  return result;
}

RooRealVar* EXOSourceAgreement::GetEnergyObservableIn(RooArgList obsList)
{
  for(int i = 0; i < obsList.getSize(); i++)
  {
    RooRealVar* obs = dynamic_cast<RooRealVar*>(obsList.at(i));
    if(not obs)
      continue;
    TString obsName(obs->GetName());
    if(obsName.Contains("energy"))
      return obs;
  }
  return 0;
}

TString EXOSourceAgreement::GetObservableLimitsCut(RooArgList obsList)
{
  TString cut;
  bool first = true;
  for(int i = 0; i < obsList.getSize(); i++)
  {
    RooRealVar* obs = dynamic_cast<RooRealVar*>(obsList.at(i));
    if(not obs)
      continue;
    
    //TString varName = var.GetName();
    // if(varName.Contains("min")) or if(varName.Contains("max"))

    
    cut += first ? "" : " && ";
    cut += Form("(%g <= %s && %s <= %g)", obs->getMin(),obs->GetName(),obs->GetName(),obs->getMax());
    first = false;
  }
  return cut;
}
