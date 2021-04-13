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

from pathlib import Path

def main(): 
    # Initiate session
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    # Export to AP214
    stepCreator = theSession.DexManager.CreateStepCreator()
    stepCreator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    
    stepCreator.OutputFile = "C:\\Mallit\\DI\\NX\\v1\\Combined Results\\EXPORT-to-FEM\\combined-to-FEM-v1.stp"      # TODO : to myStepData.json
    
    # Replace path if your NX is not installed to default directory
    stepCreator.SettingsFile = "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\ugstep214.def"
    
    stepCreator.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.SelectedObjects
    
    stepCreator.ColorAndLayers = True
    
    stepCreator.BsplineTol = 0.01                               # TODO : to myStepData.json
    
    stepCreator.Author = "Janne Lehtimäki"                      # TODO : to myStepData.json
    stepCreator.Company = "Etteplan"                            # TODO : to myStepData.json
    
    stepCreator.InputFile = "C:\\Mallit\\DI\\nTop\\dev\\1-nTpCL\\m1-root.prt"                           # TODO : make dynamic, detect from session
    stepCreator.OutputFile = "C:\\Mallit\\DI\\NX\\v1\\Combined Results\\EXPORT-to-FEM\\m1-root.stp"     # TODO :  combined:  myStepData.json - dynamic from session
    
    bodyToExport = workPart.Bodies.FindObject("EXTRUDE(3)")     # TODO : to myStepData.json
    added1 = stepCreator.ExportSelectionBlock.SelectionComp.Add(bodyToExport)
    
    stepCreator.FileSaveFlag = False
    
    stepCreator.LayerMask = "1-256"
    
    nXObject1 = stepCreator.Commit()
    

    theSession.SetUndoMarkName(markId1, "Export to STEP Options")
    
    stepCreator.Destroy()
    
if __name__ == '__main__':
    main()