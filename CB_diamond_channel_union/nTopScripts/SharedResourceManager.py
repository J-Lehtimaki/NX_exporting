# Author: Janne Lehtimäki
# e-mail: janne.lehtimaki@etteplan.com
# Company: Etteplan Finland Oy
# License: MIT (This code-snippet is part of public thesis-work)

import time
import os
import pathlib
import glob

from multiprocessing import Process, Lock

# Class for resource sharing. Input names from folder.
class SharedResourceManager:
    def __init__(self, inputFileList):
        self.inputFiles_ = inputFileList
        self.unprocessedInputFIles_ = inputFileList
        self.processedInputFiles_ = []

    def getSharedResourceValue(self): return self.value_
    def getInputFiles(self): return self.inputFiles_
    def getUnprocessedInputFiles(self): return self.unprocessedInputFIles_
    def getProcessedInputFiles(self): return self.processedInputFiles_

    # Returns [][] list of lists, amount being n
    def splitInputToEqualLists(self, n):
        copyInputs = self.inputFiles_
        result = []     # append sliced copyinputs here
        subsetSize = len(copyInputs)//n
        # Process files that are in the range of subsetSize
        for i in range(0,n):
            result.append(copyInputs[0:subsetSize])
            del copyInputs[0:subsetSize]
        # Process remainder files
        tracker = 0     # Tracker for dividing equally to different processes
        for f in copyInputs:
            result[tracker].append(f)
            tracker += 1
        return result

    # Returns path to inputfile and removes it from unprocessed list
    def getInput(self):
        if(len(self.unprocessedInputFIles_) == 0):
            return None
        else:
            i = len(self.unprocessedInputFIles_) - 1
            toProcessing = self.unprocessedInputFIles_.pop(i)
            return toProcessing

