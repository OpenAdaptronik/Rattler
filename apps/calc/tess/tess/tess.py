'''
Created on 10.11.2017

@author: stoll
'''

import csv
from numpy import argwhere, transpose
import numpy
from apps.calc.tess.tess import helpers
from apps.calc.tess.tess import waterfalls


def tess(time,data,data2):
    '''
    TESS is a software project that is part of the OpenAdaptronics program, conducted at the Fraunhofer LBF.
    Its preliminary title is an acronym for “Tool zur Empfehlung von Strategien zur Schwingungsberuhigung”

    :param time: time data
    :param data: acceleration of the instrument
    :param data2: exciting acceleration
    :return:
    '''

    analysisweightsFILENAME = 'apps/tess/tess_input/analysis_weights.csv'
    DesiredAmpLevel = 8
    MinFrequency = 3;               # general minimum frequency taken into account in Hz
    TFMode = 0
    #analysis sensitivity parameters
    sens_FindPeaks = 50;            # sensitivity of finding peaks in measurement data in %
                                    # | 0% -> peaks are virtually not found 
                                    # | 100% -> peaks are found very often
    
    sens_SumUpPeaks = 50;           # sensitivity of summing up peaks to real peaks in %
                                    # | 0% -> peaks are virtually never summed up to a real peak 
                                    # | 100% -> peaks are very likely to be summed up to a real peak 
    
    sens_TFOrigin = 50;             # sensitivity of finding that a real peak's origin is the TF (and not the excitation) in %
                                    # | 0% -> finding that the origin of a real peak is the excitation is very likely 
                                    # | 100% -> finding that the origin of a real peak is the TF is very likely
    
    sens_TimevariantBehavior = 50;  # sensitivity of considering the vibration behavior to be timevariant
                                    # | 0% -> behavior is virtually never considered timevariant 
                                    # | 100% -> behavior is very easily considered timevariant
                                    
    sens_UnproblematicLFD = 50;     # sensitivity of considering the amplitude level in the low frequency domain (LFD) of A_1 to be unproblematic
                                    # | 0% -> the amp level in the LFD is virtually never considered unproblematic
                                    # | 100% -> the amp level in the LFD is very easily considered unproblematic
                                    
    sens_UnproblematicNFD = 50;     # sensitivity of considering the amplitude level in the (peak-) neighboring frequency domain (NFD) of A_1 to be unproblematic
                                    # | 0% -> the amp level in the NFD is virtually never considered unproblematic
                                    # | 100% -> the amp level in the NFD is very easily considered unproblematic
                                    
    sens_UnproblematicHFD = 50;     # sensitivity of considering the amplitude level in the high frequency domain (HFD) of A_0 to be unproblematic
                                    # | 0% -> the amp level in the HFD is virtually never considered unproblematic
                                    # | 100% -> the amp level in the HFD is very easily considered unproblematic
    SV = numpy.zeros(17)

    
    # solution identifiers
    SID = []
    SID.append('System Verstimmen, passiv')
    SID.append('System Verstimmen, schaltbar')
    SID.append('System Verstimmen, semi-aktiv')
    SID.append('Daempfung erhoehen, passiv')
    SID.append('Daempfung erhoehen, schaltbar')
    SID.append('Daempfung erhoehen, semi-aktiv')
    SID.append('Aktorik in Struktur einbringen')
    SID.append('Tilger, passiv')
    SID.append('Tilger, schaltbar')
    SID.append('Neutralisator, passiv')
    SID.append('Neutralisatior, schaltbar')
    SID.append('Adaptiver Tilger/Neutralisator')
    SID.append('Elastische Lagerung, passiv')
    SID.append('Elastische Lagerung, schaltbar')
    SID.append('Elastische Lagerung, semi-aktiv')
    SID.append('Elastische Lagerung, aktiv')
    SID.append('Inertialmassenaktor IMA')
    
    
    # CSV-Datei mit den Bewertungsgewichten/Parametern einlesen
    analysisweights = []
    with open(analysisweightsFILENAME) as csvfile:
        rd = csv.reader(csvfile)
        for row in rd:
            analysisweights.append(row)
    del analysisweights [0]
    analysisweights = transpose([[float(j) for j in i] for i in analysisweights])
    

    #@TODO: Daten einlesen überprüfen
    t = time
    a_0 = data
    a_1 = data2
    A_0, f, tout = waterfalls.waterfall(t, a_0, 256, overlap=.5)
    A_1, f, tout = waterfalls.waterfall(t, a_1, 256, overlap=.5)
    tfmat = numpy.divide(A_1,A_0)
    tf = numpy.average(tfmat, 0, A_0)
    
    iValidF = numpy.where(f >= MinFrequency)
    
    ifmin = argwhere(f>=MinFrequency)[0];
    
    fft_rec_max_mod = A_1[:, iValidF].flatten()
    
    
    
    # max occuring amplitude (median of top 10 maximum amplitudes)
    lst = numpy.sort(fft_rec_max_mod)
    maxamp = numpy.median(lst[-10:-1])
    
    # problematic level used as reference
    problvl = (DesiredAmpLevel/100)*maxamp
    
    
    # finding real peaks in measurement data and determine origin
    peakloc_ind, collectivepeaks, numrealpeaks, meannumrealpeaks, realpeakloc, isrealpeakfromTF = helpers.findRealPeaks(A_1, tf, f, iValidF, sens_FindPeaks, sens_TFOrigin, sens_SumUpPeaks, maxamp, problvl)
    

    if meannumrealpeaks > 1.1:
        multiplepeaks = True
        SV = SV+analysisweights[0]
    else:
        multiplepeaks = False
        SV = SV+analysisweights[1]
        pass
    meanpeaksfromtf = numpy.zeros(len(tout))
    
    
    for i in range(len(tout)):
        meanpeaksfromtf[i] = numpy.nanmean(isrealpeakfromTF[i])
        pass
    
    if numpy.nanmean(meanpeaksfromtf) >= 0.95:
        allpeaksfromtf = True
        SV = SV + analysisweights[2]
    else:
        allpeaksfromtf = False
        SV = SV + analysisweights[3]
    
    isrealpeaktimevariant = helpers.analyseTimeVariance(A_1, f, collectivepeaks, sens_TimevariantBehavior, peakloc_ind, problvl)
    
    meanpeakstimevariant=[]           
    for i in range(len(isrealpeaktimevariant)):
        meanpeakstimevariant.append(numpy.nanmean(isrealpeaktimevariant[i]))
        
    if numpy.nanmean(meanpeakstimevariant) >= 0.05:
        timevariantbehavior = True
        SV = SV + analysisweights[4]
    else:
        timevariantbehavior = False
        SV = SV + analysisweights[5]
        
    islfdunproblematic, ishfdunproblematic, isnfdunproblematic = helpers.analyseFDAmplitude(A_1, f, iValidF, realpeakloc, numrealpeaks, multiplepeaks, sens_UnproblematicLFD, sens_UnproblematicHFD, sens_UnproblematicNFD, problvl)
    
    # Analysis of Amplitude Level
    
    if numpy.mean(islfdunproblematic) >= .95:
        lfdunproblematic = True
        SV = SV + analysisweights[6]
    else:
        lfdunproblematic = False
        SV = SV + analysisweights[7]
        
    if ~multiplepeaks:
        if numpy.mean(isnfdunproblematic)>=.95:
            nfdunproblematic = True
            SV = SV + analysisweights[8]
        else:
            nfdunproblematic = False
            SV = SV + analysisweights[9]
    
    if numpy.mean(ishfdunproblematic) >= .95:
        hfdunproblematic = True
        SV = SV + analysisweights[10]
    else:
        hfdunproblematic = False
        SV = SV + analysisweights[11]
    
    srt = numpy.argsort(SV)
    lst = numpy.sort(SV)
    
    return   ''.join(['            beste Strategie: ', SID[srt[-1]], ', ', str(SV[srt[-1]]) ]) +'\b' \
            +''.join(['       zweitbeste Strategie: ', SID[srt[-2]], ', ', str(SV[srt[-2]]) ]) +'\b' \
            +''.join(['       drittbeste Strategie: ', SID[srt[-3]], ', ', str(SV[srt[-3]]) ]) +'\b' \
            +''.join(['       viertbeste Strategie: ', SID[srt[-4]], ', ', str(SV[srt[-4]]) ]) +'\b' \
            +''.join(['      fuenftbeste Strategie: ', SID[srt[-5]], ', ', str(SV[srt[-5]]) ])
