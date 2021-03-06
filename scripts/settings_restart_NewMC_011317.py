# This file contains variables that are common to all scripts
#
# Calibration:	Data after the re-start. This is only used for
#		monitoring the behavior of the resolution.
#		For this calibration the data using the new lightmap
#		and the Phase II MC is used
#
# Created:	01-13-17

def init():
  global SourceRunsFileName		# Filename of the polished source info file
  global RecoFileName			# Path to the processed files
  global DataTreeFileName		# Path to the preprocessed files
  global SelectionTreeFileName		# Path to the selection file names
  global DataMultiplicityWildcard	# Multiplicity wildcard for selection files
  global DataId				# Name scheme for the data files
  global MCTreeFileName			# Path to the preprocessed MC files
  global MCSelectionFileName		# Path to the selection MC files
  global fiducial1			# Apothem of the fiducial volume
  global fiducial2			# Min Z of the fiducial volume
  global fiducial3			# Max Z of the fiducial voluem
  global cutName			# Cut name for fiducial volume
  global minWeek			# Weeks greater than this number are selected
  global maxWeek			# Weeks greater than this number are cut
  global calibFlavor1			# Weekly calibration flavor
  global calibFlavor2			# Average calibration flavor
  global calibFlavor3			# Dummy value
  global diagonalCut			# Diagonal cut flavor
  global calibrationChannel		# Calibration channel
  global applyZCorrection		# Apply Z-correction?
  global ZCorrectionFlavor		# Z-correction flavor
  global CalibrationOutput		# Output path for the calibration results
  global AngleFitterOutput		# Output path for the rotation angle fitter
  global isDenoised			# Flag indicating whether the data is denoised
  global useAngleFile			# Specify whether to read the rotation angle from file
  global angleFile			# Path to the file containing rotation angles
  global FitRange			# Fit range in units of rotated energy [low_ss, high_ss, low_ms, high_ms]
  global IgnoreLimit			# Energy range to be ignored
  global ShapeAgreeCalibFlavor		# Calibration flavor to be used for the source agreement study
  global CalibType			# Calibration type. Usually energy-mcbased-fit
  global ShapeAgreeRange		# Energy range for shape agreement study [low_ss, high_ss, low_ms, high_ms]
  global ShapeAgreeOutput		# Path to the output file of the shape agreement study

  fiducial1 = 162.
  fiducial2 = 10.
  fiducial3 = 182.
  cutName = 'fv_%i_%i_%i'%(fiducial1,fiducial2,fiducial3)
  SourceRunsFileName = '../data/UpdatedLivetimeSourceRunsInfo_20160616.txt'
  RecoFileName = '/nfs/slac/g/exo-userdata/users/mjjewell/Analysis/Reproc_NewLightMap_12_19_2016/[RunNumber]/reproc0000[RunNumber]-*.root'
  DataTreeFileName = '/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/preprocessed/2017_restart_NewLightMap_011117/ForCalibration/run_[RunNumber]_tree.root'
  SelectionTreeFileName = '/nfs/slac/g/exo_data6/groups/Energy/data/WIPP/selection/2017_restart_NewLightMap_011117/ForCalibration/%s/run_[RunNumber]_tree.root'%(cutName)
  DataMultiplicityWildcard = '[MULTIPLICITY]'
  DataId = 'run_[RunNumber]_[MULTIPLICITY]'
  MCTreeFileName = '/nfs/slac/g/exo_data6/groups/Fitting/data/MC/preprocessed/2017_Phase2_v1/preset/'
  MCSelectionFileName = '/nfs/slac/g/exo_data6/groups/Fitting/data/MC/selection/2017_Phase2_v1/preset/fv_162_10_182/'
  minWeek = 244
  maxWeek = 272
  calibFlavor1 = '2015-v3-weekly'
  calibFlavor2 = '2015-v3-average'
  calibFlavor3 = 'dummy'
  diagonalCut = 'vanilla'
  calibrationChannel = 'Rotated'
  applyZCorrection = False
  ZCorrectionFlavor = 'vanilla'
  CalibrationOutput = '/nfs/slac/g/exo_data4/users/Energy/data/results/calibration/2017_NewMC_011317/rotated/%s/'%(cutName)
  AngleFitterOutput = '/nfs/slac/g/exo_data4/users/Energy/data/results/angle/2017_NewMC_011317/'
  isDenoised = False
  useAngleFile = True
  angleFile = '/nfs/slac/g/exo_data4/users/maweber/software/Devel/EXOEnergy/scripts/WeeklyAngle_061616_NonDenoised.txt'
  FitRange = [1200,6000,1200,6000]
  IgnoreLimit = None # [5000,5200]
  ShapeAgreeCalibFlavor = '2016-v2-weekly'
  CalibType = 'energy-msbased-fit'
  ShapeAgreeRange = [800,4000,300,4000]
  ShapeAgreeOutput = '/nfs/slac/g/exo_data4/users/maweber/software/Devel/EXOEnergy/scripts/srcAgreePlots_061616.root'

