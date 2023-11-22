#!/usr/bin/env python
##############################################################################################################################################
#
#   This script creates 1 practice spreadsheet, and 20 trial spreadsheets.
#
#   Written by Catherine Kennon from CurveSpace
#
##############################################################################################################################################


#Import section
import pandas as pd
import os
import numpy as np
import io
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
from psychopy import data, gui, misc, core
import pylab, scipy
import math
import random

#This funcutation takes a csv filename and creates 20 blocks and one practice spreadsheet. 
#The practice spreadsheet will contain 28 images. Each block spreadsheet will contain 28 images.
#Left and right will be counterbalanced, 50% each as will real or fake.
#For trial type, 75% will be matched while 25% will be mismatched.
def createBlocks(thisFileName, pid):

    #local variables
    numbPracTrials = 28
    numbRealTrials = 28
    blockNameList = []
    
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    #read in the csv file
    df = pd.read_csv(thisFileName)

    #spilt the data frame into real and fake
    realDf = df.loc[df['realOrFake'] == 'real']
    fakeDf = df.loc[df['realOrFake'] == 'fake']

    #randomise the rows in both these dataframes
    realDf = realDf.sample(frac=1)
    fakeDf = fakeDf.sample(frac=1)

    #take the first set of rows for the practice trials
    #50% from real and 50% from fake
    prac1 = realDf[:int(numbPracTrials/2)].copy()
    prac2 = fakeDf[:int(numbPracTrials/2)].copy()

    #Concatenate them
    prac = pd.concat([prac1, prac2])

    #randomise the rows
    prac = prac.sample(frac=1)

    #add trialType
    prac["trialType"] = createLists('match', 'mismatch', math.ceil(numbPracTrials * 0.75), math.floor(numbPracTrials * 0.25))
    
    prac["BlockName"] = createLists('Prac', 'Prac', numbPracTrials, 0)

    #save as an csv file
    prac.to_csv (_thisDir + '\\conditions\\' + pid + '_Prac.csv', index = False, header=True)
    
    #set the indices
    startIndex = int(numbPracTrials/2)

    #create blocks of numbRealTrials trials
    for i in range(20): 

        #take the next rows for the real trials 50% from real and 50% from fake
        block1 = realDf[startIndex:int(startIndex + (numbRealTrials/2))].copy()
        block2 = fakeDf[startIndex:int(startIndex + (numbRealTrials/2))].copy()

        #Concatenate the dataframes
        block = pd.concat([block1, block2])

        #randomise the rows
        block = block.sample(frac=1)

        #add trialType
        block["trialType"] = createLists('match', 'mismatch', math.ceil(numbRealTrials * 0.75), math.floor(numbRealTrials * 0.25))

        #generate a filename
        currentFname = _thisDir + '\\conditions\\' + pid + '_Block' + str(i+1) + '.csv'

        #save as an excel file
        block.to_csv (currentFname, index = False, header=True)

        #add the filename to the list
        blockNameList.append(pid + '_Block' + str(i+1) + '.csv')

        #increment the starting index
        startIndex = int(startIndex + (numbRealTrials/2))
       

    #randomise the list
    random.shuffle(blockNameList)

    #create a new dataframe to hold the master condition list
    master = pd.DataFrame()

    #add the column BlockName
    master["BlockName"] = blockNameList

    #save as a csv file
    master.to_csv ( _thisDir + '\\conditions\\' + pid + '_master_conditions.csv', index = False, header=True)

#This funcutation take two strings, and a total number times each string needs to be repeated.
#A combined and randomised list is returned.
def createLists(firstString, secondString, firstTotal, secondTotal):
    
    #first list
    firstList = [firstString] * int(firstTotal)
    
    #second list
    secondList = [secondString] * int(secondTotal)
   
    #concatenate the lists
    combinedList = firstList + secondList
    
    #randomise the list
    random.shuffle(combinedList)
    
    #return the list
    return combinedList