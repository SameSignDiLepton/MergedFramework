#!/bin/bash

## Batch

#INPATH="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/ssdilep/Zmumu/nominal"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/MCtoRun/Sherpa_CT10_VV_llmumu_4000M5000_tree.root/"
INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/MCtoRun/SignalSamples/"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/MCtoRun/MadGraphPythia8EvtGen_A14NNPDF23LO_ttZllonshell_Np1_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/Data/299243.physics_Main_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/MCtoRun/Sherpa_221_NNPDF30NNLO_Zmumu_MAXHTPTV280_500_CVetoBVeto_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/MCtoRun/Sherpa_221_NNPDF30NNLO_lllv_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v3/Data/302053.physics_Main_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/Data/302393.physics_Main_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v2/Data/302925.physics_Main_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Pythia8EvtGen_A14NNPDF23LO_DCH500_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/Data/300345.physics_Main_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Pythia8EvtGen_A14NNPDF23LO_DCH300_tree.root/"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Pythia8EvtGen_A14NNPDF23LO_DCH1000_tree.root/" 
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Sherpa_CT10_VV_llee_50M150_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Sherpa_CT10_VV_llee_4000M5000_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Pythia8EvtGen_A14NNPDF23LO_DCH500_tree.root"
#INPATH="/gpfs_data/local/atlas/ucchielli/ExoticNtuples/v1/MCtoRun/Sherpa_CT10_VV_llmumu_50M150_tree.root"
#INPATH="/home/ATLAS-T3/ucchielli/SSCode/SSDiLep/user.gucchiel.SSDiLep.v1Ntuples.364118.Sherpa_221_NNPDF30NNLO_Zee_MAXHTPTV70_140_CFilterBVeto_tree.root"
INSCRIPT="/home/ATLAS-T3/ucchielli/Katja/MergedFramework/ssdilep/run/"
#SCRIPT="j.plotter_SignalEfficiencyStudy.py"
#SCRIPT="j.plotter_BkgEstimation.py"
#SCRIPT="j.plotter_SSInclusiveValidation.py"
#SCRIPT="j.plotter_CRemu_SSVR.py"
#SCRIPT="j.plotter_VR2.py"
#SCRIPT="j.plotter_CRemu_diboson.py"
#SCRIPT="j.plotter_CRemu_ttbar.py"
SCRIPT="j.plotter_emu_SR12_syst.py"
#SCRIPT="j.plotter_CR2EEEE.py"
#SCRIPT="j.plotter_CRemu_Zveto.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/zumu.root --sampletype="mc" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9814654._000001.tree.root.2   --sampletype="mc" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.mmuskinj.10363561._000001.tree.root --sampletype="mc" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.mmuskinj.10919469._000001.tree.root --sampletype="mc" --samplename="ntuple" --config="max_entry:20000"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/DCH450.root  --sampletype="mc" --samplename="DCH450_HREpMp_HREmMm" #--config="max_entry:20000"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/DCH900.root   --sampletype="mc" --samplename="ntuple"  #--config="sys:TRIG_UP"  #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9697164._000005.tree.root   --sampletype="data" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9647165._000002.tree.root   --sampletype="data" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9647460._000002.tree.root  --sampletype="data" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9814654._000001.tree.root.2   --sampletype="mc" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/user.gucchiel.9635625._000001.tree.root   --sampletype="mc" #--events=2000 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/physics_Main_00302380.root --sampletype="data" --events=200 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH}/Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_BFilter.root --sampletype="mc" --events=200   #--config="sys:FF_DN" 

