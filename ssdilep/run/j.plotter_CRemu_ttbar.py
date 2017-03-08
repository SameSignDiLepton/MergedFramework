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
    config.setdefault('sys',None)
    systematic = config['sys']

    sys_ff    = None

    if   systematic == None: pass
    elif systematic == 'FF_UP':      sys_ff    = 'up'
    elif systematic == 'FF_DN':      sys_ff    = 'dn'
    else: 
        assert False, "Invalid systematic %s!"%(systematic)


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
    loop += ssdilep.algs.vars.BuildTrigConfig(
        required_triggers = ["HLT_e17_lhloose_nod0_mu14"],
        key = 'leptons_dilepton',
        )
    
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

    ## initialize and/or decorate objects
    ## ---------------------------------------
    loop += ssdilep.algs.vars.EleMuVars(key_electrons='electrons_loose',key_muons='muons')   
   
    ## cuts
    ## +++++++++++++++++++++++++++++++++++++++
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='OneElectronOneMuon')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='BadJetVeto')
    loop += ssdilep.algs.algs.CutAlg(cutflow='presel',cut='DCHFilter') 

    loop += ssdilep.algs.EvWeights.OneOrTwoBjetsSF(
            key='OneOrTwoBjetsSF',
            )    

    ## weights configuration
    ## ---------------------------------------
    ## event
    ## +++++++++++++++++++++++++++++++++++++++
    #loop += ssdilep.algs.EvWeights.TrigPresc(
    #        use_avg   = True,
    #        SKIP      = True,
    #        key       = "DataUnPrescAvg",
    #        )
    loop +=  ssdilep.algs.EvWeights.EleTrigSF(
            trig_list =  ["HLT_e17_lhloose_nod0_mu14"],
            key       = "EleTrigSF",
            scale     = None,
            )

    loop += ssdilep.algs.EvWeights.ChargeFlipEleSF(
            key='ChargeFlipEleSF',
            config_file=os.path.join(main_path,'ssdilep/data/chargeFlipRates-12-01-2017.root'),
            chargeFlipSF=True,
            )
    
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
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.EleAllSF(
            ele_index      = 0,
            ele_iso        = "isolLoose",
            ele_reco       = "MediumLLH",
            key           = "Ele0AllSF",
            scale         = None,
            )

    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "NotFixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu0RecoSF",
            scale         = None,
            )
    loop += ssdilep.algs.ObjWeights.MuAllSF(
            mu_index      = 0,
            mu_iso        = "FixedCutTightTrackOnly",
            mu_reco       = "Loose",
            key           = "Mu0AllSF",
            scale         = None,
            )

    #implementation of electron fake factors

    loop += ssdilep.algs.ObjWeights.EleFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/fakeFactor-09-01-2017.root'),
            ele_index=0,
            key='Ele0FF',
            sys=None,
            )
    loop += ssdilep.algs.ObjWeights.MuFakeFactorGraph(
            config_file=os.path.join(main_path,'ssdilep/data/g_reducedthr_ff.root'),
            mu_index=0,
            key='Mu0FF',
            scale=sys_ff,
            )

    ## configure histograms
    ## ---------------------------------------
    hist_list = []
    hist_list += ssdilep.hists.EleMuMain_hists.hist_list
    
    ##-------------------------------------------------------------------------
    ## make plots
    ##-------------------------------------------------------------------------

    ## OS CR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRttbar_TT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddOSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuTT',['Ele0AllSF','Mu0AllSF']],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRttbar_TL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddOSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuTL',['Ele0AllSF','Mu0RecoSF','Mu0FF']],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRttbar_LT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddOSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuLT',['Ele0RecoSF','Mu0AllSF','Ele0FF']],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'OSCRttbar_LL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddOSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuLL',['Ele0RecoSF','Mu0RecoSF','Ele0FF','Mu0FF']],
                           ],
            )
    ## SS CR
    ## ---------------------------------------
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SSCRttbar_TT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddSSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuTT',['Ele0AllSF','Mu0AllSF','ChargeFlipEleSF']],
                           ['MassBelow200GeV',None],
                           ],
            )

    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SSCRttbar_TL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddSSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuTL',['Ele0AllSF','Mu0RecoSF','Mu0FF']],
                           ['MassBelow200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SSCRttbar_LT',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddSSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuLT',['Ele0RecoSF','Mu0AllSF','Ele0FF']],
                           ['MassBelow200GeV',None],
                           ],
            )
    loop += ssdilep.algs.algs.PlotAlg(
            region       = 'SSCRttbar_LL',
            plot_all     = False,
            do_var_check = True,
            hist_list    = hist_list,
            cut_flow     = [
                           ['PassMixed',None],
                           ['OddSSElectronMuon',None],
                           ['OneOrTwoBjets',['OneOrTwoBjetsSF']],
                           ['EleMuLL',['Ele0RecoSF','Mu0RecoSF','Ele0FF','Mu0FF']],
                           ['MassBelow200GeV',None],
                           ],
            )

    loop += pyframe.algs.HistCopyAlg()

    ##-------------------------------------------------------------------------
    ## run the job
    ##-------------------------------------------------------------------------
    loop.run(chain, 0, config['events'],
            branches_on_file = config.get('branches_on_file'),
            do_var_log = config.get('do_var_log'),
            )
#______________________________________________________________________________
if __name__ == '__main__':
    pyframe.config.main(analyze)


