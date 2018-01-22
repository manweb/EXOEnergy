
import ROOT, settings
import sys, argparse, os, numpy, math
from array import *

ROOT.gSystem.Load('../lib/libEXOEnergy.so')

ROOT.gStyle.SetPalette(51)
ROOT.gStyle.SetOptStat(0)

def CheckDiagonalCut(infoRuns,diagCut,energyThreshold):
	allWeeks = infoRuns.GetListOf('WeekIndex')

	grFraction = ROOT.TGraph()

	grFraction.SetMarkerStyle(20)
	grFraction.SetMarkerSize(0.8)

	h_empty = ROOT.TH2D('cut events','cut events',100,240,300,100,0,1.0)

	h_empty.GetXaxis().SetTitle('week')
	h_empty.GetYaxis().SetTitle('fraction cut (%)')

	h_empty.GetXaxis().CenterTitle()
	h_empty.GetYaxis().CenterTitle()
	
	c1 = ROOT.TCanvas('c1','c1',1000,600)
	c1.Print('DiagCut.pdf(')

	rotate = False

	weeks = set([])
	weekOld = -1
	for i in range(allWeeks.size()):
		week = allWeeks.at(i)

		if week == weekOld:
			continue

		weekOld = week

		print 'Working on week',week
		fraction = LoadDataForWeek(infoRuns,week,diagCut,rotate,energyThreshold)

		grFraction.SetPoint(i,float(week),fraction*100)

	c1 = ROOT.TCanvas('c1','c1',1000,600)

	h_empty.Draw()
	grFraction.Draw('Psame')

	c1.Print('DiagCut.pdf)')

	fOut = ROOT.TFile('DiagCutFraction.root','RECREATE')

	c1.Write()

	fOut.Close()

	return

def DetermineDiagonalCut(infoRuns,source,ELow,EHigh):
	infoRunsCopy = infoRuns.Clone();
	infoRunsCopy.CutExact('SourceName',source,True)

	print 'Determining diagonal cut for source ', source

	histo1D = ROOT.TH1F('histo1D','histo1D', 600,0,3000)
	histo2D = ROOT.TH2F('rotated SS','rotated SS',1000,0,5000,1000,0,20000)

	runs = set([])
	allRuns = infoRunsCopy.GetListOf('RunNumber')
	allWeeks = infoRunsCopy.GetListOf('WeekIndex')
	for i in range(allRuns.size()):
		run = allRuns.at(i)
		week = allWeeks.at(i)
		angle = GetAngleForWeek(week)

		r = FillDataOfRun(histo1D,histo2D,run,angle,0,0,True,None)

	h1DY = histo2D.ProjectionY('projectionY',histo2D.GetXaxis().FindBin(ELow),histo2D.GetXaxis().FindBin(EHigh))
	h1DX = histo2D.ProjectionX('projectionX')

	c1 = ROOT.TCanvas('c1','c1',1000,600)
	histo2D.Draw('colz')

	c2 = ROOT.TCanvas('c2','c2')
	h1DY.Draw()

	c3 = ROOT.TCanvas('c3','c3')
	h1DX.Draw()

	fOut = ROOT.TFile('DiagCutTest.root','RECREATE')
	c1.Write()
	c2.Write()
	c3.Write()

	fOut.Close()

	return

def LoadDataForWeek(infoRuns,week,diagCut,rotate,energyThreshold):
	infoRunsCopy = infoRuns.Clone();
	infoRunsCopy.CutExact('WeekIndex',week,True)
	allRuns = infoRunsCopy.GetListOf('RunNumber')

	histo1D = ROOT.TH1F('histo1D %s' % week,'histo1D %s' % week, 600,0,3000)
	histo2D = ROOT.TH2F('week %s SS' % week,'week %s SS' % week,1000,0,3500,1000,0,20000)

	histo2D.GetXaxis().SetTitle('ionization')
	histo2D.GetYaxis().SetTitle('scintillation')

	histo2D.GetXaxis().CenterTitle()
	histo2D.GetYaxis().CenterTitle()

	nEventsCut = 0

	angle = GetAngleForWeek(week)
	calibPars = GetCalibPars(week)
	if not calibPars:
		print 'Calibration parameters not found for week %s. Skipping this week.' % (week)
		return None

	runs = set([])
	for i in range(allRuns.size()):
		run = allRuns.at(i)

		nEventsCut += FillDataOfRun(histo1D, histo2D, run, angle, calibPars[0], calibPars[1], rotate, diagCut, energyThreshold)

		#for k in range(len(runData)):
		#	histo.Fill(runData[k])

	fraction = 0
	if histo2D.GetEntries() > 0:
		fraction = nEventsCut / histo2D.GetEntries()
	print 'Cut events = ',nEventsCut,'Entries = ',histo2D.GetEntries(),'Fraction = ',fraction

	c1 = ROOT.TCanvas('c1','c1',1000,600)

	histo2D.Draw('colz')
	diagCut.Draw('same')

	c1.Print('DiagCut.pdf')

	return fraction

