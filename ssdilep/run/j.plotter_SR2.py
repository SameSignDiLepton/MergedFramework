#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
j.postprocessor.py
"""

## std modules
import os,re

## ROOT
import ROOT
ROOT.gROOT.SetBatch(True)

## my modules
import pyframe

## local modules
import ssdilep

GeV = 1000.0


#_____________________________________________________________________________
def analyze(config):
  
    ##-------------------------------------------------------------------------
    ## setup
    ##-------------------------------------------------------------------------
    config['tree']       = 'physics/nominal'
    config['do_var_log'] = True
    main_path = os.getenv('MAIN')
    
    ## build chain
    chain = ROOT.TChain(config['tree'])
    for fn in config['input']: chain.Add(fn)

    ##-------------------------------------------------------------------------
    ## systematics 
    ##------------------------------------------------------------------------- 
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    """
    pass systematics on the command line like this:
    python j.plotter.py --config="sys:SYS_UP"
    """
    config.setdefault('sys',None)
    systematic = config['sys']


    sys_FF_ele   = None
    sys_FF_mu   = None
    sys_trig = None
    sys_id   = None
    sys_iso  = None
    sys_reco = None
    sys_TTVA = None
    sys_CF = None
    sys_kfactor = None
    sys_beam = None
    sys_choice = None
    sys_pdf = None
    sys_pi = None
    sys_scale_z = None
    ## tree systematics
    treeSys = ""
    if systematic == 'EG_RESOLUTION_ALL_UP': treeSys = "EG_RESOLUTION_ALL__1up"
    elif systematic == 'EG_RESOLUTION_ALL_DN': treeSys = "EG_RESOLUTION_ALL__1down"
    elif systematic == 'EG_SCALE_ALLCORR_UP': treeSys = "EG_SCALE_ALLCORR__1up"
    elif systematic == 'EG_SCALE_ALLCORR_DN': treeSys = "EG_SCALE_ALLCORR__1down"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_UP': treeSys = "EG_SCALE_E4SCINTILLATOR__1up"
    elif systematic == 'EG_SCALE_E4SCINTILLATOR_DN': treeSys = "EG_SCALE_E4SCINTILLATOR__1down"
    elif systematic == 'MUON_ID_DN':treeSys= "MUON_ID___1down"
    elif systematic == 'MUON_ID_UP':treeSys= "MUON_ID___1up"
    elif systematic == 'MUON_MS_DN':treeSys= "MUON_MS___1down"
    elif systematic == 'MUON_MS_UP':treeSys= "MUON_MS___1up"
    elif systematic == 'MUON_RESBIAS_DN':treeSys= "MUON_SAGITTA_RESBIAS___1down"
    elif systematic == 'MUON_RESBIAS_UP':treeSys= "MUON_SAGITTA_RESBIAS___1up"
    elif systematic == 'MUON_RHO_DN':treeSys= "MUON_SAGITTA_RHO___1down"
    elif systematic == 'MUON_RHO_UP':treeSys= "MUON_SAGITTA_RHO___1up"
    elif systematic == 'MUON_SCALE_DN':treeSys= "MUON_SCALE___1down"
    elif systematic == 'MUON_SCALE_UP':treeSys= "MUON_SCALE___1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARCALIB_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARCALIB_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2015PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2015PRE__1down"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_UP': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1up"
    # elif systematic == 'EG_SCALE_LARTEMPERATURE_EXTRA2016PRE_DN': treeSys = "EG_SCALE_LARTEMPERATURE_EXTRA2016PRE__1down"
    else:
        treeSys = "nominal"
        if systematic == None: pass
        elif systematic == 'ELEFF_UP':      sys_FF_ele   = 'UP'
        elif systematic == 'ELEFF_DN':      sys_FF_ele   = 'DN'
        elif systematic == 'MUFF_UP':      sys_FF_mu   = 'UP'
        elif systematic == 'MUFF_DN':      sys_FF_mu   = 'DN'
        elif systematic == 'CF_UP':      sys_CF   = 'UP'
        elif systematic == 'CF_DN':      sys_CF   = 'DN'
        elif systematic == 'TRIG_UP':    sys_trig = 'UP'
        elif systematic == 'TRIG_DN':    sys_trig = 'DN'
        elif systematic == 'TRIG_UPSTAT': sys_trig= 'UPSTAT'
        elif systematic == 'TRIG_UPSYS':  sys_trig= 'UPSYS'
        elif systematic == 'TRIG_DNSTAT': sys_trig= 'DNSTAT'
        elif systematic == 'TRIG_DNSYS':  sys_trig= 'DNSYS'
        elif systematic == 'ID_UP':      sys_id   = 'UP'
        elif systematic == 'ID_DN':      sys_id   = 'DN'
        elif systematic == 'ID_UPSTAT': sys_id    = 'UPSTAT'
        elif systematic == 'ID_DNSTAT': sys_id    = 'DNSTAT'
        elif systematic == 'ID_UPSYS':  sys_id    = 'UPSYS'
        elif systematic == 'ID_DNSYS':  sys_id    = 'DNSYS'
        elif systematic == 'ISO_UP':    sys_iso   = 'UP'
        elif systematic == 'ISO_DN':    sys_iso   = 'DN'
        elif systematic == 'ISO_UPSTAT':     sys_iso   = 'UPSTAT'
        elif systematic == 'ISO_DNSTAT':     sys_iso   = 'DNSTAT'
        elif systematic == 'ISO_UPSYS':     sys_iso   = 'UPSYS'
        elif systematic == 'ISO_DNSYS':     sys_iso   = 'DNSYS'
        elif systematic == 'RECO_UP':    sys_reco  = 'UP'
        elif systematic == 'RECO_DN':    sys_reco  = 'DN'    
        elif systematic == 'RECO_UPSTAT':  sys_reco  = 'UPSTAT'
        elif systematic == 'RECO_DNSTAT':  sys_reco  = 'DNSTAT'    
        elif systematic == 'RECO_UPSYS':  sys_reco  = 'UPSYS'
        elif systematic == 'RECO_DNSYS':  sys_reco  = 'DNSYS'    
        elif systematic == 'TTVA_UPSTAT':  sys_TTVA  = 'UPSTAT'
        elif systematic == 'TTVA_DNSTAT':  sys_TTVA  = 'DNSTAT'    
        elif systematic == 'TTVA_UPSYS':  sys_TTVA  = 'UPSYS'
        elif systematic == 'TTVA_DNSYS':  sys_TTVA  = 'DNSYS'    
        elif systematic == 'BEAM_UP':    sys_beam  = 'UP'
        elif systematic == 'BEAM_DN':    sys_beam  = 'DN'    
        elif systematic == 'CHOICE_UP':  sys_choice  = 'UP'
        elif systematic == 'CHOICE_DN':  sys_choice  = 'DN'    
        elif systematic == 'PDF_UP':     sys_pdf  = 'UP'
        elif systematic == 'PDF_DN':     sys_pdf  = 'DN'    
        elif systematic == 'PI_UP':      sys_pi  = 'UP'
        elif systematic == 'PI_DN':      sys_pi  = 'DN'
        elif systematic == 'SCALE_Z_UP': sys_scale_z  = 'UP'
        elif systematic == 'SCALE_Z_DN': sys_scale_z  = 'DN'

    assert treeSys!="", "Invalid systematic %s!"%(systematic)

    ##-------------------------------------------------------------------------
    ## event loop
    ##-------------------------------------------------------------------------
    loop = pyframe.core.EventLoop(name='ssdilep',
                                  sampletype=config['sampletype'],
                                  samplename=config['samplename'],
                                  outfile=config['samplename']+".root",
                                  quiet=False,
                                  )
    
    ## configure the list of triggers 
    ## with eventual prescales and puts a
    ## trig list to the store for later cutflow
    ## ---------------------------------------
    """
    loop += ssdilep.algs.vars.BuildTrigConfig(
        required_triggers = ["HLT_2e17_lhloose","HLT_e17_lhloose_nod0_mu14","HLT_2mu14"],
        key = 'electrons',
        )
    """
    ## build and pt-sort objects
    ## ---------------------------------------
    loop += pyframe.algs.ListBuilder(
        prefixes = ['muon_','el_','jet_'],
        keys = ['muons','electrons','jets'],
        )
    loop += pyframe.algs.AttachTLVs(
        keys = ['muons','electrons','jets'],
        )
    # just a decoration of particles ...
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='muons',
        )
    loop += ssdilep.algs.vars.ParticlesBuilder(
        key='electrons',
        )
    loop += ssdilep.algs.vars.BuildLooseElectrons(
        key_electrons='electrons',
        )
    loop += ssdilep.algs.vars.BuildLooseAndTightMuons(
        key_muons='muons',
        )
    ## build MET
    ## ---------------------------------------
    loop += ssdilep.algs.met.METCLUS(
        prefix='metFinalClus',
        key = 'met_clus',
        )
    loop += ssdilep.algs.met.METTRK(
        prefix='metFinalTrk',
        key = 'met_trk',
        )

    ## start preselection cutflow 
    ## ---------------------------------------
    loop += pyframe.algs.CutFlowAlg(key='presel')
    
    ## weights
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.EvWeights.MCEventWeight(cutflow='presel',key='weight_mc_event')
    loop += ssdilep.algs.EvWeights.LPXKfactor(cutflow='presel',key='weight_kfactor')
    loop += ssdilep.algs.EvWeights.Pileup(cutflow='presel',key='weight_pileup')

    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='PassTriggersDLT')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='TwoTruthPairsFromDCH')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='FourLeptons')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='ZeroTotalCharge')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BJetVeto')
    #loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter') 

    loop += ssdilep.algs.vars.SR2ChannelFlavour()

    ## initialize and/or decorate objects
    ## ---------------------------------------
    loop += ssdilep.algs.vars.MultiLeptonVars(key_muons='muons', key_electrons='electrons_loose')   

    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = True,
    #        SKIP      = True,
    #        key       = "DataUnPrescAvg",
    #        )
    """
    loop +=  ssdilep.algs.EvWeights.EleTrigSF(
            trig_list =  ["HLT_2e17_lhloose"],
            key       = "EleTrigSF",
            scale     = None,
            )
    """
    
    #Muon trigger efficiency implementation
    """
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Tight",
            mu_sublead_type = "Loose",
            key             = "EffCorrTL",
            scale           = None,
            )
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Loose",
            mu_sublead_type = "Tight",
            key             = "EffCorrLT",
            scale           = None,
            )
    loop += ssdilep.algs.EvWeights.EffCorrPair(
            config_file=os.path.join(main_path,'ssdilep/data/g_corr_eff.root'),
            mu_lead_type    = "Loose",
            mu_sublead_type = "Loose",
            key             = "EffCorrLL",
            scale           = None,

    """
    ## objects
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele0RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele0AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 1,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele1RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 1,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele1AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 2,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele2RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 2,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele2AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 3,
            ele_iso        = "NotLoose",
            ele_reco       = "LooseAndBLayerLLH",
            key           = "Ele3RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 3,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele3AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_reco = sys_reco,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu0RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu0AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 1,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu1RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 1,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu1AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 2,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu2RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 2,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu2AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 3,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu3RecoSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 3,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Medium",
            key           = "Mu3AllSF",
            sys_id = sys_id,
            sys_iso = sys_iso,
            sys_TTVA = sys_TTVA,
            )

    #implementation of electron fake factors

    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-16-05-2017.root'),
            ele_index=0,
            key='Ele0FF',
            sys=sys_FF_ele,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-16-05-2017.root'),
            ele_index=1,
            key='Ele1FF',
            sys=sys_FF_ele,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-16-05-2017.root'),
            ele_index=2,
            key='Ele2FF',
            sys=sys_FF_ele,
            )
    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-16-05-2017.root'),
            ele_index=3,
            key='Ele3FF',
            sys=sys_FF_ele,
            )
    
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
            mu_index=0,
            key='Mu0FF',
            sys=sys_FF_mu,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
            mu_index=1,
            key='Mu1FF',
            sys=sys_FF_mu,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
            mu_index=2,
            key='Mu2FF',
            sys=sys_FF_mu,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/sys_ff_mulead_pt_data_bveto.root'),
            mu_index=3,
            key='Mu3FF',
            sys=sys_FF_mu,
            )

    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.SR2Variables_hists.hist_list
    #hist_list += ssdilep.hists.PtOnly_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## SS CR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEESLTORDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',['SRWeight0']],
                           ['EleTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Ele3AllSF']],
                           ['PassTriggersSLTORDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEEDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',['SRWeight0']],
                           ['EleTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Ele3AllSF']],
                           ['PassTriggersDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEESLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',['SRWeight0']],
                           ['EleTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Ele3AllSF']],
                           ['PassTriggersSLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMMMSLTORDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',['SRWeight1']],
                           ['MuMuMuMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3AllSF']],
                           ['PassTriggersSLTORDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMMMDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',['SRWeight1']],
                           ['MuMuMuMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3AllSF']],
                           ['PassTriggersDLT',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMMMSLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',['SRWeight1']],
                           ['MuMuMuMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3AllSF']],
                           ['PassTriggersSLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEMUMUSLTORDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',['SRWeight2']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['PassTriggersSLTORDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEMUMUDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',['SRWeight2']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['PassTriggersDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEMUMUSLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',['SRWeight2']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['PassTriggersSLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EMUEMUSLTORDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',['SRWeight3']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['PassTriggersSLTORDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EMUEMUDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',['SRWeight3']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['PassTriggersDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EMUEMUSLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',['SRWeight3']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['PassTriggersSLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEMSLTORDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',['SRWeight4']],
                           ['EEEMuTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Mu0AllSF']],
                           ['PassTriggersSLTORDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEMDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',['SRWeight4']],
                           ['EEEMuTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Mu0AllSF']],
                           ['PassTriggersDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEMSLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',['SRWeight4']],
                           ['EEEMuTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Mu0AllSF']],
                           ['PassTriggersSLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMEMSLTORDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',['SRWeight5']],
                           ['MuMuEMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Ele0AllSF']],
                           ['PassTriggersSLTORDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMEMDLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',['SRWeight5']],
                           ['MuMuEMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Ele0AllSF']],
                           ['PassTriggersDLT',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMEMSLT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',['SRWeight5']],
                           ['MuMuEMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Ele0AllSF']],
                           ['PassTriggersSLT',None],
                           ],
            )
    """
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEE',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronPairs',['SRWeight0']],
                           #['DiElePass',['EleTrigSF']],
                           ['EleTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Ele3AllSF']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ['DeltaMassOverMass',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMMM',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSMuonPairs',['SRWeight1']],
                           #['DiElePass',['EleTrigSF']],
                           ['MuMuMuMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Mu3AllSF']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEMUMU',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEMM',['SRWeight2']],
                           #['DiElePass',['EleTrigSF']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EMUEMU',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEMEM',['SRWeight3']],
                           #['DiElePass',['EleTrigSF']],
                           ['EEMuMuTTTT',['Ele0AllSF','Ele1AllSF','Mu0AllSF','Mu1AllSF']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_EEEM',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsEEEM',['SRWeight4']],
                           #['DiElePass',['EleTrigSF']],
                           ['EEEMuTTTT',['Ele0AllSF','Ele1AllSF','Ele2AllSF','Mu0AllSF']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SR2_MMEM',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['TwoSSElectronMuonPairsMMEM',['SRWeight5']],
                           #['DiElePass',['EleTrigSF']],
                           ['MuMuEMuTTTT',['Mu0AllSF','Mu1AllSF','Mu2AllSF','Ele0AllSF']],
                           ['IsSignalRegion2',None],
                           ['ZVeto',None],
                           ['DeltaMassOverMass',None],
                           ],
            )
    """        
    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    min_entry = int(config.get('min_entry') if ('min_entry' in config.keys()) else  0)
    max_entry = int(config.get('max_entry') if ('max_entry' in config.keys()) else -1)
    print min_entry," ",max_entry
    loop.run(chain, 
            min_entry = min_entry,
            max_entry = max_entry,
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)



