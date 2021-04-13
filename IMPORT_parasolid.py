# NX 12.0.0.27
# Journal created by ett17801 on Mon Apr  5 20:29:32 2021 FLE Daylight Time
#
import math
import NXOpen
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: File->Import->Parasolid...
    # ----------------------------------------------

    ParaSolidImporter = workPart.ImportManager.CreateParasolidImporter()
    ParaSolidImporter.FileName = "C:\\Mallit\\DI\\nTop\\dev\\1-nTpCL\\smoothen\\mySolid_from_nTop_9.stp.X_T"
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Parasolid Import")
    nXObject1 = ParaSolidImporter.Commit()
    ParaSolidImporter.Destroy()

    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()