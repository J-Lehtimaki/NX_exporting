# Janne Lehtimäki
# janne.lehtimaki@etteplan.com
# Etteplan Finland Oy
# NX 12.0.0.27

# Description:
#  - Exports solid to .step from active NX session
# Pre-conditions:
#  - Configure parameters at  ./myStepData.json

import math
import NXOpen
import json
import os
import sys

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

def main(argPath):
    # load export data from ./myStepData.json
    exportData = loadJson(argPath)

    # Initiate session
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    # Export to AP214
    stepCreator = theSession.DexManager.CreateStepCreator()
    stepCreator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    
    # From ./myStepData.json
    stepCreator.SettingsFile = exportData["exportData"]["exportSettings"]["settingsFile"]    # Replace path in myStepData.json if your NX is not installed to default directory
    stepCreator.ColorAndLayers = exportData["exportData"]["exportSettings"]["colorAndLayers"]    # mod
    stepCreator.BsplineTol = exportData["exportData"]["exportSettings"]["bSplineTol"]    # mod
    stepCreator.Author = exportData["exportData"]["author"]["person"]        # mod
    stepCreator.Company = exportData["exportData"]["author"]["company"]      # mod
    stepCreator.FileSaveFlag = exportData["exportData"]["exportSettings"]["fileSaveFlag"]    # mod
    stepCreator.LayerMask = exportData["exportData"]["exportSettings"]["layerMask"]  # mod
    bodyToExport = workPart.Bodies.FindObject(exportData["exportData"]["session"]["body"])     # mod    # Single body to export
 
    # From combined workdir + ./myStepData.json
    stepCreator.InputFile = os.path.join(argPath, exportData["exportData"]["filename"]["inputPrt"] + '.prt')       # mod
    stepCreator.OutputFile = os.path.join(argPath, exportData["exportData"]["filename"]["outputStep"] + '.stp')     # mod
    
    # Based on json data
    added = stepCreator.ExportSelectionBlock.SelectionComp.Add(bodyToExport)
    stepCreator.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.SelectedObjects

    # End
    nXObject1 = stepCreator.Commit()    
    stepCreator.Destroy()
    
if __name__ == '__main__':
    main(sys.argv[1])
