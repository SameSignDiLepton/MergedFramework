#!/bin/bash

## Batch

#INPATH_DATA="/afs/cern.ch/user/s/sarnling/Exot12_data/*.physics_Main.root,"
#INPATH_DATA_EXOT19="/afs/cern.ch/user/s/sarnling/exot19_data/exot12data1.root"
#INPATH_MC="/afs/cern.ch/user/s/sarnling/Exot12_mc/*.root,"
#INSCRIPT="/afs/cern.ch/user/s/sarnling/MergedFramework/ssdilep/run"
#SCRIPT="j.plotter_CF.py"

#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA}  --sampletype="data" --samplename="ntuple_data" --events=-1 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA_EXOT19}  --sampletype="data" --samplename="ntuple_data_exot19" --events=-1 #--config="sys:FF_DN"
#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_MC}  --sampletype="mc" --samplename="ntuple_mc" --events=-1 #--config="sys:FF_DN"


#INPATH_DATA="/afs/cern.ch/user/s/sarnling/Exot12_data/*.physics_Main.root,"
INPATH_MC="/afs/cern.ch/work/s/sarnling/TauTest/*.root,"
INSCRIPT="/afs/cern.ch/user/s/sarnling/MergedFramework/ssdilep/run"
SCRIPT="j.plotter_CF_tau.py"


#python ${INSCRIPT}/${SCRIPT} --input ${INPATH_DATA}  --sampletype="data" --samplename="ntuple_data" --events=-1 #--config="sys:FF_DN"
python ${INSCRIPT}/${SCRIPT} --input ${INPATH_MC}  --sampletype="mc" --samplename="ntuple_mc_tau" --events=200000 #--config="sys:FF_DN"


