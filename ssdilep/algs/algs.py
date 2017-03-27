#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
algs.py

This module contains a set of analysis specific algs 
for calculating variables, applying selection and 
plotting.
"""

## std modules
import itertools
import os
import math
import ROOT
from array import array

## logging
import logging
log = logging.getLogger(__name__)

## python
from itertools import combinations
import collections
from copy import copy
import sys

## pyframe
import pyframe

GeV = 1000.0

#------------------------------------------------------------------------------
class CutAlg(pyframe.core.Algorithm):
    """
    Filtering alg for applying a single cut.  The predefined cuts must be
    implemeneted as a function with the prefix "cut_". One can then specify the
    cut to be applied by passing the cut=<cut name> in the constructor, which
    will execture the cut_<cut name>() function.
    """
    #__________________________________________________________________________
    def __init__(self,
                 name     = None,
                 cut      = None,
                 cutflow  = None,
                 isfilter = True,
                 ):
        pyframe.core.Algorithm.__init__(self, name if name else cut,isfilter=isfilter)
        self.cutflow = cutflow
         
    #__________________________________________________________________________
    def execute(self, weight):
        pyframe.core.Algorithm.execute(self, weight)

        return self.apply_cut(self.name)

    #__________________________________________________________________________
    def apply_cut(self,cutname):
        if self.store.has_key(cutname): return self.store[cutname]
        cut_function = 'cut_%s'%cutname
        assert hasattr(self,cut_function),"cut %s doesnt exist!'"%(cutname)
        self.store[cutname] = result = getattr(self,cut_function)()
        return result
    #__________________________________________________________________________
    def cut_AtLeastTwoMuons(self):
      return self.chain.nmuon > 1
    #__________________________________________________________________________
    def cut_AtLeastTwoSSMuons(self):
      muons = self.store['muons']
      if self.chain.nmuon >= 2:
        for p in combinations(muons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: return True
      return False
    #__________________________________________________________________________
    def cut_AtLeastTwoSSMuonPairs(self):
      muons = self.store['muons']
      if self.chain.nmuon >= 4:
        for p in combinations(muons,4):
          if p[0].trkcharge * p[1].trkcharge * p[2].trkcharge * p[3].trkcharge > 0.0: return True
      return False
    #__________________________________________________________________________
    def cut_OddSSMuons(self):
      muons = self.store['muons']
      ss_pairs = []
      if self.chain.nmuon >= 2:
        for p in combinations(muons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: ss_pairs.append(p)
      if len(ss_pairs)==1 or len(ss_pairs)==3: return True
      return False
    #__________________________________________________________________________
    def cut_TwoSSMuonPairs(self):
      muons = self.store['muons']
      ss_pairs = []
      if self.chain.nmuon == 4:
        for p in combinations(muons,4):
          if p[0].trkcharge * p[1].trkcharge *p[2].trkcharge * p[3].trkcharge > 0.0: return True
      return False

    #__________________________________________________________________________
    def cut_OddOSMuons(self):
      muons = self.store['muons']
      os_pairs = []
      if self.chain.nmuon >= 2:
        for p in combinations(muons,2):
          if p[0].trkcharge * p[1].trkcharge < 0.0: os_pairs.append(p)
      if len(os_pairs)==1 or len(os_pairs)==3: return True
      return False
    
    #__________________________________________________________________________
    def cut_AtLeastOneMuPt28(self):
        muons = self.store['muons']
        for m in muons:
          if m.tlv.Pt()>28*GeV: return True
        return False
    #__________________________________________________________________________
    def cut_LeadMuPt30(self):
        muons = self.store['muons']
        return muons[0].tlv.Pt()>30*GeV
    #__________________________________________________________________________
    def cut_LeadMuPt28(self):
        muons = self.store['muons']
        return muons[0].tlv.Pt()>28*GeV
    #__________________________________________________________________________
    def cut_SubLeadMuPt28(self):
        muons = self.store['muons']
        return muons[1].tlv.Pt()>28*GeV
    #__________________________________________________________________________
    def cut_TagPt28(self):
        tag = self.store['tag']
        return tag.tlv.Pt()>28*GeV
    #__________________________________________________________________________
    def cut_OneMuon(self):
        return self.chain.nmuon == 1
    #__________________________________________________________________________
    def cut_TwoMuons(self):
        return self.chain.nmuon == 2
    #__________________________________________________________________________
    def cut_ThreeMuons(self):
        return self.chain.nmuon == 3
    #__________________________________________________________________________
    def cut_FourMuons(self):
        return self.chain.nmuon == 4
    
    #__________________________________________________________________________
    def cut_TwoSSMuons(self):
      muons  = self.store['muons']
      if len(muons)==2:
        if muons[0].trkcharge * muons[1].trkcharge > 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_TwoOSMuons(self):
      muons  = self.store['muons']
      if len(muons)==2:
        if muons[0].trkcharge * muons[1].trkcharge < 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_OneJet(self):
      if hasattr(self.chain,"njets"): return self.chain.njets == 1
      if hasattr(self.chain,"njet"):  return self.chain.njet == 1
    
    #__________________________________________________________________________
    def cut_JetCleaning(self):
      for j in self.store['jets']:
        if not j.isClean: return False
      return True
    
    #__________________________________________________________________________
    def cut_AllMuPt22(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and m.tlv.Pt()>=22.0*GeV
      return passed
    #__________________________________________________________________________
    def cut_AllMuPt25(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and m.tlv.Pt()>=25.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllMuPt28(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and m.tlv.Pt()>=28.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllMuPt30(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and m.tlv.Pt()>=30.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllMuEta247(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and abs(m.tlv.Eta())<2.47
      return passed
    #__________________________________________________________________________
    def cut_AllMuZ0SinTheta05(self):
      muons = self.store['muons']
      passed = True
      for m in muons:
        passed = passed and abs(m.trkz0sintheta)<0.5
      return passed
    
    #__________________________________________________________________________
    def cut_DCHFilter(self):
      lep_dict = { "Mm":-13, "Mp":13, "Em":-11, "Ep":11}
      if "DCH" in self.samplename:
        
        pdgId_sampl = []
        for s in self.samplename.split("_"):
          if "HL" in s: pdgId_sampl += [lep_dict[s.replace("HL","")[-2:]],lep_dict[s.replace("HL","")[:2]]]
          if "HR" in s: pdgId_sampl += [lep_dict[s.replace("HR","")[-2:]],lep_dict[s.replace("HR","")[:2]]]
        
        pdgId_branch = []
        if "HL" in self.samplename:
          for pdgId in self.chain.HLpp_Daughters: pdgId_branch += [pdgId]
          for pdgId in self.chain.HLmm_Daughters: pdgId_branch += [pdgId]
        if "HR" in self.samplename:
          for pdgId in self.chain.HRpp_Daughters: pdgId_branch += [pdgId]
          for pdgId in self.chain.HRmm_Daughters: pdgId_branch += [pdgId]
        
        pdgId_branch = filter(lambda pdgId: pdgId != 0, pdgId_branch) 
        
        if not collections.Counter(pdgId_branch) == collections.Counter(pdgId_sampl): return False
      return True

    #__________________________________________________________________________
    def cut_MuNoFilterTT(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      
      return lead_is_tight and sublead_is_tight
    #__________________________________________________________________________
    def cut_MuNoFilterTL(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)

      return lead_is_tight and sublead_is_loose 
    #__________________________________________________________________________
    def cut_MuNoFilterLT(self):
      muons = self.store['muons']
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)

      return lead_is_loose and sublead_is_tight
    #__________________________________________________________________________
    def cut_MuNoFilterLL(self):
      muons = self.store['muons']
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)

      return lead_is_loose and sublead_is_loose
    
    
    #__________________________________________________________________________
    def cut_MuUniTT(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuUniTL(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuUniLT(self):
      muons = self.store['muons']
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_loose and sublead_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuUniLL(self):
      muons = self.store['muons']
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      pass_mc_filter   = True

      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_loose and sublead_is_loose and pass_mc_filter
        
    #__________________________________________________________________________
    def cut_MuTT(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTL(self):
      muons = self.store['muons']
      lead_is_tight    = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = sublead_is_real   

      return lead_is_tight and sublead_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLT(self):
      muons = self.store['muons']
      sublead_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter = lead_is_real   

      return lead_is_loose and sublead_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLL(self):
      muons = self.store['muons']
      lead_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      sublead_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      pass_mc_filter   = True

      if self.sampletype=="mc":
        lead_is_real     = muons[0].isTrueIsoMuon()
        sublead_is_real  = muons[1].isTrueIsoMuon()
        pass_mc_filter   = lead_is_real or sublead_is_real     

      return lead_is_loose and sublead_is_loose and pass_mc_filter
    
    
    #__________________________________________________________________________
    def cut_MuTTT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTipghtTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real   

      return mu0_is_tight and mu1_is_tight and mu2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTTL(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_loose     = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_tight and mu1_is_tight and mu2_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTLT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_loose     = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_tight and mu1_is_loose and mu2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLTT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_loose     = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_loose and mu1_is_tight and mu2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLLT(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_loose     = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      mu1_is_loose     = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      mu2_is_tight     = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_loose and mu1_is_loose and mu2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLTL(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_loose     = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      mu1_is_tight     = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      mu2_is_loose     = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_loose and mu1_is_tight and mu2_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuTLL(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_tight     = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      mu1_is_loose     = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      mu2_is_loose     = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_tight and mu1_is_loose and mu2_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_MuLLL(self):
      muons = self.store['muons']
      if len(muons) < 3: return False
      
      mu0_is_loose     = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      mu1_is_loose     = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      mu2_is_loose     = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        mu0_is_real      = muons[0].isTrueIsoMuon()
        mu1_is_real      = muons[1].isTrueIsoMuon()
        mu2_is_real      = muons[2].isTrueIsoMuon()
        pass_mc_filter   = mu0_is_real and mu1_is_real and mu2_is_real

      return mu0_is_loose and mu1_is_loose and mu2_is_loose and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_AllMuMedium(self):
      muons = self.store['muons']
      for m in muons:
        is_medium = bool(m.isMedium) or bool(m.isTight)
        if not is_medium: return False
      return True
    #__________________________________________________________________________
    def cut_AllMuLoose(self):
      muons = self.store['muons']
      for m in muons:
        is_loose = bool(m.isLoose) or bool(m.isMedium) or bool(m.isTight)
        if not is_loose: return False
      return True
    
    #__________________________________________________________________________
    def cut_LeadMuIsLoose(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      is_loose = bool(lead_mu.isLoose) or bool(lead_mu.isMedium) or bool(lead_mu.isTight)
      return is_loose
    #__________________________________________________________________________
    def cut_LeadMuIsMedium(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      is_medium = bool(lead_mu.isMedium) or bool(lead_mu.isTight)
      return is_medium
    #__________________________________________________________________________
    def cut_LeadMuIsTight(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      is_tight = bool(lead_mu.isTight)
      return is_tight
    
    #__________________________________________________________________________
    def cut_LeadMuIsoFixedCutTightTrackOnly(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return lead_mu.isIsolated_FixedCutTightTrackOnly
    #__________________________________________________________________________
    def cut_LeadMuIsoNotFixedCutTightTrackOnly(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return not lead_mu.isIsolated_FixedCutTightTrackOnly
    
    #__________________________________________________________________________
    def cut_LeadMuIsoGradient(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return lead_mu.isIsolated_Gradient
    #__________________________________________________________________________
    def cut_LeadMuIsoNotGradient(self):
      muons = self.store['muons']
      lead_mu = muons[0]
      return not lead_mu.isIsolated_Gradient 
    
    
    #__________________________________________________________________________
    def cut_AllMuIsoBound08(self):
      muons = self.store['muons']
      for m in muons:
        if m.ptvarcone30 / m.tlv.Pt() > 0.8: return False
      return True
    #__________________________________________________________________________
    def cut_AllMuIsoBound15(self):
      muons = self.store['muons']
      for m in muons:
        if m.ptvarcone30 / m.tlv.Pt() > 1.5: return False
      return True
    
    
    #__________________________________________________________________________
    def cut_MZwindow(self):
      mZ = 91.1876*GeV
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis - mZ) < 10*GeV
    
    #__________________________________________________________________________
    def cut_VetoMZwindow(self):
      mZ = 91.1876*GeV
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis - mZ) > 20 * GeV
    
    #__________________________________________________________________________
    def cut_AllPairsM20(self):
      muons = self.store['muons']
      if self.chain.nmuon >= 2:
        for p in combinations(muons,2):
          if (p[0].tlv + p[1].tlv).M()<20*GeV: return False
      return True
    
    
    #__________________________________________________________________________
    def cut_M15(self):
      muons = self.store['muons']
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis)>15*GeV
    
    #__________________________________________________________________________
    def cut_Mlow200(self):
      muons = [self.store['muon1'],self.store['muon2']]
      mu_lead = muons[0] 
      mu_sublead = muons[1] 
      m_vis = (mu_lead.tlv + mu_sublead.tlv).M()

      return abs(m_vis)<200*GeV
    
    #__________________________________________________________________________
    def cut_SingleMuPassAndMatch(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["SingleMuTrigIndex"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["SingleMuTrigIndex"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered: 
              return True  
      return False

    #__________________________________________________________________________
    def cut_DiElePass(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      for trig in required_triggers:
        if trig in passed_triggers: return True
      return False      
    
    #__________________________________________________________________________
    def cut_PassMixed(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      for trig in required_triggers:
          if trig in passed_triggers: return True
      return False      

    #__________________________________________________________________________
    def cut_TagIsMatched(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      tag = self.store['tag'] 
      for trig in required_triggers:
        if trig in self.store["SingleMuTrigIndex"].keys():
          tag_is_matched     = bool( tag.isTrigMatchedToChain.at(self.store["SingleMuTrigIndex"][trig]) )
          event_is_triggered = bool( trig in passed_triggers )
          if tag_is_matched and event_is_triggered: 
            return True
      return False
    
    #__________________________________________________________________________
    def cut_LeadIsMatched(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      lead_mu = self.store['muons'][0]
      for trig in required_triggers:
        if trig in self.store["SingleMuTrigIndex"].keys():
          lead_mu_is_matched = bool( lead_mu.isTrigMatchedToChain.at(self.store["SingleMuTrigIndex"][trig]) )
          event_is_triggered = bool( trig in passed_triggers )
          if lead_mu_is_matched and event_is_triggered: 
            return True
      return False
    #__________________________________________________________________________
    def cut_SubLeadIsMatched(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      sublead_mu = self.store['muons'][1]
      for trig in required_triggers:
        if trig in self.store["SingleMuTrigIndex"].keys():
          sublead_mu_is_matched = bool( sublead_mu.isTrigMatchedToChain.at(self.store["SingleMuTrigIndex"][trig]) )
          event_is_triggered = bool( trig in passed_triggers )
          if sublead_mu_is_matched and event_is_triggered: 
            return True

    #__________________________________________________________________________
    def cut_SingleMuPassAndMatchPresc(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      muons = self.store['muons']
      for m in muons:
        for trig in required_triggers:
          if trig in self.store["SingleMuTrigIndex"].keys():
            muon_is_matched    = bool( m.isTrigMatchedToChain.at(self.store["SingleMuTrigIndex"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if muon_is_matched and event_is_triggered:
              if m.tlv.Pt()>=self.store["SingleMuTrigSlice"][trig][0] and m.tlv.Pt()<self.store["SingleMuTrigSlice"][trig][1]:
                return True
      return False
    
    
    #__________________________________________________________________________
    def cut_LeadMuTruthFilter(self):
      muons = self.store['muons'] 
      if self.sampletype == "mc":
        return muons[0].isTrueIsoMuon()
      return True
    #__________________________________________________________________________
    def cut_LeadMuFakeFilter(self):
      muons = self.store['muons'] 
      if self.sampletype == "mc":
        return muons[0].isTrueNonIsoMuon()
      return True
    #__________________________________________________________________________
    def cut_ProbeTruthFilter(self):
      if self.sampletype == "mc":
        return self.store['probe'].isTrueIsoMuon()
      return True
    #__________________________________________________________________________
    def cut_ProbeMuFakeFilter(self):
      if self.sampletype == "mc":
        return self.store['probe'].isTrueNonIsoMuon()
      return True
    #__________________________________________________________________________
    def cut_ProbeMuFailTruthFilter(self):
      if self.sampletype == "mc":
        return not self.store['probe'].isTrueIsoMuon()
      return True
    #__________________________________________________________________________
    def cut_TagAndProbeExist(self):
      if "tag" in self.store.keys() and "probe" in self.store.keys():
        return True
      return False
    #__________________________________________________________________________
    def cut_TagisTight(self):
      return self.store['tag'].isIsolated_FixedCutTightTrackOnly and self.store['tag'].trkd0sig<3.
    #__________________________________________________________________________
    def cut_TagisLoose(self):
      return not self.store['tag'].isIsolated_FixedCutTightTrackOnly and self.store['tag'].trkd0sig<10.
    #__________________________________________________________________________
    def cut_ProbeisTight(self):
      return self.store['probe'].isIsolated_FixedCutTightTrackOnly and self.store['probe'].trkd0sig<3.
    #__________________________________________________________________________
    def cut_ProbeisLoose(self):
      return not self.store['probe'].isIsolated_FixedCutTightTrackOnly and self.store['probe'].trkd0sig<10.
   
    
    #__________________________________________________________________________
    def cut_LeadMuD0Sig2(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<2. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig3(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<3. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig4(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<4. 
    #__________________________________________________________________________
    def cut_LeadMuD0Sig10(self):
      muons = self.store['muons']
      return muons[0].trkd0sig<10. 
    
    #__________________________________________________________________________
    def cut_LeadMuZ0SinTheta05(self):
      muons = self.store['muons']
      return abs(muons[0].trkz0sintheta)<0.5
    
    #__________________________________________________________________________
    def cut_METlow40(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 40 * GeV
    #__________________________________________________________________________
    def cut_METlow50(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 50 * GeV
    #__________________________________________________________________________
    def cut_METlow30(self):
      met = self.store["met_clus"]
      return met.tlv.Pt() < 30 * GeV
    
    #__________________________________________________________________________
    def cut_MuJetDphi27(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.7
      else: return False
    #__________________________________________________________________________
    def cut_MuJetDphi28(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.8
      else: return False
    #__________________________________________________________________________
    def cut_MuJetDphi26(self):
      lead_mu = self.store["muons"][0]
      lead_jet = None
      if self.store["jets"]:
        lead_jet = self.store["jets"][0]
      if lead_jet:
        return abs(lead_mu.tlv.DeltaPhi(lead_jet.tlv)) > 2.6
      else: return False
    
    #__________________________________________________________________________
    def cut_AllJetPt25(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 25 * GeV: return False
      return True
    #__________________________________________________________________________
    def cut_AllJetPt35(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 35 * GeV: return False
      return True
    #__________________________________________________________________________
    def cut_AllJetPt40(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 40 * GeV: return False
      return True
    #__________________________________________________________________________
    def cut_AllJetPt45(self):
      if self.store["jets"]:
        jets = self.store["jets"]
        for j in jets:
          if j.tlv.Pt() < 45 * GeV: return False
      return True
    #__________________________________________________________________________
    def cut_BadJetVeto(self):
        jets = self.store['jets']
        for jet in jets:
          if not jet.isClean:
            return False
        return True
    #__________________________________________________________________________
    def cut_OneOrTwoBjets(self):
        nbjets = 0
        jets = self.store['jets']
        for jet in jets:
          if jet.isFix77:
            nbjets += 1
        if nbjets in [1,2]:
          return True
        else:
          return False

    #__________________________________________________________________________

    def cut_BadJetVeto(self):
        jets = self.store['jets']
        for jet in jets:
          if not jet.isClean:
            return False
        return True

    #__________________________________________________________________________
    #
    # Electron cuts from the old framework
    #__________________________________________________________________________    


    def cut_AtLeastOneLooseElectrons(self):
        return self.chain.nel > 0
    #__________________________________________________________________________  
         
    def cut_AtLeastTwoLooseElectrons(self):
        return self.chain.nel > 1

    #__________________________________________________________________________                    
    def cut_OneLooseElectron(self):
        return self.chain.nel == 1

    #__________________________________________________________________________                   
    def cut_TwoLooseElectrons(self):
        return self.chain.nel == 2


    #__________________________________________________________________________
    # continue here with cut_LeadElectronIsLoose(self) etc from the old framework

    #__________________________________________________________________________
    #
    # New cuts for electros
    #__________________________________________________________________________

    #__________________________________________________________________________
    def cut_AtLeastTwoElectrons(self):
      return self.chain.nel > 1
    #__________________________________________________________________________
    def cut_AtLeastTwoSSElectrons(self):
      electrons = self.store['electrons_loose']
      if self.chain.nel >= 2:
        for p in combinations(electrons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: return True
      return False
    #__________________________________________________________________________
    def cut_AtLeastTwoSSElePairs(self):
      electrons = self.store['electrons_loose']
      if self.chain.nel >= 4:
        for p in combinations(electrons,4):
          if p[0].trkcharge * p[1].trkcharge * p[2].trkcharge * p[3].trkcharge > 0.0: return True
      return False
    #__________________________________________________________________________
    def cut_FourLeptons(self):
        if((len(self.store['electrons_loose'])==4 and len(self.store['muons'])==0) or (len(self.store['electrons_loose'])==0 and len(self.store['muons'])==4) or (len(self.store['electrons_loose'])==2 and len(self.store['muons'])==2) or (len(self.store['electrons_loose'])==3 and len(self.store['muons'])==1) or (len(self.store['electrons_loose'])==1 and len(self.store['muons'])==3)): return True
        return False
    #__________________________________________________________________________
    def cut_OneElectron(self):
        return self.chain.nel == 1
    #__________________________________________________________________________
    def cut_TwoElectrons(self):
        return len(self.store['electrons_loose']) == 2
    #__________________________________________________________________________
    def cut_ThreeElectrons(self):
        return len(self.store['electrons_loose']) == 3
    #__________________________________________________________________________
    def cut_FourElectrons(self):
        return len(self.store['electrons_loose']) == 4 and len(self.store['muons'])==0
    #__________________________________________________________________________
    def cut_OneElectronOneMuon(self):
        if(len(self.store['electrons_loose'])==1 and len(self.store['muons'])==1):return True
        return False
    #__________________________________________________________________________
    def cut_TwoElectronsTwoMuons(self):
        return (len(self.store['electrons_loose'])==2 and len(self.store['muons'])==2)
    #__________________________________________________________________________
    def cut_ThreeElectronsOneMuon(self):
        return (len(self.store['electrons_loose'])==3 and len(self.store['muons'])==1)
    #__________________________________________________________________________
    def cut_OneElectronsThreeMuons(self):
        return (len(self.store['electrons_loose'])==1 and len(self.store['muons'])==3)
    #__________________________________________________________________________
    def cut_ZeroTotalCharge(self):
        electrons = self.store['electrons_loose']
        muons     = self.store['muons']
        leptons = electrons + muons
        totalCharge=0.
        for l in leptons:
            totalCharge = totalCharge + l.trkcharge
        if(totalCharge==0): return True
        return False
    #__________________________________________________________________________
    def cut_TwoSSElectrons(self):
      electrons  = self.store['electrons_loose']
      if len(electrons)==2:
        if electrons[0].trkcharge * electrons[1].trkcharge > 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_TwoOSElectrons(self):
      electrons  = self.store['electrons_loose']
      if len(electrons)==2:
        if electrons[0].trkcharge * electrons[1].trkcharge < 0.0:
          return True
      return False

    #__________________________________________________________________________
    def cut_EleTT(self):
      electrons = self.store['electrons_loose']
      lead_is_tight    = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      sublead_is_tight = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = electrons[0].isTrueIsoElectron()
        sublead_is_real  = electrons[1].isTrueIsoElectron()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleTT(self):
      electrons = self.store['electrons_loose']
      lead_is_tight    = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      sublead_is_tight = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = electrons[0].isTrueIsoElectron()
        sublead_is_real  = electrons[1].isTrueIsoElectron()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleTL(self):
      electrons = self.store['electrons_loose']
      lead_is_tight    = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      sublead_is_loose = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = electrons[0].isTrueIsoElectron()
        sublead_is_real  = electrons[1].isTrueIsoElectron()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_tight and sublead_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleLT(self):
      electrons = self.store['electrons_loose']
      lead_is_loose    = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      sublead_is_tight = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = electrons[0].isTrueIsoElectron()
        sublead_is_real  = electrons[1].isTrueIsoElectron()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_loose and sublead_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleLL(self):
      electrons = self.store['electrons_loose']
      lead_is_loose    = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      sublead_is_loose = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        lead_is_real     = electrons[0].isTrueIsoElectron()
        sublead_is_real  = electrons[1].isTrueIsoElectron()
        pass_mc_filter   = lead_is_real and sublead_is_real     

      return lead_is_loose and sublead_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleTTT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_tight and ele1_is_tight and ele2_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleTTL(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_loose     = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_tight and ele1_is_tight and ele2_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleTLT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose     = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_tight and ele1_is_loose and ele2_is_tight and pass_mc_filter
    #__________________________________________________________________________
    def cut_EleLTT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_loose     = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_loose and ele1_is_tight and ele2_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleTLL(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose     = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_loose     = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_tight and ele1_is_loose and ele2_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleLLT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_loose     = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_loose     = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_loose and ele1_is_loose and ele2_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleLTL(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_loose     = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_loose     = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_loose and ele1_is_tight and ele2_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_EleLLL(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 3: return False
      
      ele0_is_loose     = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_loose     = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_loose     = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real   

      return ele0_is_loose and ele1_is_loose and ele2_is_loose and pass_mc_filter
    #__________________________________________________________________________
    def cut_EleTTTT(self):
        
      electrons = self.store['electrons_loose']
      if len(electrons) < 4: return False

      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      ele3_is_tight     = bool(electrons[3].isIsolated_Loose and electrons[3].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        ele3_is_real      = electrons[3].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real and ele3_is_real

      return ele0_is_tight and ele1_is_tight and ele2_is_tight and ele3_is_tight and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_EleTTTL(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 4: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      ele3_is_loose     = bool(not (electrons[3].isIsolated_Loose and electrons[3].LHMedium))
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele3_is_real      = electrons[3].isTrueIsoElectron()
        pass_mc_filter   = ele3_is_real

      return ele0_is_tight and ele1_is_tight and ele2_is_tight and ele3_is_loose and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_EleTTLT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 4: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_loose     = bool(not (electrons[2].isIsolated_Loose and electrons[2].LHMedium))
      ele3_is_tight     = bool(electrons[3].isIsolated_Loose and electrons[3].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele2_is_real      = electrons[2].isTrueIsoElectron()
        pass_mc_filter   = ele2_is_real

      return ele0_is_tight and ele1_is_tight and ele2_is_loose and ele3_is_tight and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_EleTLTT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 4: return False
      
      ele0_is_tight     = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose     = bool(not (electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      ele3_is_tight     = bool(electrons[3].isIsolated_Loose and electrons[3].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele1_is_real      = electrons[1].isTrueIsoElectron()
        pass_mc_filter   = ele1_is_real

      return ele0_is_tight and ele1_is_loose and ele2_is_tight and ele3_is_tight and pass_mc_filter
    
    #__________________________________________________________________________
    def cut_EleLTTT(self):
      electrons = self.store['electrons_loose']
      if len(electrons) < 4: return False
      
      ele0_is_loose     = bool(not (electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_tight     = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight     = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      ele3_is_tight     = bool(electrons[3].isIsolated_Loose and electrons[3].LHMedium)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real      = electrons[0].isTrueIsoElectron()
        pass_mc_filter   = ele0_is_real

      return ele0_is_loose and ele1_is_tight and ele2_is_tight and ele3_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleMuTT(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      ele_is_tight    = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      muon_is_tight   = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele_is_real     = electrons[0].isTrueIsoElectron()
        muon_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele_is_real and muon_is_real     

      return ele_is_tight and muon_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleMuLT(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      ele_is_loose    = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      muon_is_tight   = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele_is_real     = electrons[0].isTrueIsoElectron()
        muon_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele_is_real and muon_is_real     

      return ele_is_loose and muon_is_tight and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleMuTL(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      ele_is_tight    = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      muon_is_loose   = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele_is_real     = electrons[0].isTrueIsoElectron()
        muon_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele_is_real and muon_is_real     

      return ele_is_tight and muon_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_EleMuLL(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      ele_is_loose    = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      muon_is_loose   = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele_is_real     = electrons[0].isTrueIsoElectron()
        muon_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele_is_real and muon_is_real     

      return ele_is_loose and muon_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_AllElePt25(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and m.tlv.Pt()>=25.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllElePt28(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and m.tlv.Pt()>=28.0*GeV
      return passed
    
    #__________________________________________________________________________
    def cut_AllElePt30(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and m.tlv.Pt()>=30.0*GeV
      return passed
    #__________________________________________________________________________

    def cut_AtLeastOneElePt28(self):
        electrons = self.store['electrons_loose']
        for m in electrons:
          if m.tlv.Pt()>28*GeV: return True
        return False

    #_________________________________________________________________________

    def cut_AtLeastOneElePt30(self):
        electrons = self.store['electrons_loose']
        for m in electrons:
           if m.tlv.Pt()>30*GeV: return True
        return False
   
    #__________________________________________________________________________
    def cut_LeadElePt30(self):
        electrons = self.store['electrons_loose']
        return electrons[0].tlv.Pt()>30*GeV
    #__________________________________________________________________________
    def cut_LeadElePt28(self):
        electrons = self.store['electrons_loose']
        return electrons[0].tlv.Pt()>28*GeV
    #__________________________________________________________________________
    def cut_SubLeadElePt28(self):
        electrons = self.store['electrons_loose']
        return electrons[1].tlv.Pt()>28*GeV

    #_________________________________________________________________________

    def cut_SubLeadElePt30(self):
        electrons = self.store['electrons_loose']
        return electrons[1].tlv.Pt()>30*GeV

    #__________________________________________________________________________
    def cut_AllEleLHMedium(self):
      electrons = self.store['electrons_loose']
      for m in electrons:
        is_medium = bool(m.LHMedium) or bool(m.LHTight)
        if not is_medium: return False
      return True

    #__________________________________________________________________________
    def cut_AllEleLHLoose(self):
      electrons = self.store['electrons_loose']
      for m in electrons:
        is_loose = bool(m.LHLoose)
        if not is_loose: return False
      return True

    #__________________________________________________________________________

    def cut_AllEleLHTight(self):
      electrons = self.store['electrons_loose']
      for m in electrons:
        is_tight = bool(m.LHTight)
        if not is_tight: return False
      return True    

    #__________________________________________________________________________
    def cut_AllEleIsolatedLoose(self):
      electrons = self.store['electrons_loose']
      for m in electrons:
        is_IsolatedLoose = bool(m.Isolated_Loose)
        if not is_IsolatedLoose: return False
      return True

    #__________________________________________________________________________
    def cut_LeadEleIsIsolatedLoose(self):
      electrons = self.store['electrons_loose']
      lead_el = electrons[0]
      is_IsolatedLoose = bool(lead_el.Isolated_Loose)
      return is_IsolatedLoose

    #__________________________________________________________________________
    def cut_SubLeadEleIsIsolatedLoose(self):
      electrons = self.store['electrons_loose']
      sublead_el = electrons[1]
      is_IsolatedLoose = bool(sublead_el.Isolated_Loose)
      return is_IsolatedLoose

    #__________________________________________________________________________
    def cut_LeadEleIsLHLoose(self):
      electrons = self.store['electrons_loose']
      lead_el = electrons[0]
      is_LHloose = bool(lead_el.LHLoose) or bool(lead_el.LHMedium) or bool(lead_el.LHTight)
      return is_LHloose

    #__________________________________________________________________________
    def cut_LeadEleIsLHMedium(self):
      electrons = self.store['electrons_loose']
      lead_el = electrons[0]
      is_LHmedium = bool(lead_el.LHMedium) or bool(lead_el.LHTight)
      return is_LHmedium

    #__________________________________________________________________________
    def cut_LeadEleIsLHTight(self):
      electrons = self.store['electrons_loose']
      lead_el = electrons[0]
      is_LHtight = bool(lead_el.LHTight)
      return is_LHtight

    #___________________________________________________________________________

    def cut_OddSSElectrons(self):
      electrons = self.store['electrons_loose']
      ss_pairs = []
      if len(electrons) >= 2:
        for p in combinations(electrons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: ss_pairs.append(p)
      if len(ss_pairs)==1 or len(ss_pairs)==3: return True
      return False
    #___________________________________________________________________________

    def cut_TwoSSElectronPairs(self):
      electrons = self.store['electrons_loose']
      ss_pairs = []
      if len(electrons)==4:
        for p in combinations(electrons,4):
          if p[0].trkcharge * p[1].trkcharge * p[2].trkcharge * p[3].trkcharge > 0.0: return True
      return False
    #___________________________________________________________________________

    def cut_OddOSElectrons(self):
      electrons = self.store['electrons_loose']
      os_pairs = []
      if len(electrons) >= 2:
        for p in combinations(electrons,2):
          if p[0].trkcharge * p[1].trkcharge < 0.0: os_pairs.append(p)
      if len(os_pairs)==1 or len(os_pairs)==3: return True
      return False

    #___________________________________________________________________________

    def cut_OddSSElectronMuon(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      ss_pairs = []
      leptons = electrons + muons
      print len(leptons)
      if len(leptons) >= 2:
        for p in combinations(leptons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: ss_pairs.append(p)
      if len(ss_pairs)==1 or len(ss_pairs)==3: return True
      return False
    #___________________________________________________________________________

    def cut_TwoSSElectronMuonPairsEEMM(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      ss_pairs = []
      leptons = electrons + muons

      if len(electrons) == 2 and len(muons)== 2:
        ss_electrons = electrons[0].trkcharge * electrons[1].trkcharge
        ss_muons     = muons[0].trkcharge * muons[1].trkcharge
        for p in combinations(leptons,4):
          if p[0].trkcharge * p[1].trkcharge *p[2].trkcharge * p[3].trkcharge and (ss_electrons > 0.0 and ss_muons > 0.0) > 0.0:  return True
      return False

    #___________________________________________________________________________

    def cut_TwoSSElectronMuonPairsEMEM(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      ss_pairs = []
      leptons = electrons + muons

      if len(electrons) == 2 and len(muons)==2:
        for p in combinations(leptons,4):
          ss_elemu = (electrons[0].trkcharge * muons[0].trkcharge > 0.0)or(electrons[0].trkcharge * muons[1].trkcharge > 0.0)or(electrons[1].trkcharge * muons[0].trkcharge > 0.0)
          if p[0].trkcharge * p[1].trkcharge *p[2].trkcharge * p[3].trkcharge  and (ss_elemu) > 0.0:  return True
      return False
    #___________________________________________________________________________

    def cut_TwoSSElectronMuonPairsEEEM(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      ss_pairs = []
      leptons = electrons + muons

      if len(electrons) == 3 and len(muons)== 1:
        ss_electrons = (electrons[0].trkcharge*electrons[1].trkcharge>0.0)or(electrons[0].trkcharge*electrons[2].trkcharge>0.0)or(electrons[1].trkcharge*electrons[2].trkcharge>0.0)
        ss_elemu     = (muons[0].trkcharge*electrons[0].trkcharge>0.0)or(muons[0].trkcharge*electrons[1].trkcharge>0.0)or(muons[0].trkcharge*electrons[2].trkcharge>0.0)
        for p in combinations(leptons,4):
          if p[0].trkcharge * p[1].trkcharge *p[2].trkcharge * p[3].trkcharge and (ss_electrons and ss_elemu) > 0.0:  return True
      return False
    #___________________________________________________________________________

    def cut_TwoSSElectronMuonPairsMMEM(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      ss_pairs = []
      leptons = electrons + muons

      if len(electrons) == 1 and len(muons)== 3:
        ss_muons = (muons[0].trkcharge*muons[1].trkcharge>0.0)or(muons[0].trkcharge*muons[2].trkcharge>0.0)or(muons[1].trkcharge*muons[2].trkcharge>0.0)
        ss_elemu     = (muons[0].trkcharge*electrons[0].trkcharge>0.0)or(muons[1].trkcharge*electrons[0].trkcharge>0.0)or(muons[2].trkcharge*electrons[0].trkcharge>0.0)
        for p in combinations(leptons,4):
          if p[0].trkcharge * p[1].trkcharge *p[2].trkcharge * p[3].trkcharge and (ss_muons and ss_elemu) > 0.0:  return True
      return False
    #___________________________________________________________________________

    def cut_OddSSElectronMuon(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      ss_pairs = []
      leptons = electrons + muons
      if len(leptons) >= 2:
        for p in combinations(leptons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: ss_pairs.append(p)
      if len(ss_pairs)==1 or len(ss_pairs)==3: return True
      return False

    #___________________________________________________________________________

    def cut_OddOSElectronMuon(self):
      electrons = self.store['electrons_loose']
      muons     = self.store['muons']
      os_pairs = []
      leptons = electrons + muons
      if len(leptons) >= 2:
        for p in combinations(leptons,2):
          if p[0].trkcharge * p[1].trkcharge < 0.0: os_pairs.append(p)
      if len(os_pairs)==1 or len(os_pairs)==3: return True
      return False

   #____________________________________________________________________________

    def cut_AllElePairsM20(self):
      electrons = self.store['electrons_loose']
      if self.chain.nel >= 2:
        for p in combinations(electrons,2):
          if (p[0].tlv + p[1].tlv).M()<20*GeV: return False
      return True

  #____________________________________________________________________________

    def cut_AllElePt30(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and m.tlv.Pt()>30*GeV
      return passed

  #__________________________________________________________________________
    
    def cut_Mass130GeV(self):
        electrons = self.store['electrons_loose']
        if (electrons[0].tlv + electrons[1].tlv).M() > 130*GeV: return True
        return False

  #__________________________________________________________________________
    
    def cut_MassBelow200GeV(self):
        electrons = self.store['electrons_loose']
        muons     = self.store['muons']
        leptons   = electrons + muons
        if (leptons[0].tlv + leptons[1].tlv).M() < 200*GeV: return True
        return False

    #__________________________________________________________________________

    def cut_AllEleEta247AndNotCrackRegion(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and abs(m.tlv.Eta())<2.47 and not(1.37<abs(m.tlv.Eta())<1.52)
      return passed

    #__________________________________________________________________________

    def cut_AllEleZ0SinTheta05(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and abs(m.trkz0sintheta)<0.5
      return passed

    #__________________________________________________________________________

    def cut_AllEleTrkd0Sig5(self):
      electrons = self.store['electrons_loose']
      passed = True
      for m in electrons:
        passed = passed and abs(m.trkd0sig)<5
      return passed

    #__________________________________________________________________________

    def cut_AllEleIsoBound15(self):
      electrons = self.store['electrons_loose']
      for m in electrons:
        if m.ptvarcone30 / m.tlv.Pt() > 1.5: return False
      return True

    #__________________________________________________________________________

    def cut_EleMass130GeV(self):
        electrons = self.store['electrons_loose']
        if len(electrons)==2 :
          if (electrons[0].tlv + electrons[1].tlv).M() > 130*GeV:
            return True;
        return False

    #__________________________________________________________________________

    def cut_EleMass130GeV200(self):
      electrons = self.store['electrons_loose']
      if len(electrons)==2 :
          tempMass = (electrons[0].tlv + electrons[1].tlv).M()
          if tempMass > 130*GeV and tempMass < 200*GeV :
            return True;
      return False

    #__________________________________________________________________________

    def cut_SingleElePassAndMatch(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      electrons = self.store['electrons_loose']
      for m in electrons:
         for trig in required_triggers:
            if trig in self.store["SingleEleTrigIndex"].keys():
               ele_is_matched = bool( m.isTrigMatchedToChain.at(self.store["SingleEleTrigIndex"][trig]) )
               event_is_triggered = bool ( trig in passed_triggers )
               if ele_is_matched and event_is_triggered:
                   return True

      return False

     #_________________________________________________________________________

    def cut_SubLeadEleIsMatched(self):

      required_triggers = self.store["reqTrig"]
      passed_triggers = self.store["passTrig"].keys()

      sublead_ele = self.store['electrons_loose'][1]
      for trig in required_triggers:
         if trig in self.store["SingleEleTrigIndex"].keys():
             sublead_ele_is_matched = bool (sublead_ele.isTrigMatchedToChain.at(self.store["SingleEleTrigIndex"][trig]) )
             event_is_triggered = bool( trig in passed_triggers )
             if sublead_ele_is_matched and event_is_triggered:
                return True
      return False
    #__________________________________________________________________________
    def cut_TagEleIsMatched(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      tag = self.store['tag'] 
      for trig in required_triggers:
        if trig in self.store["SingleEleTrigIndex"].keys():
          tag_is_matched     = bool( tag.isTrigMatchedToChain.at(self.store["SingleEleTrigIndex"][trig]) )
          event_is_triggered = bool( trig in passed_triggers )
          if tag_is_matched and event_is_triggered: 
            return True
      return False
    #__________________________________________________________________________
    def cut_LeadEleIsMatched(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()
      
      lead_ele = self.store['electrons_loose'][0]
      for trig in required_triggers:
        if trig in self.store["SingleEleTrigIndex"].keys():
          lead_ele_is_matched = bool( lead_ele.isTrigMatchedToChain.at(self.store["SingleEleTrigIndex"][trig]) )
          event_is_triggered = bool( trig in passed_triggers )
          if lead_ele_is_matched and event_is_triggered: 
            return True
      return False

    #__________________________________________________________________________
    def cut_SingleElePassAndMatchPresc(self):
      required_triggers = self.store["reqTrig"]
      passed_triggers   = self.store["passTrig"].keys()

      electrons = self.store['electrons_loose']
      for m in electrons:
        for trig in required_triggers:
          if trig in self.store["SingleEleTrigIndex"].keys():
            ele_is_matched     = bool( m.isTrigMatchedToChain.at(self.store["SingleEleTrigIndex"][trig]) )
            event_is_triggered = bool( trig in passed_triggers )
            if ele_is_matched and event_is_triggered:
              if m.tlv.Pt()>=self.store["SingleEleTrigSlice"][trig][0] and m.tlv.Pt()<self.store["SingleEleTrigSlice"][trig][1]:
                return True
      return False


     #________________________________________________________________________


    #__________________________________________________________________________
    #
    # Mixed channel cuts
    #__________________________________________________________________________    


    def cut_AtLeastOneLooseLepton(self):
        if ((self.chain.nel>0) or (self.chain.nmuon>0)): return True;

    #__________________________________________________________________________  
         
    def cut_AtLeastTwoLooseLeptons(self):
        if ((self.chain.nel>=1 and self.chain.nmuon>=1) or (self.chain.nel==0 and self.chain.nmuon>=2) or (self.chain.nel>=2 and self.chain.nmuon==0)): return True;

    #__________________________________________________________________________                    
    def cut_OneLooseLepton(self):
        if ((self.chain.nel == 1) or (self.chain.nmuon ==1)): return True;

    #__________________________________________________________________________

    def cut_TwoLooseLeptons(self):
        if ((self.chain.nel==1 and self.chain.nmuon==1) or (self.chain.nel==0 and self.chain.nmuon==2) or (self.chain.nel==2 and self.chain.nmuon==0)): return True;
    #__________________________________________________________________________

    def cut_ExatlyTwoSSLeptons(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      if self.chain.nel == 2:
        for p in combinations(electrons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: return True
      if self.chain.nmuon == 2:
        for p in combinations(muons,2):
          if p[0].trkcharge * p[1].trkcharge > 0.0: return True
      if (self.chain.nel == 1 and self.chain.nmuon ==1):
          if electrons[0].trkcharge * muons[0].trkcharge > 0.0: return True     
      return False

    #__________________________________________________________________________
    def cut_OneEleMuonPair(self):
        if (self.chain.nel == 1 and self.chain.nmuon ==1): return True

    #__________________________________________________________________________
    def cut_OneSSEleMuonPair(self):
      electrons  = self.store['electrons_loose']
      muons = self.store['muons']
      if (len(electrons)==1 and len(muons)==1):
        if electrons[0].trkcharge * muons[0].trkcharge > 0.0:
          return True
      return False
    
    #__________________________________________________________________________
    def cut_OneOSEleMuonPair(self):
      electrons  = self.store['electrons_loose']
      muons = self.store['muons']
      if (len(electrons)==1 and len(muons)==1):
        if electrons[0].trkcharge * muons[0].trkcharge < 0.0:
          return True
      return False

    #__________________________________________________________________________

    def cut_EleMuonMass130GeV200(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      if len(electrons)==1 and len(muons)==1 :
          tempMass = (electrons[0].tlv + muons[0].tlv).M()
          if tempMass > 130*GeV and tempMass < 200*GeV :
            return True;
      return False

    #__________________________________________________________________________
    def cut_EEETTT(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_tight and ele1_is_tight and ele2_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEETTL(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_loose  = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_tight and ele1_is_tight and ele2_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEETLT(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_tight and ele1_is_loose and ele2_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEELTT(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_loose and ele1_is_tight and ele2_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_EEETLL(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_loose  = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_loose and ele1_is_loose and ele2_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_EEELLT(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_loose and ele1_is_loose and ele2_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_EEELTL(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_loose  = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_loose and ele1_is_tight and ele2_is_loose and pass_mc_filter 
    #__________________________________________________________________________
    def cut_EEELLL(self):

      electrons = self.store['electrons_loose']
      
      if (len(electrons) < 3): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      ele2_is_loose  = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        ele2_is_real    = electrons[2].isTrueIsoElectron()
        pass_mc_filter  = ele0_is_real and ele1_is_real and ele2_is_real    

      return ele0_is_loose and ele1_is_loose and ele2_is_loose and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuTTT(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_tight and muon1_is_tight and muon2_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_MuMuMuTTL(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_loose = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_tight and muon1_is_tight and muon2_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_MuMuMuTLT(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_tight and muon1_is_loose and muon2_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuLTT(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_loose and muon1_is_tight and muon2_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuTLL(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      muon2_is_loose = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_tight and muon1_is_loose and muon2_is_loose and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuLTL(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_loose = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_loose and muon1_is_tight and muon2_is_loose and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuLLT(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_loose and muon1_is_loose and muon2_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuLLL(self):

      muons = self.store['muons']
      
      if (len(muons)< 3): return False

      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      muon2_is_loose = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        muon2_is_real   = muons[2].isTrueIsoMuon()
        pass_mc_filter  = muon0_is_real and muon1_is_real and muon2_is_real

      return muon0_is_loose and muon1_is_loose and muon2_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real    

      return ele0_is_tight and ele1_is_tight and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuTTL(self):    

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real    

      return ele0_is_tight and ele1_is_tight and muon0_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuTLT(self):    

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_tight and ele1_is_loose and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuLTT(self):    

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium)) 
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real


      return ele0_is_loose and ele1_is_tight and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuLLT(self): 

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium)) 
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium)) 
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_loose and ele1_is_loose and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuLTL(self):    

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium)) 
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real


      return ele0_is_loose and ele1_is_tight and muon0_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuTLL(self):    

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium) 
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium)) 
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real


      return ele0_is_tight and ele1_is_loose and muon0_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuLLL(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 1): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium)) 
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_loose and ele1_is_loose and muon0_is_loose and pass_mc_filter

    #__________________________________________________________________________
    def cut_EMuMuTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        muon1_is_real   = muons[1].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and muon0_is_real and muon1_is_real

      return ele0_is_tight and muon0_is_tight and muon1_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuTTL(self):  

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_tight and muon0_is_tight and muon1_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuTLT(self): 

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_tight =  bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real


      return ele0_is_tight and muon0_is_loose and muon1_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuLTT(self):   

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real


      return ele0_is_loose and muon0_is_tight and muon1_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuLLT(self):   

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_loose and muon0_is_loose and muon1_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuLTL(self):    

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_loose and muon0_is_tight and muon1_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuTLL(self):  

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_tight and muon0_is_loose and muon1_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EMuMuLLL(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 2): return False

      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real    = electrons[0].isTrueIsoElectron()
        ele1_is_real    = electrons[1].isTrueIsoElectron()
        muon0_is_real   = muons[0].isTrueIsoMuon()
        pass_mc_filter  = ele0_is_real and ele1_is_real and muon0_is_real

      return ele0_is_loose and muon0_is_loose and muon1_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEMuMuTTTT(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 2): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)      
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)       

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and muon0_is_real and muon1_is_real     

      return ele0_is_tight and ele1_is_tight and muon0_is_tight and muon1_is_tight and pass_mc_filter    

    #__________________________________________________________________________
    def cut_EEMuMuTTTL(self):
      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 2): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)      
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)       

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and muon0_is_real and muon1_is_real

      return ele0_is_tight and ele1_is_tight and muon0_is_tight and muon1_is_loose and pass_mc_filter   

    #__________________________________________________________________________
    def cut_EEMuMuTTLT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 2): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)      
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)  
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)    

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and muon0_is_real and muon1_is_real

      return ele0_is_tight and ele1_is_tight and muon0_is_loose and muon1_is_tight and pass_mc_filter         

    #__________________________________________________________________________
    def cut_EEMuMuTLTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 2): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))     
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.) 
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)    

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and muon0_is_real and muon1_is_real

      return ele0_is_tight and ele1_is_loose and muon0_is_tight and muon1_is_tight and pass_mc_filter  

    #__________________________________________________________________________
    def cut_EEMuMuLTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 2 or len(muons)< 2): return False
      
      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)     
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.) 
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)    

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and muon0_is_real and muon1_is_real

      return ele0_is_loose and ele1_is_tight and muon0_is_tight and muon1_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEEMuTTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 3 or len(muons)< 1): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)  
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)      
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)    

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        ele2_is_real     = electrons[2].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real and muon0_is_real    

      return ele0_is_tight and ele1_is_tight and ele2_is_tight and muon0_is_tight and pass_mc_filter  

    #__________________________________________________________________________
    def cut_EEEMuTTTL(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 3 or len(muons)< 1): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)  
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)      
      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)   

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        ele2_is_real     = electrons[2].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real and muon0_is_real

      return ele0_is_tight and ele1_is_tight and ele2_is_tight and muon0_is_loose and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEEMuTTLT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 3 or len(muons)< 1): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)  
      ele2_is_loose  = bool(not(electrons[2].isIsolated_Loose and electrons[2].LHMedium))     
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.) 

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        ele2_is_real     = electrons[2].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real and muon0_is_real

      return ele0_is_tight and ele1_is_tight and ele2_is_loose and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEEMuTLTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 3 or len(muons)< 1): return False
      
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)
      ele1_is_loose  = bool(not(electrons[1].isIsolated_Loose and electrons[1].LHMedium))  
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.) 

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        ele2_is_real     = electrons[2].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real and muon0_is_real

      return ele0_is_tight and ele1_is_loose and ele2_is_tight and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_EEEMuLTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 3 or len(muons)< 1): return False
      
      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))  
      ele1_is_tight  = bool(electrons[1].isIsolated_Loose and electrons[1].LHMedium)
      ele2_is_tight  = bool(electrons[2].isIsolated_Loose and electrons[2].LHMedium)
      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.) 

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        ele1_is_real     = electrons[1].isTrueIsoElectron()
        ele2_is_real     = electrons[2].isTrueIsoElectron()
        muon0_is_real    = muons[0].isTrueIsoMuon()
        pass_mc_filter   = ele0_is_real and ele1_is_real and ele2_is_real and muon0_is_real

      return ele0_is_loose and ele1_is_tight and ele2_is_tight and muon0_is_tight and pass_mc_filter 

    #__________________________________________________________________________
    def cut_MuMuEMuTTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)        
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)  

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and ele0_is_real    

      return muon0_is_tight and muon1_is_tight and muon2_is_tight and ele0_is_tight and pass_mc_filter  

    #__________________________________________________________________________
    def cut_MuMuEMuTTTL(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)        
      muon2_is_loose = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and ele0_is_real

      return muon0_is_tight and muon1_is_tight and muon2_is_loose and ele0_is_tight and pass_mc_filter  

    #__________________________________________________________________________
    def cut_MuMuEMuTTLT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)        
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      ele0_is_loose  = bool(not(electrons[0].isIsolated_Loose and electrons[0].LHMedium))

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and ele0_is_real

      return muon0_is_tight and muon1_is_tight and muon2_is_tight and ele0_is_loose and pass_mc_filter  

    #__________________________________________________________________________
    def cut_MuMuEMuTLTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 3): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)      
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and ele0_is_real

      return muon0_is_tight and muon1_is_loose and muon2_is_tight and ele0_is_tight and pass_mc_filter  

    #__________________________________________________________________________
    def cut_MuMuEMuLTTT(self):

      electrons = self.store['electrons_loose']
      muons = self.store['muons']
      
      if (len(electrons) < 1 or len(muons)< 3): return False

      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.) 
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      ele0_is_tight  = bool(electrons[0].isIsolated_Loose and electrons[0].LHMedium)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        ele0_is_real     = electrons[0].isTrueIsoElectron()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and ele0_is_real

      return muon0_is_loose and muon1_is_tight and muon2_is_tight and ele0_is_tight and pass_mc_filter 
    #__________________________________________________________________________
    def cut_MuMuMuMuTTTT(self):

      muons = self.store['muons']
      
      if (len(muons)< 4): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)        
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      muon3_is_tight = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        muon3_is_real    = muons[3].isTrueIsoMuon()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and muon3_is_real    

      return muon0_is_tight and muon1_is_tight and muon2_is_tight and muon3_is_tight and pass_mc_filter  
    #__________________________________________________________________________
    def cut_MuMuMuMuTTTL(self):

      muons = self.store['muons']
      
      if (len(muons)< 4): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)        
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      muon3_is_loose = bool(not muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<10.)

      pass_mc_filter   = True
      
      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        muon3_is_real    = muons[3].isTrueIsoMuon()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and muon3_is_real    

      return muon0_is_tight and muon1_is_tight and muon2_is_tight and muon3_is_loose and pass_mc_filter  
    #__________________________________________________________________________                                                                                                    
    def cut_MuMuMuMuTTLT(self):

      muons = self.store['muons']

      if (len(muons)< 4): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_loose = bool(not muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<10.)
      muon3_is_tight = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)

      pass_mc_filter   = True

      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        muon3_is_real    = muons[3].isTrueIsoMuon()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and muon3_is_real

      return muon0_is_tight and muon1_is_tight and muon2_is_loose and muon3_is_tight and pass_mc_filter
    #__________________________________________________________________________                                                                                                    
    def cut_MuMuMuMuTLTT(self):

      muons = self.store['muons']

      if (len(muons)< 4): return False

      muon0_is_tight = bool(muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<3.)
      muon1_is_loose = bool(not muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<10.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      muon3_is_tight = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)

      pass_mc_filter   = True

      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        muon3_is_real    = muons[3].isTrueIsoMuon()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and muon3_is_real

      return muon0_is_tight and muon1_is_loose and muon2_is_tight and muon3_is_tight and pass_mc_filter
    #__________________________________________________________________________                                                                                                  
    def cut_MuMuMuMuLTTT(self):

      muons = self.store['muons']

      if (len(muons)< 4): return False

      muon0_is_loose = bool(not muons[0].isIsolated_FixedCutTightTrackOnly and muons[0].trkd0sig<10.)
      muon1_is_tight = bool(muons[1].isIsolated_FixedCutTightTrackOnly and muons[1].trkd0sig<3.)
      muon2_is_tight = bool(muons[2].isIsolated_FixedCutTightTrackOnly and muons[2].trkd0sig<3.)
      muon3_is_tight = bool(muons[3].isIsolated_FixedCutTightTrackOnly and muons[3].trkd0sig<3.)

      pass_mc_filter   = True

      if self.sampletype=="mc":
        muon0_is_real    = muons[0].isTrueIsoMuon()
        muon1_is_real    = muons[1].isTrueIsoMuon()
        muon2_is_real    = muons[2].isTrueIsoMuon()
        muon3_is_real    = muons[3].isTrueIsoMuon()
        pass_mc_filter   = muon0_is_real and muon1_is_real and muon2_is_real and muon3_is_real

      return muon0_is_loose and muon1_is_tight and muon2_is_tight and muon3_is_tight and pass_mc_filter

    #____________________________________________________________________________
    def cut_ZVeto(self):

        mZ = 91.1876*GeV
        electrons = self.store['electrons_loose']
        muons     = self.store['muons']
        passZVetoEle  = True
        passZVetoMuon = True

        if(len(electrons)>=2):
            for i in electrons:
                for j in electrons:
                    if(i==j): continue
                    else: 
                        charge = i.trkcharge * j.trkcharge
                        mass   = (i.tlv + j.tlv).M()
                        if(charge<0. and abs(mass - mZ) < 10*GeV): 
                            passZVetoEle = False
                            break
        if(len(muons)>=2):                
            for i in muons:
                for j in muons:
                    if(i==j): continue
                    else: 
                        charge = i.trkcharge * j.trkcharge
                        mass   = (i.tlv + j.tlv).M()
                        if(charge<0. and abs(mass - mZ) < 10*GeV): 
                            passZVetoMuon = False
                            break 
        if(passZVetoEle and passZVetoMuon): return True
        return False
    #____________________________________________________________________________
    def cut_IsValidationRegion2(self):
        electrons = self.store['electrons_loose']
        muons     = self.store['muons']
        leptons   = electrons + muons 
        
        if(len(leptons)>=2):
            for i in leptons:
                for j in leptons:
                    if(i==j): continue
                    else:
                        charge = i.trkcharge * j.trkcharge
                        mass   = (i.tlv + j.tlv).M()
                        if( charge>0. and mass > 200*GeV): return False
        return True                
    #____________________________________________________________________________
    def cut_IsSignalRegion2(self):
        electrons = self.store['electrons_loose']
        muons     = self.store['muons']
        leptons   = electrons + muons 
        if(len(leptons)>=2):
            for i in leptons:
                for j in leptons:
                    if(i==j): continue
                    else:
                        charge = i.trkcharge * j.trkcharge
                        mass   = (i.tlv + j.tlv).M()
                        if( charge>0. and mass < 200*GeV): return False
        return True                
    #____________________________________________________________________________
    def cut_DeltaMassOverMass(self):
        alpha = array('d',[0.08, 0.004, 0.005, 0.004, 0.003, 0.004])
        beta  = array('d',[0.78, 1.50,  1.41,  1.45,  1.41,  1.46 ])
        electrons = self.store['electrons_loose']
        muons     = self.store['muons']
        leptons   = electrons + muons 
        
        flavour =self.store['ChannelFlavour']

        if(len(leptons)>=2):
            for i in leptons:
                for j in leptons:
                    if(i==j): continue
                    else:
                        charge   = i.trkcharge * j.trkcharge
                        massDiff = (i.tlv.M()/GeV - j.tlv.M()/GeV)
                        mass     = (i.tlv.M()/GeV + j.tlv.M()/GeV)/2
                        massCut  = (abs(massDiff)/(alpha[flavour]*(pow(mass,beta[flavour]))))
                        if( charge>0. and (abs(massDiff)>3)): return False
        return True                   
    #____________________________________________________________________________

    def cut_PASS(self):
      return True


#------------------------------------------------------------------------------
class PlotAlg(pyframe.algs.CutFlowAlg,CutAlg):
  
    #__________________________________________________________________________
    def __init__(self,
                 name          = 'PlotAlg',
                 region        = '',
                 hist_list     = [], # list of histograms to be filled
                 cut_flow      = None,
                 plot_all      = True,
                 do_var_check  = False,
                 ):
        pyframe.algs.CutFlowAlg.__init__(self,key=region)
        CutAlg.__init__(self,name,isfilter=False)
        self.cut_flow     = cut_flow
        self.region       = region
        self.plot_all     = plot_all
        self.hist_list    = hist_list
        self.do_var_check = do_var_check
    
    #_________________________________________________________________________
    def initialize(self):
        
        # remove eventual repetitions from list of histograms
        h_dict = {}
        for h in self.hist_list: h_dict[h.hname] = h
        self.hist_list = h_dict.values()

        pyframe.algs.CutFlowAlg.initialize(self)
    #_________________________________________________________________________
    def execute(self, weight):
   
        # next line fills in the cutflow hists
        # the first bin of the cutflow does not
        # take into account object weights
        pyframe.algs.CutFlowAlg.execute(self, weight)

        list_cuts = []
        for cut, list_weights in self.cut_flow:
            ## apply weights for this cut
            if list_weights:
              for w in list_weights: weight *= self.store[w]

            list_cuts.append(cut)
            passed = self.check_region(list_cuts)
            self.hists[self.region].count_if(passed, cut, weight)

            ## if plot_all is True, plot after each cut, 
            ## else only plot after full selection
            
            if (self.plot_all or len(list_cuts)==len(self.cut_flow)):
               region_name = os.path.join(self.region,'_'.join(list_cuts))
               region_name = region_name.replace('!', 'N')
               region = os.path.join('/regions/', region_name)
               
               self.plot(region, passed, list_cuts, cut, weight=weight)

        return True

    #__________________________________________________________________________
    def finalize(self):
        pyframe.algs.CutFlowAlg.finalize(self)

    #__________________________________________________________________________
    def plot(self, region, passed, list_cuts, cut, list_weights=None, weight=1.0):

        # -----------------
        # Create histograms
        # -----------------
        for h in self.hist_list:
            if h.get_name() == "Hist1D":
              h.instance = self.hist(h.hname, "ROOT.TH1F('$', ';%s;%s', %d, %lf, %lf)" % (h.xtitle,h.ytitle,h.nbins,h.xmin,h.xmax), dir=os.path.join(region, '%s'%h.dir))
            elif h.get_name() == "Hist2D": 
              h.instance = self.hist(h.hname, "ROOT.TH2F('$', ';%s;%s', %d, %lf, %lf, %d, %lf, %lf)" % (h.hname,h.hname,h.nbinsx,h.xmin,h.xmax,h.nbinsy,h.ymin,h.ymax), dir=os.path.join(region, '%s'%h.dir))
              h.set_axis_titles()

        # ---------------
        # Fill histograms
        # ---------------
        if passed:
          for h in self.hist_list:
            if self.do_var_check:
              exec ( "present = %s"%h.varcheck() )
              if not present: 
                sys.exit( "ERROR: variable %s  not found for hist %s"%(h.vexpr,h.hname) )
            
            if h.get_name() == "Hist1D":
              var = -999.
              
              # this all part gives me the shivers. But is just temporary. Don't panic
              if hasattr(self.chain,"njets") and "njets" in h.vexpr: exec( "var = self.chain.njets" ) 
              elif: hasattr(self.chain,"njet") and "njet" in h.vexpr: exec( "var = self.chain.njet" ) 
              else: exec( "var = %s" % h.vexpr ) # so dirty !!!
              
              if h.instance and var!=-999.: h.fill(var, weight)
            
            elif h.get_name() == "Hist2D":
              varx = -999.
              vary = -999.
              exec( "varx,vary = %s" % h.vexpr ) # so dirty !!!
              if h.instance and varx!=-999. and vary!=-999.: h.fill(varx,vary, weight)
          
    #__________________________________________________________________________
    def check_region(self,cutnames):
        cut_passed = True
        for cn in cutnames:
            if cn == 'ALL': continue

            if cn.startswith('!'):
                cut_passed = not self.apply_cut(cn[1:])
            else:
                cut_passed = self.apply_cut(cn) and cut_passed
        return cut_passed
    
    
#__________________________________________________________________________
def log_bins(nbins,xmin,xmax):
    xmin_log = math.log(xmin)
    xmax_log = math.log(xmax)
    log_bins = [ float(i)/float(nbins)*(xmax_log-xmin_log) + xmin_log for i in xrange(nbins+1)]
    bins = [ math.exp(x) for x in log_bins ]
    return bins

#__________________________________________________________________________
def log_bins_str(nbins,xmin,xmax):
    bins = log_bins(nbins,xmin,xmax)
    bins_str = "%d, array.array('f',%s)" % (len(bins)-1, str(bins))
    return bins_str 


