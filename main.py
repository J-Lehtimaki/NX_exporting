# Janne Lehtimäki
# janne.lehtimaki@etteplan.com
# Etteplan Finland Oy

# NX 12.0.0.27
# Description:
#  - Exports solid to .step from active NX session
#  - Use by running via NXJournal
# Parameters:
#    sys.argv[1] = Path to .prt -files folder
# Pre-conditions:
#  - Configure parameters at  ./myStepData.json
import json
import os
import sys
import time
import subprocess

import NXOpen
from pathlib import Path
from filehandler import StepFileHandler
#from nTopCLpipe import NTopProcessManager

# Creates a dict for file locations
def createSmoothenWorkflowData(inputDir):
    NXExportPath = inputDir
    # NXimportNTopPath = inputDir[:len(inputDir) - 4] + '.prt'
    NXimportNTopPath = inputDir[:len(inputDir) - 4] + 'nTopSmoothed.X_T'
    workflowData = {
        "inputFileLocation": inputDir,
        "outputFileDestination": NXimportNTopPath
    }
    return workflowData

def main(argPath):
    # Check what version of Python NX uses
    nxPyVersion = open(r"C:/Users/Public/Documents/ntopTest/NX_py_version.txt","w")
    nxPyVersion.write(sys.version)  # 3.6.1 on my NX12
    nxPyVersion.close() #to change file access modes
    os.system('python C:\Mallit\DI\sälä\pythonversion.py')  # 3.9.2 on my comp

    # load export data from ./myStepData.json
    stepHandler = StepFileHandler(argPath)
    # Initiate session
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    # WORK FLOW - export - nTop notebook - import
    # STEP 1: Export solid from NX
    stepCreator = theSession.DexManager.CreateStepCreator()
    stepCreator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    NXexportedPath = stepHandler.exportSolidNX(stepCreator, workPart)
    stepCreator.Destroy()
    # Wait until file is created by NX
    while(os.path.exists(NXexportedPath) == False):
        time.sleep(4)
    
    # STEP 2: Launch nTop notebook with latest version of Python
    smoothenWorkflow = createSmoothenWorkflowData(NXexportedPath)
    cmd = 'python {nTopCLhandler} {input} {output}'.format(
        nTopCLhandler = 'C:/Mallit/DI/nTop/dev/1-nTpCL/python/nTopCLpipe.py',
        input = smoothenWorkflow['inputFileLocation'],
        output = smoothenWorkflow['outputFileDestination'])
    os.system(cmd)
    # Wait until file is created by nTopology
    timer = 600      # Adjust way up, for large meshes. Ideally find a better way
    while(os.path.exists(smoothenWorkflow["outputFileDestination"]) == False):
        time.sleep(1)
        timer -= 1
        if(timer < 0):
            break

    # STEP 3: import stepfile nTop result - ntop only exports 242, NX can't import with my license
    #step214Importer = theSession.DexManager.CreateStep214Importer() # init
    #stepHandler.importStepNX(step214Importer, smoothenWorkflow["outputFileDestination"])
    #step214Importer.Destroy()

    # STEP 3: Import parasolid that nTopology created
    ParaSolidImporter = workPart.ImportManager.CreateParasolidImporter()
    ParaSolidImporter.FileName = smoothenWorkflow['outputFileDestination']
    nXObject1 = ParaSolidImporter.Commit()
    ParaSolidImporter.Destroy()

if __name__ == '__main__':
    main(sys.argv[1])