def GetCalibPars(week):
	f = ROOT.TFile(settings.CalibrationOutput+'fit_week_%s_ss.root' % (week),'READ')

	if f.IsZombie():
		return None

	calib = f.Get('calib')

	calibPar = [calib.GetParameter(0),calib.GetParameter(1)]

	return calibPar

def FillDataOfRun(histo1D, histo2D, runNumber, angle, calibPar0, calibPar1, rotate, diagCut, energyThreshold):
	f = ROOT.TFile(settings.SelectionTreeFileName.replace('[RunNumber]',runNumber),'READ')

	print 'Adding run %s: angle = %f, p0 = %f, p1 = %f' % (runNumber,angle,calibPar0,calibPar1)

	entryList = f.Get('EventList_ss')
	treeName = entryList.GetTreeName()
	fileName = entryList.GetFileName()

	f2 = ROOT.TFile(fileName,'READ')
	tree = f2.Get(treeName)
	tree.SetEntryList(entryList)

	tree.Draw('(cos(%f)*e_charge + sin(%f)*e_scint)*%f+%f' % (angle, angle, calibPar1, calibPar0),'multiplicity < 1.5','goff')

	if tree.GetSelectedRows() > 0:
		histo1D.FillN(tree.GetSelectedRows(), tree.GetV1(), numpy.ones(tree.GetSelectedRows()))

	if energyThreshold:
		if rotate:
			tree.Draw('(e_charge*TMath::Sin(%f)+e_scint*TMath::Cos(%f)):(e_charge*TMath::Cos(%f)-e_scint*TMath::Sin(%f))'%(-1*angle,-1*angle,-1*angle,-1*angle),'multiplicity < 1.5 && ((TMath::Cos(%f)*e_charge + TMath::Sin(%f)*e_scint)*%f+%f) > %f'%(angle,angle,calibPar1,calibPar0,energyThreshold),'goff')
		else:
        		tree.Draw('e_scint:e_charge','multiplicity < 1.5 && ((TMath::Cos(%f)*e_charge + TMath::Sin(%f)*e_scint)*%f+%f) > %f'%(angle,angle,calibPar1,calibPar0,energyThreshold),'goff')
	else:
		if rotate:
			tree.Draw('(e_charge*TMath::Sin(%f)+e_scint*TMath::Cos(%f)):(e_charge*TMath::Cos(%f)-e_scint*TMath::Sin(%f))'%(-1*angle,-1*angle,-1*angle,-1*angle),'multiplicity < 1.5','goff')
		else:
	        	tree.Draw('e_scint:e_charge','multiplicity < 1.5','goff')

	nEventsCut = 0

        if tree.GetSelectedRows() > 0:
        	histo2D.FillN(tree.GetSelectedRows(), tree.GetV2(), tree.GetV1(), numpy.ones(tree.GetSelectedRows()))

		if diagCut:
			for i in range(tree.GetSelectedRows()):
				if tree.GetV1()[i] > diagCut.Eval(tree.GetV2()[i]):
					nEventsCut += 1
	else:
		print 'No rows selected'

	return nEventsCut

def GetAngleForWeek(week):
	t = ROOT.TTree()
	t.ReadFile(settings.angleFile)

	t.Draw('angle','week == '+week+' && mult == 1','goff')

	angle = t.GetV1()[0]

	return angle

if __name__ == '__main__':

	settings.init()

	infoRuns = ROOT.EXOSourceRunsPolishedInfo(settings.SourceRunsFileName)

	infoRuns.CutDoubleComparison('WeekIndex',settings.minWeek,True)
	infoRuns.CutDoubleComparison('WeekIndex',settings.maxWeek,False)

	infoRuns.CutDefaultRuns()

	infoRuns.CutExact('SourceName','Cs-137',False)
	infoRuns.CutExact('TriggerPrescale','0',True)

	infoRuns.CutExact('RunNumber','7536',False) # for now
	infoRuns.CutExact('RunNumber','7537',False) # for now
	infoRuns.CutExact('RunNumber','7490',False) # for now Th228 at S8 with strange feature
	infoRuns.CutExact('RunNumber','7248',False) # for now low stat
	infoRuns.CutExact('RunNumber','7633',False) # for now low stat
	infoRuns.CutExact('RunNumber','7640',False) # for now low stat

	diagCut = ROOT.TF1('diagCut','[0]*x+[1]',0,5000)

	diagCut.SetLineStyle(2)

	energyThreshold = 1000

	#diagCut.SetParameters(3.405,2600.67) # SS
	#diagCut.SetParameters(3.63036,2876.03) # MS

	diagCut.SetParameters(2.827,1573) # SS Phase2
	#diagCut.SetParameters(2.942,1742) # MS Phase2

	CheckDiagonalCut(infoRuns,diagCut,energyThreshold)

	#infoRuns.CutExact('WeekIndex','266',True)
	#DetermineDiagonalCut(infoRuns,'Th-228',4000,4400)

