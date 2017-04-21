# encoding: utf-8
'''
vars.py
description:
variables for all the channels
'''

## modules
from var import Var
from funcs import generateLogBins

## Cutflows
## ---------------------------------------
cutflow_weighted          = Var(name = 'cutflow_weighted_mumu',log=False)
cutflow                   = Var(name = 'cutflow_mumu',log=False)
cutflow_weighted_mu_pairs = Var(name = 'cutflow_weighted_mumu_mu_pairs',log=False)
cutflow_mu_pairs          = Var(name = 'cutflow_mumu_mu_pairs',log=False)
cutflow_presel            = Var(name = 'cutflow_presel',log=False)
cutflow_weighted_presel   = Var(name = 'cutflow_weighted_presel',log=False)
cutflow_ZCR               = Var(name = 'cutflow_ZCR',log=False)
cutflow_weighted_ZCR      = Var(name = 'cutflow_weighted_ZCR',log=False)

bins_pt = generateLogBins(35,30,2000)
bins_pt_2 = generateLogBins(20,30,1000)

## Event variables
## ---------------------------------------
averageIntPerXing = Var(name = 'averageIntPerXing',
              path  = 'event',
              xmin  = 0,
              xmax  = 45,
              log   = False,
              )

actualIntPerXing = Var(name = 'actualIntPerXing',
              path  = 'event',
              xmin  = 0,
              xmax  = 45,
              log   = False,
              )

NPV = Var(name = 'NPV',
              path  = 'event',
              xmin  = 0,
              xmax  = 35.,
              log   = False,
              )

