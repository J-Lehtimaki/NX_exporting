# Author: Janne Lehtimäki, Etteplan
# Description:
# - Convert .STP -files in the desired directory into .PRT -files
#   with same base name

# How to use:
# - Run file in the open session
# - Give parameter to folder containing all the .STP -files to convert into .PRT

# sys.argv[1] = Path where you want the conversion to happen

# Thread-safety: None

import math
import sys
import glob
import os

import NXOpen
import NXOpen.Assemblies
import NXOpen.Assemblies.ProductInterface
import NXOpen.PDM
import NXOpen.Positioning
import NXOpen.Preferences

class PartPositioner:
    def __init__(self, directory):
        self.rootFolderPath_ = directory
        self.stpFileNames_ = self.folderContentStep(directory)
        self.positionData_ = self.createPositions(self.stpFileNames_)

    def folderContentStep(self, dir):
        existingVersions = []
        regexPath = dir + '/**/' + '*.stp'
        # Add all files names to list that was found
        for file in glob.iglob(regexPath, recursive=True):
            existingVersions.append(str(os.path.basename(file)))
        return existingVersions

    def createPositions(self, stpFileNames):
        positionData = []
        xPos, yPos, zPos = 0, 0, 0
        for file in self.stpFileNames_:
            plainName = file.strip('.stp')
            stpName = plainName + '.stp'
            prtName = plainName + '.prt'
            absPathStp = os.path.join(self.rootFolderPath_, stpName)
            absPathPrt = os.path.join(self.rootFolderPath_, prtName)
            positionData.append([   # During dev, do not change the indexes, change values in them
                prtName,
                absPathPrt,
                xPos,
                yPos,
                zPos,
                stpName,
                absPathStp])
            # TODO: incrementation logics
            yPos -= 50
        return positionData

    def getPositionData(self):
        return self.positionData_

class StepToPartCreator:
    def __init__(self, CurrentSessionNX):
        self.CurrentSessionNX_ = CurrentSessionNX

    def createPartFromStep(self, inputStpPath, outputPrtPath):
        step214Importer1 = self.CurrentSessionNX_.DexManager.CreateStep214Importer()
        step214Importer1.InputFile = inputStpPath   #
        step214Importer1.OutputFile = outputPrtPath  #
        step214Importer1.LayerDefault = 1
        step214Importer1.SettingsFile = "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\step214ug.def"
        step214Importer1.ObjectTypes.Curves = False
        step214Importer1.ObjectTypes.Surfaces = False
        step214Importer1.ObjectTypes.PmiData = False
        step214Importer1.SimplifyGeometry = False
        step214Importer1.FileOpenFlag = False

        step214Importer1.ImportTo = NXOpen.Step214Importer.ImportToOption.NewPart

        nXObject1 = step214Importer1.Commit()
        step214Importer1.Destroy()

def main(arg):
    # Initiate NX session
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    # Read folder content and form conversion and matrix position data
    positioner = PartPositioner(arg)
    partData = positioner.getPositionData()    # [prtName, prtAbsPath, x, y, z, stpName, absPathStp]

    stpToPrtConverter = StepToPartCreator(theSession)

    #   Menu: Assemblies->Components->Add Component...
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")    # This should enable 'Ctrl - Z" after playing journal

    for i in range(0, len(partData)):
        stpToPrtConverter.createPartFromStep(partData[i][6], partData[i][1])

    theSession.SetUndoMarkName(markId1, "Add Component Dialog")     # This should enable 'Ctrl - Z" after playing journal

if __name__ == '__main__':
    main(sys.argv[1])