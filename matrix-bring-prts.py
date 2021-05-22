# Author: Janne Lehtimäki, Etteplan
# Description:
# - Convert .STP -files in the desired directory into .PRT -files
#   with same base name

# How to use:
# - Open new NX-assembly
# - Run file in the open session
#    - Give parameter to folder containing all the family members .prt -files and the
#    data.csv that contains the file names and xyz -coordinates
# - NX now loads all the parts from that directory to the assembly, without making
#   any constraints between parts

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
        xPos, yPos, zPos = 0.0, 0.0, 150.0
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
            yPos -= 50.0
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

        addComponentBuilder1 = workPart.AssemblyManager.CreateAddComponentBuilder()
        componentPositioner1 = workPart.ComponentAssembly.Positioner
        componentPositioner1.ClearNetwork()

        componentPositioner1.BeginAssemblyConstraints()

        allowInterpartPositioning1 = theSession.Preferences.Assemblies.InterpartPositioning

        unit1 = workPart.UnitCollection.FindObject("MilliMeter")
        unit2 = workPart.UnitCollection.FindObject("Degrees")

        network1 = componentPositioner1.EstablishNetwork()

        addComponentBuilder1.SetComponentAnchor(NXOpen.Assemblies.ProductInterface.InterfaceObject.Null)
        addComponentBuilder1.SetInitialLocationType(NXOpen.Assemblies.AddComponentBuilder.LocationType.Snap)
        addComponentBuilder1.SetCount(1)
        addComponentBuilder1.SetScatterOption(True)
        addComponentBuilder1.ReferenceSet = "Unknown"
        addComponentBuilder1.Layer = -1

        basePart1, partLoadStatus1 = theSession.Parts.OpenBase(partData[i][1])

        partLoadStatus1.Dispose()
        addComponentBuilder1.ReferenceSet = "Entire Part"

        partstouse1 = [NXOpen.BasePart.Null] * 1 
        part1 = basePart1
        partstouse1[0] = part1
        addComponentBuilder1.SetPartsToAdd(partstouse1)

        productinterfaceobjects1 = addComponentBuilder1.GetAllProductInterfaceObjects()

        # # POSITIO TÄÄLLÄ
        coordinates1 = NXOpen.Point3d(partData[i][2], partData[i][3], partData[i][4])
        point1 = workPart.Points.CreatePoint(coordinates1)

        # # POSITIO TÄÄLLÄ
        coordinates2 = NXOpen.Point3d(partData[i][2], partData[i][3], partData[i][4])
        point2 = workPart.Points.CreatePoint(coordinates2)

        # # POSITIO TÄÄLLÄ
        origin1 = NXOpen.Point3d(partData[i][2], partData[i][3], partData[i][4])
        vector1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
        direction1 = workPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.WithinModeling)

        # # POSITIO TÄÄLLÄ
        origin2 = NXOpen.Point3d(partData[i][2], partData[i][3], partData[i][4])
        vector2 = NXOpen.Vector3d(1.0, 0.0, 0.0)
        direction2 = workPart.Directions.CreateDirection(origin2, vector2, NXOpen.SmartObject.UpdateOption.WithinModeling)

        # # POSITIO TÄÄLLÄ
        origin3 = NXOpen.Point3d(partData[i][2], partData[i][3], partData[i][4])
        matrix1 = NXOpen.Matrix3x3()
        matrix1.Xx = 1.0
        matrix1.Xy = 0.0
        matrix1.Xz = 0.0
        matrix1.Yx = 0.0
        matrix1.Yy = 1.0
        matrix1.Yz = 0.0
        matrix1.Zx = 0.0
        matrix1.Zy = 0.0
        matrix1.Zz = 1.0

        plane1 = workPart.Planes.CreateFixedTypePlane(origin3, matrix1, NXOpen.SmartObject.UpdateOption.WithinModeling)
        xform1 = workPart.Xforms.CreateXformByPlaneXDirPoint(plane1, direction2, point2, NXOpen.SmartObject.UpdateOption.WithinModeling, 0.625, False, False)
        cartesianCoordinateSystem1 = workPart.CoordinateSystems.CreateCoordinateSystem(xform1, NXOpen.SmartObject.UpdateOption.WithinModeling)

        # # POSITIO TÄÄLLÄ
        point3 = NXOpen.Point3d(partData[i][2], partData[i][3], partData[i][4])
        orientation1 = NXOpen.Matrix3x3()
        orientation1.Xx = 1.0
        orientation1.Xy = 0.0
        orientation1.Xz = 0.0
        orientation1.Yx = 0.0
        orientation1.Yy = 1.0
        orientation1.Yz = 0.0
        orientation1.Zx = 0.0
        orientation1.Zy = 0.0
        orientation1.Zz = 1.0
        addComponentBuilder1.SetInitialLocationAndOrientation(point3, orientation1)

        addComponentBuilder1.SetKeepConstraintsOption(False)

        componentPositioner1.ClearNetwork()
        componentPositioner1.EndAssemblyConstraints()

        logicalobjects1 = addComponentBuilder1.GetLogicalObjectsHavingUnassignedRequiredAttributes()
        addComponentBuilder1.ComponentName = partData[i][0].upper()

        nXObject1 = addComponentBuilder1.Commit()

        # END addComponentBuilder
        errorList1 = addComponentBuilder1.GetOperationFailures()
        errorList1.Dispose()
        addComponentBuilder1.Destroy()
        componentPositioner1.PrimaryArrangement = NXOpen.Assemblies.Arrangement.Null
        workPart.Points.DeletePoint(point1)

    theSession.SetUndoMarkName(markId1, "Add Component Dialog")     # This should enable 'Ctrl - Z" after playing journal

if __name__ == '__main__':
    main(sys.argv[1])