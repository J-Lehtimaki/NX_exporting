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
import ENVIRONMENT

# 1) Create variables for classical parametrisation
DEG_PUSHROD_SIDE = [-20, -5, 10, 15, 30, 55]        # Used to create 'channel2_x_y'
DEG_VALVE_SIDE = [-30, -15, 0, 15, 30, 50]    # used to create 'channel2_x_y'

# wdir/sys.argv[2]_degPr_deg_V.stp
# Variant is saved, and variables make the ID for the part
def makeExportPath(name, id):
    f = '{n}_{i}.stp'.format(n=name, i=id)
    p = os.path.join(ENVIRONMENT.TASK_CONSTS["stp_output_folder"], f)
    return p

def getExportData(name,id):
    result = {
        "author" : "Janne Lehtimäki",
        "company" : "Etteplan",
        "settingsFile" : ENVIRONMENT.TASK_CONSTS["NX_step214ug_settings"],
        "colorsAndLayers" : True,
        "bSplineTol" : 0.01,
        "fileSaveFlag" : False,
        "layerMask" : "1-256",
        "outputFile" : makeExportPath(name,id)
    }
    return result

def main():
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
    #c1 = displayPart.ComponentAssembly.RootComponent.FindObject(ENVIRONMENT.TASK_CONSTS["NX_assembly_component"])
    #partLoadStatus1 = theSession.Parts.SetWorkComponent(
    #    c1,
    #    NXOpen.PartCollection.RefsetOption.Entire,
    #    NXOpen.PartCollection.WorkComponentOption.Visible)
    #workPart = theSession.Parts.Work
    #partLoadStatus1.Dispose()

    # 1.3) Select bodies to export
    b1 = workPart.Bodies.FindObject("SWEPT(29)")
    b2 = workPart.Bodies.FindObject("SWEPT(30)")
    b3 = workPart.Bodies.FindObject("SWEPT(31)")
    b4 = workPart.Bodies.FindObject("SWEPT(32)")

    # 2) Instantiate variables to modify from current NX Session
    degPushrodSide = workPart.Expressions.FindObject("PR_angle")
    degValveSide = workPart.Expressions.FindObject("V_angle")

    partID = 0

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
            dataExport = getExportData(ENVIRONMENT.TASK_CONSTS["file_base_name"], partID)

            stepCreator.Author = dataExport["author"]
            stepCreator.Company = dataExport["company"]
            stepCreator.SettingsFile = dataExport["settingsFile"]
            stepCreator.ColorAndLayers = dataExport["colorsAndLayers"]
            stepCreator.BsplineTol = dataExport["bSplineTol"]
            stepCreator.FileSaveFlag = dataExport["fileSaveFlag"]
            stepCreator.LayerMask = dataExport["layerMask"]
            stepCreator.OutputFile = dataExport["outputFile"]

            # Add all the sweeps to be exported
            stepCreator.ExportSelectionBlock.SelectionComp.Add(b1)
            stepCreator.ExportSelectionBlock.SelectionComp.Add(b2)
            stepCreator.ExportSelectionBlock.SelectionComp.Add(b3)
            stepCreator.ExportSelectionBlock.SelectionComp.Add(b4)

            stepCreator.Commit()
            stepCreator.Destroy()

            # Increment ID for next export
            partID += 1

if __name__ == '__main__':
    main()
