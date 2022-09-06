import time, queue, sys, datetime, json, math, scipy, pywt, time
import pandas as pd
import numpy as np
from statistics import mode
from scipy import stats
from sklearn import preprocessing
from collections import defaultdict, Counter
from scipy.special import expit

#================================================================================================
#  Feature Extraction from Physiological Signals
#================================================================================================
def calculate_entropy(list_values):
    counter_values = Counter(list_values).most_common()
    probabilities = [elem[1]/len(list_values) for elem in counter_values]
    entropy=scipy.stats.entropy(probabilities)
    return entropy

def calculate_statistics(list_values):
    n5 = np.nanpercentile(list_values, 5)
    n25 = np.nanpercentile(list_values, 25)
    n75 = np.nanpercentile(list_values, 75)
    n95 = np.nanpercentile(list_values, 95)
    median = np.nanpercentile(list_values, 50)
    mean = np.nanmean(list_values)
    std = np.nanstd(list_values)
    var = np.nanvar(list_values)
    rms = np.nanmean(np.sqrt(list_values**2))
    return [n5, n25, n75, n95, median, mean, std, var, rms]

def calculate_crossings(list_values):
    zero_crossing_indices = np.nonzero(np.diff(np.array(list_values)> 0))[0]
    no_zero_crossings = len(zero_crossing_indices)
    mean_crossing_indices = np.nonzero(np.diff(np.array(list_values) > np.nanmean(list_values)))[0]
    no_mean_crossings = len(mean_crossing_indices)
    return [no_zero_crossings, no_mean_crossings]

def get_features(list_values):
    list_values = list_values[0,:]
    entropy = calculate_entropy(list_values)
    crossings = calculate_crossings(list_values)
    statistics = calculate_statistics(list_values)
    return [entropy] + crossings + statistics
#================================================================================================


#================================================================================================
# EDA Feature Extraction (Wavelet Features)
#================================================================================================
def extract_eda_features(raw_eda):
    features =[]
    EDA = raw_eda
    list_coeff = pywt.wavedec(EDA, 'db4', level=3)

    for coeff in list_coeff:
        features += get_features(coeff)
    return features
#================================================================================================

#================================================================================================
# RESP BELT Feature Extraction (Wavelet Features)
#================================================================================================

def extract_resp_belt_features(raw_data):
    features =[]
    resp_belt = raw_data
    list_coeff = pywt.wavedec(resp_belt, 'db4', level=3)

    for coeff in list_coeff:
        features += get_features(coeff)
    return features
#================================================================================================

#================================================================================================
# EEG Feature Extraction (Wavelet Features)
#================================================================================================

def eeg_features(raw_data):
    ch = 0
    features= []
    def calculate_entropy(list_values):
        counter_values = Counter(list_values).most_common()
        probabilities = [elem[1]/len(list_values) for elem in counter_values]
        entropy=scipy.stats.entropy(probabilities)
        return entropy

    def calculate_statistics(list_values):
        median = np.nanpercentile(list_values, 50)
        mean = np.nanmean(list_values)
        std = np.nanstd(list_values)
        var = np.nanvar(list_values)
        rms = np.nanmean(np.sqrt(list_values**2))
        return [median, mean, std, var, rms]

    def get_features(list_values):
    #     list_values = list_values[0,:]
        entropy = calculate_entropy(list_values)
        statistics = calculate_statistics(list_values)
        return [entropy] + statistics

    for i in range(raw_data.shape[0]):
        ch_data = raw_data[i]
        list_coeff = pywt.wavedec(ch_data, 'db4', level=5)
        for coeff in list_coeff:
            features += get_features(coeff)

        ch = ch+1
    return features

#=================================================================================================
