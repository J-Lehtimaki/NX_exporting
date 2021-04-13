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

def setupStepConversionFromJSON(workPart, stepCreator, argPath, exportData):
    # From ./myStepData.json
    stepCreator.SettingsFile = exportData["exportData"]["exportSettings"]["settingsFile"]    # Replace path in myStepData.json if your NX is not installed to default directory
    stepCreator.ColorAndLayers = exportData["exportData"]["exportSettings"]["colorAndLayers"]
    stepCreator.BsplineTol = exportData["exportData"]["exportSettings"]["bSplineTol"]
    stepCreator.Author = exportData["exportData"]["author"]["person"]
    stepCreator.Company = exportData["exportData"]["author"]["company"]
    stepCreator.FileSaveFlag = exportData["exportData"]["exportSettings"]["fileSaveFlag"]
    stepCreator.LayerMask = exportData["exportData"]["exportSettings"]["layerMask"]
    bodyToExport = workPart.Bodies.FindObject(exportData["exportData"]["session"]["body"])     # Single body to export

    # From combined workdir + ./myStepData.json
    stepCreator.InputFile = os.path.join(argPath, exportData["exportData"]["filename"]["inputPrt"] + '.prt')
    stepCreator.OutputFile = os.path.join(argPath, exportData["exportData"]["filename"]["outputStep"] + '.stp')
 
    # Based on json data
    added = stepCreator.ExportSelectionBlock.SelectionComp.Add(bodyToExport)
    stepCreator.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.SelectedObjects

def main(argPath):
    # load export data from ./myStepData.json
    exportData = loadJson(argPath)

    # Initiate session
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    # Initiate export to AP214
    stepCreator = theSession.DexManager.CreateStepCreator()
    stepCreator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    
    # Handle Json
    setupStepConversionFromJSON(workPart, stepCreator, argPath, exportData)

    # End
    nXObject1 = stepCreator.Commit()    
    stepCreator.Destroy()
    
if __name__ == '__main__':
    main(sys.argv[1])