nmuons = Var(name = 'nmuons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

nelectrons = Var(name = 'nelectrons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

nleptons = Var(name = 'nleptons',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

njets = Var(name = 'njets',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

nmuonpairs = Var(name = 'nmuonpairs',
              path  = 'event',
              xmin  = 0,
              xmax  = 6,
              log   = False,
              )

mujet_dphi = Var(name = 'mujet_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = True,
              )

scdphi = Var(name     = 'scdphi',
              path    = 'event',
              xmin    = -2.,
              xmax    = 2.,
              rebin   = 4,
              log     = False,
              )

muons_mVis = Var(name     = 'muons_mVis',
              path    = 'event',
              #xmin    = 0.,
              xmin    = 0.,
              #xmax    = 800.,
              xmax    = 1500.,
              rebin   = 20,
              #rebin   = 1,
              log     = False,
              )

muons_mVisTot = Var(name     = 'muons_mVisTot',
              path    = 'event',
              #xmin    = 0.,
              xmin    = 0.,
              #xmax    = 800.,
              xmax    = 1500.,
              rebin   = 40,
              #rebin   = 1,
              log     = False,
              )

muons_mTTot = Var(name     = 'muons_mTTot',
              path    = 'event',
              #xmin    = 0.,
              xmin    = 0.,
              #xmax    = 800.,
              xmax    = 2000.,
              rebin   = 40,
              #rebin   = 1,
              log     = False,
              )

muons_dphi = Var(name = 'muons_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

muons_deta = Var(name = 'muons_deta',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 4,
              log     = False,
              )

muons_dR = Var(name = 'muons_dR',
              path    = 'event',
              xmin    = 0.,
              xmax    = 5.0,
              rebin  = 4,
              log     = False,
              )

muons_chargeprod = Var(name = 'muons_chargeprod',
              path    = 'event',
              xmin    = -2,
              xmax    = 2,
              #rebin  = 10,
              log     = False,
              )

muons_chargesum = Var(name = 'muons_chargesum',
              path    = 'event',
              xmin    = -3,
              xmax    = 3,
              #rebin  = 10,
              log     = False,
              )

muons_pTH = Var(name  = 'muons_pTH',
              path    = 'event',
              xmin    = 0.,
              xmax    = 500.,
              rebin   = 10,
              log     = False,
              )

electrons_mVis = Var(name     = 'electrons_mVis',
              path    = 'event',
              xmin    = 0.,
              xmax    = 2000.,
              rebin   = 4,
              log     = True,
              )

electrons_mTtot = Var(name     = 'electrons_mTtot',
              path    = 'event',
              xmin    = 0.,
              xmax    = 2000.,
              rebin   = 1,
              log     = True,
              )

electrons_dphi = Var(name = 'electrons_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

electrons_deta = Var(name = 'electrons_deta',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 4,
              log     = False,
              )

electrons_chargeprod = Var(name = 'electrons_chargeprod',
              path    = 'event',
              xmin    = -2,
              xmax    = 2,
              #rebin  = 10,
              log = False,
              )

elemu_chargeprod = Var(name = 'elemu_chargeprod',
              path    = 'event',
              xmin    = -2,
              xmax    = 2,
              #rebin  = 10,
              log = False,
              )

elemu_mVis = Var(name     = 'elemu_mVis',
              path    = 'event',
              xmin    = 0.,
              xmax    = 210.,
              rebin   = 20,
              log     = True,
              #logx    = False,
              )

elemu_mTtot = Var(name = 'elemu_mTtot',
              path    = 'event',
              xmin    = 0.,
              xmax    = 2000.,
              rebin   = 1,
              log     = True,
              )

elemu_dphi = Var(name = 'elemu_dphi',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

elemu_deta = Var(name = 'elemu_deta',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 4,
              log     = False,
              )

OSelemu_mVis1 = Var(name     = 'OSelemu_mVis1',
              path    = 'event',
              xmin    = 0.,
              xmax    = 210.,
              rebin   = 20,
              log     = True,
              #logx    = False,
              )

OSelemu_mTtot1 = Var(name = 'OSelemu_mTtot1',
              path    = 'event',
              xmin    = 0.,
              xmax    = 2000.,
              rebin   = 1,
              log     = True,
              )

OSelemu_dphi1 = Var(name = 'OSelemu_dphi1',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

OSelemu_deta1 = Var(name = 'OSelemu_deta1',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 4,
              log     = False,
              )

OSelemu_mVis2 = Var(name     = 'OSelemu_mVis2',
              path    = 'event',
              xmin    = 0.,
              xmax    = 210.,
              rebin   = 20,
              log     = True,
              #logx    = False,
              )

OSelemu_mTtot2 = Var(name = 'OSelemu_mTtot2',
              path    = 'event',
              xmin    = 0.,
              xmax    = 2000.,
              rebin   = 1,
              log     = True,
              )

OSelemu_dphi2 = Var(name = 'OSelemu_dphi2',
              path    = 'event',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

OSelemu_deta2 = Var(name = 'OSelemu_deta2',
              path    = 'event',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin  = 4,
              log     = False,
              )


## Single muon variables
## ---------------------------------------
mulead_pt = Var(name = 'mulead_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 400.,
              #xmax   = 120.,
              #rebin  = 20,
              rebin  = 5,
              log    = False,
              )

musublead_pt = Var(name = 'musublead_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 400.,
              #xmax   = 120.,
              rebin  = 20,
              #rebin  = 5,
              log    = False,
              )

mulead_eta = Var(name = 'mulead_eta',
              path    = 'muons',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 5,
              log     = False,
              )

musublead_eta = Var(name = 'musublead_eta',
              path    = 'muons',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 5,
              log     = False,
              )

mulead_phi = Var(name = 'mulead_phi',
              path    = 'muons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

musublead_phi = Var(name = 'musublead_phi',
              path    = 'muons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

mulead_trkd0 = Var(name = 'mulead_trkd0',
              path    = 'muons',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin  = 1,
              log     = False,
              )

musublead_trkd0 = Var(name = 'musublead_trkd0',
              path    = 'muons',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin   = 1,
              log     = False,
              )

mulead_trkd0sig = Var(name = 'mulead_trkd0sig',
              path    = 'muons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

musublead_trkd0sig = Var(name = 'musublead_trkd0sig',
              path    = 'muons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

mulead_trkz0 = Var(name = 'mulead_trkz0',
              path    = 'muons',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

musublead_trkz0 = Var(name = 'musublead_trkz0',
              path    = 'muons',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

mulead_trkz0sintheta = Var(name = 'mulead_trkz0sintheta',
              path    = 'muons',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

musublead_trkz0sintheta = Var(name = 'musublead_trkz0sintheta',
              path    = 'muons',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

## Single muon variables
# isolation
mulead_topoetcone20 = Var(name = 'mulead_topoetcone20',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )

mulead_topoetcone30 = Var(name = 'mulead_topoetcone30',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
mulead_topoetcone40 = Var(name = 'mulead_topoetcone40',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
mulead_ptvarcone20 = Var(name = 'mulead_ptvarcone20',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = True,
              )
mulead_ptvarcone30 = Var(name = 'mulead_ptvarcone30',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
mulead_ptvarcone40 = Var(name = 'mulead_ptvarcone40',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
mulead_ptcone20 = Var(name = 'mulead_ptcone20',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
mulead_ptcone30 = Var(name = 'mulead_ptcone30',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
mulead_ptcone40 = Var(name = 'mulead_ptcone40',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )


## Muon tag and probe
## -------------------------------------
tag_pt = Var(name = 'tag_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 400.,
              rebin  = 10,
              log    = False,
              )
probe_pt = Var(name = 'probe_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 400.,
              rebin  = 10,
              log    = False,
              )
probe_ptiso = Var(name = 'probe_ptiso',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 500.,
              rebin  = 10,
              log    = False,
              )
probe_ujet_pt = Var(name = 'probe_ujet_pt',
              path   = 'muons',
              xmin   = 0.,
              xmax   = 500.,
              rebin  = 10,
              log    = False,
              )

# jets
jetlead_pt = Var(name = 'jetlead_pt',
              path    = 'jets',
              xmin    = 0.,
              xmax    = 300.,
              rebin   = 5,
              log     = True,
              )


## Single electron variables
## ---------------------------------------
elelead_pt = Var(name = 'elelead_pt',
              path   = 'electrons',
              xmin   = 0.,
              #xmax   = 400.,
              xmax   = 2000.,
              #xmax   = 120.,
              #rebin  = 20,
              #rebin  = 5,
              rebin   = 1,
              #rebinVar = bins_invM,
              log    = True,
              #logx   = False,
              )

elesublead_pt = Var(name = 'elesublead_pt',
              path   = 'electrons',
              xmin   = 0.,
              #xmax   = 400.,
              xmax   = 2000.,
              #xmax   = 120.,
              #rebin  = 20,
              #rebin  = 5,
              rebin  = 1,
              #rebinVar = bins_invM,
              log    = True,
              #logx   = False,
              )

elelead_eta = Var(name = 'elelead_eta',
              path    = 'electrons',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin   = 5,
              rebin   = 1,
              #rebinVar = bins_invM,
              log     = False,
              #logx    = False,
              )

elesublead_eta = Var(name = 'elesublead_eta',
              path    = 'electrons',
              xmin    = -2.5,
              xmax    = 2.5,
              #rebin   = 5,
              rebin   = 1,
              #rebinVar = bins_invM,
              log     = False,
              #logx    = False,
              )

elelead_phi = Var(name = 'elelead_phi',
              path    = 'electrons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              logx    = False,
              )

elesublead_phi = Var(name = 'elesublead_phi',
              path    = 'electrons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              logx    = False,
              )

elelead_trkd0 = Var(name = 'elelead_trkd0',
              path    = 'electrons',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin  = 1,
              log     = False,
              )

elesublead_trkd0 = Var(name = 'elesublead_trkd0',
              path    = 'electrons',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin   = 1,
              log     = False,
              )

elelead_trkd0sig = Var(name = 'elelead_trkd0sig',
              path    = 'electrons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

elesublead_trkd0sig = Var(name = 'elesublead_trkd0sig',
              path    = 'electrons',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

elelead_trkz0 = Var(name = 'elelead_trkz0',
              path    = 'electrons',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

elesublead_trkz0 = Var(name = 'elesublead_trkz0',
              path    = 'electrons',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

elelead_trkz0sintheta = Var(name = 'elelead_trkz0sintheta',
              path    = 'electrons',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

elesublead_trkz0sintheta = Var(name = 'elesublead_trkz0sintheta',
              path    = 'electrons',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

# isolation
elelead_topoetcone20 = Var(name = 'elelead_topoetcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )

elelead_topoetcone30 = Var(name = 'elelead_topoetcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_topoetcone40 = Var(name = 'elelead_topoetcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptvarcone20 = Var(name = 'elelead_ptvarcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = True,
              )
elelead_ptvarcone30 = Var(name = 'elelead_ptvarcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptvarcone40 = Var(name = 'elelead_ptvarcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptcone20 = Var(name = 'elelead_ptcone20',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptcone30 = Var(name = 'elelead_ptcone30',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
              )
elelead_ptcone40 = Var(name = 'elelead_ptcone40',
              path   = 'electrons',
              xmin   = 0.,
              xmax   = 1.2,
              rebin  = 20,
              log    = False,
)


## Mixed channel (e/mu) variables
## ---------------------------------------

## single lepton variables

leplead_pt = Var(name = 'leplead_pt',
              path   = 'elemu',
              xmin   = 30.,
              xmax   = 400.,
              #xmax   = 120.,
              #rebin  = 20,
              rebin  = 1,
              rebinVar = bins_pt,   
              log    = False,
              logx   = True,   
              )

lepsublead_pt = Var(name = 'lepsublead_pt',
              path   = 'elemu',
              xmin   = 30.,
              xmax   = 300.,
              #xmax   = 120.,
              rebin  = 1,
              rebinVar = bins_pt_2,   
              #rebin  = 5,
              log    = False,
              logx   = True,   
              )

leplead_eta = Var(name = 'leplead_eta',
              path    = 'elemu',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 5,
              log     = False,
              )

lepsublead_eta = Var(name = 'lepsublead_eta',
              path    = 'elemu',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 5,
              log     = False,
              )

leplead_phi = Var(name = 'leplead_phi',
              path    = 'elemu',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

lepsublead_phi = Var(name = 'lepsublead_phi',
              path    = 'elemu',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

leplead_trkd0 = Var(name = 'leplead_trkd0',
              path    = 'elemu',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin  = 1,
              log     = False,
              )

lepsublead_trkd0 = Var(name = 'lepsublead_trkd0',
              path    = 'elemu',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin   = 1,
              log     = False,
              )

leplead_trkd0sig = Var(name = 'leplead_trkd0sig',
              path    = 'elemu',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

lepsublead_trkd0sig = Var(name = 'lepsublead_trkd0sig',
              path    = 'elemu',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )

leplead_trkz0 = Var(name = 'leplead_trkz0',
              path    = 'elemu',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

lepsublead_trkz0 = Var(name = 'lepsublead_trkz0',
              path    = 'elemu',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )

leplead_trkz0sintheta = Var(name = 'leplead_trkz0sintheta',
              path    = 'elemu',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

lepsublead_trkz0sintheta = Var(name = 'lepsublead_trkz0sintheta',
              path    = 'elemu',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )
lep3_pt = Var(name = 'lep3_pt',
              path   = 'leptons',
              xmin   = 30.,
              xmax   = 400.,
              #xmax   = 120.,
              #rebin  = 20,
              rebin  = 1,
              rebinVar = bins_pt_2,   
              log    = False,
              logx   = True,   
              )
lep3_eta = Var(name = 'lep3_eta',
              path    = 'leptons',
              xmin    = -2.5,
              xmax    = 2.5,
              rebin   = 5,
              log     = False,
              )
lep3_phi = Var(name = 'lep3_phi',
              path    = 'leptons',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )
lep3_trkd0 = Var(name = 'lep3_trkd0',
              path    = 'elemu',
              xmin    = -0.2,
              xmax    = 0.2,
              rebin  = 1,
              log     = False,
              )
lep3_trkd0sig = Var(name = 'lep3_trkd0sig',
              path    = 'elemu',
              xmin    = 0.,
              xmax    = 10.,
              rebin   = 3,
              log     = False,
              )
lep3_trkz0 = Var(name = 'lep3_trkz0',
              path    = 'elemu',
              xmin    = -1.0,
              xmax    = 1.0,
              rebin   = 1,
              log     = False,
              )
lep3_trkz0sintheta = Var(name = 'lep3_trkz0sintheta',
              path    = 'elemu',
              xmin    = -0.7,
              xmax    = 0.7,
              rebin   = 2,
              log     = False,
              )

## MET variables
## ---------------------------------------
met_clus_et = Var(name = 'met_clus_et',
              path    = 'met',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 10,
              log     = False,
              )

met_clus_phi = Var(name = 'met_clus_phi',
              path    = 'met',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 4,
              log     = False,
              )

met_trk_et = Var(name = 'met_trk_et',
              path    = 'met',
              xmin    = 0.,
              xmax    = 200.,
              rebin   = 20,
              log     = False,
              )

met_trk_phi = Var(name = 'met_trk_phi',
              path    = 'met',
              xmin    = -3.2,
              xmax    = 3.2,
              rebin   = 2,
              log     = False,
              )

met_clus_sumet = Var(name = 'met_clus_sumet',
              path    = 'met',
              xmin    = 0.,
              xmax    = 1000.,
              rebin   = 50,
              log     = False,
              )

met_trk_sumet = Var(name = 'met_trk_sumet',
              path    = 'met',
              xmin    = 0.,
              xmax    = 1000.,
              rebin   = 50,
              log     = False,
              )



vars_list = []


# ---------------------------------
# for all studies: event variables
# ---------------------------------

vars_list.append(averageIntPerXing)
vars_list.append(actualIntPerXing)
vars_list.append(NPV)
vars_list.append(nmuons)
vars_list.append(nelectrons)
vars_list.append(nleptons)
vars_list.append(njets)
vars_list.append(nmuonpairs)

vars_list.append(met_clus_et)
vars_list.append(met_clus_phi)
vars_list.append(met_clus_sumet)

# -----------------
# for muon studies
# -----------------

vars_list.append(muons_mTTot)
vars_list.append(muons_mVis)
vars_list.append(muons_mVisTot)
vars_list.append(muons_dphi)
vars_list.append(muons_deta)
vars_list.append(muons_dR)
vars_list.append(muons_chargeprod)
vars_list.append(muons_chargesum)
vars_list.append(muons_pTH)

vars_list.append(mulead_pt)
vars_list.append(mulead_eta)
vars_list.append(mulead_phi)
vars_list.append(mulead_trkd0)
vars_list.append(mulead_trkd0sig)
vars_list.append(mulead_trkz0)
vars_list.append(mulead_trkz0sintheta)
vars_list.append(mulead_ptvarcone30)

vars_list.append(musublead_pt)
vars_list.append(musublead_eta)
vars_list.append(musublead_phi)
vars_list.append(musublead_trkd0)
vars_list.append(musublead_trkd0sig)
vars_list.append(musublead_trkz0)
vars_list.append(musublead_trkz0sintheta)

# -------------------
# Muon tag-and-probe
# -------------------
"""
vars_list.append(tag_pt)
vars_list.append(probe_pt)
vars_list.append(probe_ptiso)
vars_list.append(probe_ptiso)
vars_list.append(probe_ujet_pt)
"""


# ---------------------
# just for muon fake-factors
# ---------------------
"""
vars_list.append(mujet_dphi)
vars_list.append(scdphi)
vars_list.append(jetlead_pt)
"""

# ---------------------
# for electron studies
# ---------------------

vars_list.append(electrons_mTtot)
vars_list.append(electrons_mVis)
vars_list.append(electrons_dphi)
vars_list.append(electrons_deta)
vars_list.append(electrons_chargeprod)

vars_list.append(elelead_pt)
vars_list.append(elelead_eta)
vars_list.append(elelead_phi)
vars_list.append(elelead_trkd0)
vars_list.append(elelead_trkd0sig)
vars_list.append(elelead_trkz0)
vars_list.append(elelead_trkz0sintheta)
vars_list.append(elelead_ptvarcone30)

vars_list.append(elesublead_pt)
vars_list.append(elesublead_eta)
vars_list.append(elesublead_phi)
vars_list.append(elesublead_trkd0)
vars_list.append(elesublead_trkd0sig)
vars_list.append(elesublead_trkz0)
vars_list.append(elesublead_trkz0sintheta)


# --------------------------
# for mixed channel studies
# -------------------------

vars_list.append(elemu_mTtot)
vars_list.append(elemu_mVis)
vars_list.append(elemu_dphi)
vars_list.append(elemu_deta)
vars_list.append(elemu_chargeprod)

vars_list.append(OSelemu_mTtot1)
vars_list.append(OSelemu_mVis1)
vars_list.append(OSelemu_dphi1)
vars_list.append(OSelemu_deta1)

vars_list.append(OSelemu_mTtot2)
vars_list.append(OSelemu_mVis2)
vars_list.append(OSelemu_dphi2)
vars_list.append(OSelemu_deta2)

vars_list.append(leplead_pt)
vars_list.append(leplead_eta)
vars_list.append(leplead_phi)
vars_list.append(leplead_trkd0)
vars_list.append(leplead_trkd0sig)
vars_list.append(leplead_trkz0)
vars_list.append(leplead_trkz0sintheta)

vars_list.append(lepsublead_pt)
vars_list.append(lepsublead_eta)
vars_list.append(lepsublead_phi)
vars_list.append(lepsublead_trkd0)
vars_list.append(lepsublead_trkd0sig)
vars_list.append(lepsublead_trkz0)
vars_list.append(lepsublead_trkz0sintheta)

vars_list.append(lep3_pt)
vars_list.append(lep3_eta)
vars_list.append(lep3_phi)
vars_list.append(lep3_trkd0)
vars_list.append(lep3_trkd0sig)
vars_list.append(lep3_trkz0)
vars_list.append(lep3_trkz0sintheta)
# ---------------------
# cutflows
# ---------------------
"""
vars_list.append(cutflow_presel)
vars_list.append(cutflow_weighted_presel)
vars_list.append(cutflow_ZCR)
vars_list.append(cutflow_weighted_ZCR)
"""

vars_dict = {}
for var in vars_list: vars_dict[var.name] = var.__dict__


## EOF



