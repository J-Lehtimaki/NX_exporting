# Janne Lehtimäki
# janne.lehtimaki@etteplan.com
# Etteplan Finland Oy

# NX 12.0.0.27

import json
import os
import sys

import NXOpen
from pathlib import Path

# Description:
# - Loads export settings from myStepData.json
# Pre-conditions:
# - json file is in work dir
# Exceptions:
# - TODO : crashes if file not in workdir
def loadJson(argPath):
    workdir = Path(argPath)
    jsonPath = os.path.join(workdir, 'myStepData.json')
    f = open(jsonPath)
    jsonData = json.load(f)
    return jsonData

def setupStepImportFromJSON(step214Importer, importData, argPath):
    step214Importer.SimplifyGeometry = True     #
    step214Importer.LayerDefault = 1            #
    step214Importer.SettingsFile = "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\step214ug.def"      #
    step214Importer.ObjectTypes.Curves = False      #
    step214Importer.ObjectTypes.Surfaces = False        #
    step214Importer.ObjectTypes.PmiData = False     #
    step214Importer.FileOpenFlag = False    #

    raise ValueError(os.path.join(argPath, importData["exportData"]["filename"]["outputStep"] + '.stp'))

    # Use ./myStepData.json NX exported file
    step214Importer.InputFile = os.path.join(argPath, importData["exportData"]["filename"]["outputStep"] + '.stp')
    step214Importer.OutputFile = os.path.join(argPath, importData["exportData"]["filename"]["outputStep"] + '.prt')


def main(argPath):
    # load import data from ./myStepData.json
    importData = loadJson(argPath)

    # Initiate session and AP214 importer
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    step214Importer = theSession.DexManager.CreateStep214Importer()

    # Handle Json
    setupStepImportFromJSON(step214Importer, importData, argPath)

    # End
    nXObject1 = step214Importer.Commit()
    step214Importer.Destroy()

if __name__ == '__main__':
    main(sys.argv[1])