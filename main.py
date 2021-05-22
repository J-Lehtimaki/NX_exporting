# Janne Lehtimäki
# janne.lehtimaki@etteplan.com
# Etteplan Finland Oy

# NX 12.0.0.27
# Description:
# - Export parametetric configurations of single part by modifying
#   user expressions inside NX
# - Edit user expressions in this file: [name, values[]], and all possible variations
#   will be then exported automatically. Be sure that name matches the existing
#   user expression in .prt -file.
# - Place this script in location of your .prt files you have to modify
# - Run via NXJournal
import json
import os
import sys
import time

import NXOpen
from pathlib import Path
from filehandler import StepFileHandler

# Folder where your pars will be saved (here ./channels_step_files)
OUT_DIR = r"C:/Mallit/DI/NX/v2/channels_step_files2"

# 1) Create variables for classical parametrisation
#DEG_PUSHROD_SIDE = [120, 97, 74, 51, 28, 5, -20]        # Used to create 'channel_x_y'
#DEG_VALVE_SIDE = [220, 207, 194, 181, 168, 155, 140]    # used to create 'channel_x_y'
# phase1 DEG_PUSHROD_SIDE = [80, 69, 57, 46, 34, 23, 0]        # Used to create 'channel2_x_y'
# phase1 DEG_VALVE_SIDE = [15, 2, -12, -26, -52, -66, -80]    # used to create 'channel2_x_y'
DEG_PUSHROD_SIDE = [30, 15, 0, -15, -30, -45, -60]        # Used to create 'channel2_x_y'
DEG_VALVE_SIDE = [50, 36, 23, 10, -3, -16, -30]    # used to create 'channel2_x_y'


# wdir/sys.argv[2]_degPr_deg_V.stp
# Variant is saved, and variables make the ID for the part
def makeExportPath(degPr, degV):
    f = '{name}_{dpr}_{dv}.stp'.format(name=sys.argv[1], dpr=str(degPr), dv=str(degV))
    p = os.path.join(OUT_DIR, f)
    return p

def getExportData(degPr, degV):
    result = {
        "author" : "Janne Lehtimäki",
        "company" : "Etteplan",
        "settingsFile" : "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\ugstep214.def",
        "colorsAndLayers" : True,
        "bSplineTol" : 0.01,
        "fileSaveFlag" : False,
        "layerMask" : "1-256",
        "outputFile" : makeExportPath(degPr, degV)
    }
    return result

def main(partName):
    # 0) Initiate NX Session
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # 0.1) Get unit types for variable changes
    DegreesTypeNX = workPart.UnitCollection.FindObject("Degrees")   # Unit type from NX for degree

    # 0.1) Create step generator NXOpen
    # stepCreator = theSession.DexManager.CreateStepCreator()
    # stepCreator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214

    # 1.1) Find workpart which expressions is to be modified
    c1 = displayPart.ComponentAssembly.RootComponent.FindObject("COMPONENT channel_skeleton 1")
    partLoadStatus1 = theSession.Parts.SetWorkComponent(
        c1,
        NXOpen.PartCollection.RefsetOption.Entire,
        NXOpen.PartCollection.WorkComponentOption.Visible)
    workPart = theSession.Parts.Work
    partLoadStatus1.Dispose()
    # 1.2) Find workpart what to be exported
    c2 = c1.FindObject("COMPONENT channel_inverse 1")
    # 1.3) Select bodies to export
    #b1 = c2.FindObject("PROTO#.Bodies|CABLE(10)")
    #b2 = c2.FindObject("PROTO#.Bodies|CABLE(12)")
    b1 = c2.FindObject("PROTO#.Bodies|SWEPT(20)")
    b2 = c2.FindObject("PROTO#.Bodies|SWEPT(16)")

    # 2) Instantiate variables to modify from current NX Session
    degPushrodSide = workPart.Expressions.FindObject("DEG_PUSHROD_SIDE")
    degValveSide = workPart.Expressions.FindObject("DEG_VALVE_SIDE")

    # 4) Iterate over all possible variable configurations
    for i in DEG_PUSHROD_SIDE:
        # Change expression i
        workPart.Expressions.EditWithUnits(degPushrodSide, DegreesTypeNX, str(i))
        # increment i

        for j in DEG_VALVE_SIDE:
            # Change expression j
            workPart.Expressions.EditWithUnits(degValveSide, DegreesTypeNX, str(j))
            # increment j

            # STEP 1: Export solid from NX, use stepCreator
            # Create step generator NXOpen
            stepCreator = theSession.DexManager.CreateStepCreator()
            stepCreator.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
            # Get exportdata
            dataExport = getExportData(i,j)

            stepCreator.Author = dataExport["author"]
            stepCreator.Company = dataExport["company"]
            stepCreator.SettingsFile = dataExport["settingsFile"]
            stepCreator.ColorAndLayers = dataExport["colorsAndLayers"]
            stepCreator.BsplineTol = dataExport["bSplineTol"]
            stepCreator.FileSaveFlag = dataExport["fileSaveFlag"]
            stepCreator.LayerMask = dataExport["layerMask"]
            stepCreator.OutputFile = dataExport["outputFile"]

            added1 = stepCreator.ExportSelectionBlock.SelectionComp.Add(b1)
            added2 = stepCreator.ExportSelectionBlock.SelectionComp.Add(b2)

            stepCreator.Commit()
            stepCreator.Destroy()

if __name__ == '__main__':
    main(sys.argv[1])  # Current path, assembly component name
