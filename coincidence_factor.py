#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 15:19:19 2020

@author: louis
"""
import numpy as np

def coincidence_factor(ref, model, w):
    
    E=0
    M=0
    
    # Compute M :
    model_matches = []
    for i in range(len(ref)):
        ref_spike_time = ref[i]
        window = [ref_spike_time - w, ref_spike_time + w]
        potential_matches = [time for time in model if window[0] < time < window[1]]
        diff = 2
        
        if len(potential_matches) >= 2: 
            for j in range(len(potential_matches)):
                model_spike_time = potential_matches[j]
                if (new_diff := abs(model_spike_time - ref_spike_time)) < diff:
                    match = model_spike_time
                    diff = new_diff
            model_matches.append(match)
            
        elif len(potential_matches) == 1 :
            model_matches.append(potential_matches[0])
            
        elif len(potential_matches) == 0:
            M +=1
            
    # Count whether a spike time in the model has been counted twice or more
    # when computing matches. 
    for i in range(len(np.unique(model_matches))):
        spike_time = np.unique(model_matches)[i]
        if (count := model_matches.count(spike_time)) > 1:
            M += count - 1
            
    # Compute E : 
    ref_matches = []
    for i in range(len(model)):
        model_spike_time = model[i]
        window = [model_spike_time - w, model_spike_time + w]
        potential_matches = [time for time in ref if window[0] < time < window[1]]
        diff = 2
        
        if len(potential_matches) >= 2:
            for j in range(len(potential_matches)):
                ref_spike_time = potential_matches[j]
                if (new_diff := abs(model_spike_time - ref_spike_time)) < diff:
                    match = ref_spike_time
                    diff = new_diff   
            ref_matches.append(match)
            
        elif len(potential_matches) == 1:
            ref_matches.append(potential_matches[0])
        elif len(potential_matches) == 0:
            E += 1
    
    for i in range(len(np.unique(ref_matches))):
        spike_time = np.unique(ref_matches)[i]
        if (count:=ref_matches.count(spike_time)) > 1:
            E += count - 1 
            
   
    M = M / len(ref) 
    E = E / len(model) 
    gamma = 1 - ((E + M) / 2)
    
    return E, M, gamma

