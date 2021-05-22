# NX 12.0.0.27
# Journal created by ett17801 on Tue Apr 13 12:39:48 2021 FLE Daylight Time
#
import math
import NXOpen
import NXOpen.Assemblies
import NXOpen.MenuBar
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    
    component1 = displayPart.ComponentAssembly.RootComponent.FindObject("COMPONENT DS1 1")
    partLoadStatus1 = theSession.Parts.SetWorkComponent(component1, NXOpen.PartCollection.RefsetOption.Entire, NXOpen.PartCollection.WorkComponentOption.Visible)
    
    workPart = theSession.Parts.Work # DS1
    partLoadStatus1.Dispose()
    theSession.SetUndoMarkName(markId1, "Make Work Part")
    
    
    component2 = displayPart.ComponentAssembly.RootComponent.FindObject("COMPONENT channel_skeleton 1")
    partLoadStatus2 = theSession.Parts.SetWorkComponent(component2, NXOpen.PartCollection.RefsetOption.Entire, NXOpen.PartCollection.WorkComponentOption.Visible)
    
    workPart = theSession.Parts.Work # channel_skeleton
    partLoadStatus2.Dispose()
    theSession.SetUndoMarkName(markId2, "Make Work Part")
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Make Work Part")
    
    component3 = component2.FindObject("COMPONENT channel_inverse 1")
    partLoadStatus3 = theSession.Parts.SetWorkComponent(component3, NXOpen.PartCollection.RefsetOption.Entire, NXOpen.PartCollection.WorkComponentOption.Visible)
    
    workPart = theSession.Parts.Work # channel_inverse
    partLoadStatus3.Dispose()
    theSession.SetUndoMarkName(markId3, "Make Work Part")
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()