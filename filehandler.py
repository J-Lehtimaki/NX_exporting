# Ver 0.1
# Janne Lehtimäki
# janne.lehtimaki@etteplan.com
# Etteplan Finland Oy

import json
import os
import glob
import time

import NXOpen
from pathlib import Path

class StepFileHandler():
    def __init__(self, rootDir):
        self.rootDir_ = Path(rootDir)
        #raise ValueError(os.path.join(self.rootDir_, 'python', 'mySolid_from_NX_3.stp'))
        self.commonData_ = {}
        self.NXData_ = {}
        self.nTopCLData_ = {}
        self.initPipeData()
        # Export filenames set during export process based on versioning
        self.NXExportPath_ = ''
        self.nTopExportPath_ = ''

    def initPipeData(self):
        jsonPath = os.path.join(self.rootDir_, 'python', 'pipeData.json')
        f = open(jsonPath)
        jsonData = json.load(f)
        f.close()
        self.commonData_ = jsonData['project']['common']
        self.NXData_ = jsonData['project']['NX']
        self.nTopCLData_ = jsonData['project']['nTopology']

    # Description:
    #   Creates absolute path for export destination with filename.
    #   Automatically increments version number for file if "automaticIncrement"
    #   flag is true.
    # Return:
    #   Path - Absolute path to export destination
    def exportNameNX(self):
        exportNameNX = '\\' + self.commonData_['exportBaseName'] + '_from_NX'
        if(self.commonData_['automaticIncrement']):
            exportNameNX += '_' + str(self.incrementFileNameNumberingNX())
        exportNameNX += '.stp'
        self.NXExportPath_ = str(self.rootDir_) + exportNameNX
        return self.NXExportPath_
 
    # TODO Description: TODO TEST
    #   Returns list of .stp files in the argument folder
    def folderContentStep(self):
        existingVersions = []
        regexPath = str(self.rootDir_) + '/**/' + self.commonData_["exportBaseName"] + '*.stp'
        # Add all files names to list that was found
        for file in glob.iglob(regexPath, recursive=True):
            existingVersions.append(str(os.path.basename(file)))
        return existingVersions

    # Description:
    #   Determines what version number will be added to .stp -file basename
    # Return:
    #   Integer to be added
    def incrementFileNameNumberingNX(self):
        existingVersions = self.folderContentStep()
        # Find the one with greatest version number
        if(len(existingVersions) == 0 ):
            return "1"
        else:
            # Latest export is first in descending list
            existingVersions.sort(reverse=True)
            latest = existingVersions[0]
            latest = latest[:len(latest) - 4]   # remove .stp -extension
            splitted = latest.split('_')
            number = splitted[len(splitted) - 1]
            if(number == '' or number == 'NX'):
                return "1"
            return str(int(number) + 1)

    # Description:
    #   Prevents commit if selected filename already exists and overWriteProtection
    #   is set active.
    # Exception:
    #   ValueError - File already exists, change name or turn off over-write -protection
    def overwriteProtection(self):
        pass

    # Description:
    #   Sets parameters for exporting body from NX and commits
    # Parameters:
    #   (1), StepCreator - NXOpenAPI class for creating steps
    #   (2), WorkPart - NXOpenAPI class for active part in session 
    def exportSolidNX(self, stepCreator, workPart):
        stepCreator.Author = self.commonData_['author']
        stepCreator.Company = self.commonData_['company']
        stepCreator.SettingsFile = self.NXData_['exportSettings']['settingsFile']
        stepCreator.ColorAndLayers = self.NXData_['exportSettings']['colorAndLayers']
        stepCreator.BsplineTol = self.NXData_['exportSettings']['bSplineTol']
        stepCreator.FileSaveFlag = self.NXData_['exportSettings']['fileSaveFlag']
        stepCreator.LayerMask = self.NXData_['exportSettings']['layerMask']

        # Inputfile is the active .prt
        stepCreator.InputFile = os.path.join(self.rootDir_, self.NXData_['inputPrt'])
        exportedPath = self.exportNameNX()

        stepCreator.OutputFile = exportedPath

        bodyToExport = workPart.Bodies.FindObject(self.NXData_['body'])    # TODO: Multiple body option
        stepCreator.ExportSelectionBlock.SelectionComp.Add(bodyToExport)
        stepCreator.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.SelectedObjects

        stepCreator.Commit()
        return exportedPath

    def importStepNX(self, step214Importer, exportedPath):
        step214Importer.SimplifyGeometry = self.NXData_['importSettings']['simplifyGeometry']
        step214Importer.LayerDefault = self.NXData_['importSettings']['layerDefault']
        step214Importer.SettingsFile = self.NXData_['importSettings']['settingsFile']
        step214Importer.ObjectTypes.Curves = self.NXData_['importSettings']['objectTypes']['curves']
        step214Importer.ObjectTypes.Surfaces = self.NXData_['importSettings']['objectTypes']['surfaces']
        step214Importer.ObjectTypes.PmiData = self.NXData_['importSettings']['objectTypes']['pmiData']
        step214Importer.FileOpenFlag = self.NXData_['importSettings']['fileOpenFlag']

        step214Importer.InputFile = exportedPath
        step214Importer.OutputFile = exportedPath[:len(exportedPath) - 4] + '.prt'

        nXObject1 = step214Importer.Commit()