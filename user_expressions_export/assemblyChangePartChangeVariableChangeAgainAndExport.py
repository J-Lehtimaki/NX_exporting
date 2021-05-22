# NX 12.0.0.27
# Journal created by ett17801 on Tue Apr 13 18:41:37 2021 FLE Daylight Time
#
import math
def main(): 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    component1 = displayPart.ComponentAssembly.RootComponent.FindObject("COMPONENT channel_skeleton 1")         # PICK THE COMPONENT THAT HAS THE VARIABLES
    partLoadStatus1 = theSession.Parts.SetWorkComponent(component1, NXOpen.PartCollection.RefsetOption.Entire, NXOpen.PartCollection.WorkComponentOption.Visible)
    
    workPart = theSession.Parts.Work # channel_skeleton
    partLoadStatus1.Dispose()

    
    expression1 = workPart.Expressions.FindObject("DEG_PUSHROD_SIDE")
    unit1 = workPart.UnitCollection.FindObject("Degrees")
    workPart.Expressions.EditWithUnits(expression1, unit1, "20")
    
    theSession.Preferences.Modeling.UpdatePending = False
    
    nErrs1 = theSession.UpdateManager.DoUpdate(markId2)
    
    theSession.Preferences.Modeling.UpdatePending = False
    
    # ----------------------------------------------
    #   Menu: File->Export->STEP...
    # ----------------------------------------------

    stepCreator1 = theSession.DexManager.CreateStepCreator()
    
    stepCreator1.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    
    stepCreator1.OutputFile = "C:\\Mallit\\DI\\NX\\python\\channel_inverse.stp"
    
    stepCreator1.SettingsFile = "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\ugstep214.def"
    
    stepCreator1.ExportSelectionBlock.SelectionScope = NXOpen.ObjectSelector.Scope.SelectedObjects
    
    stepCreator1.ColorAndLayers = True
    
    stepCreator1.BsplineTol = 0.01
    
    stepCreator1.Author = "Etteplan"
    
    stepCreator1.Company = "Etteplan"
    
    stepCreator1.InputFile = "C:\\Mallit\\DI\\NX\\v2\\channel_skeleton.prt"
    
    stepCreator1.OutputFile = "C:\\Mallit\\DI\\NX\\python\\channel_skeleton.stp"


    component2 = component1.FindObject("COMPONENT channel_inverse 1")       # SELECT THE COMPONENT TO EXPORT
    body1 = component2.FindObject("PROTO#.Bodies|CABLE(4)")                 # SELECT THE BODY TO EXPORT
    added1 = stepCreator1.ExportSelectionBlock.SelectionComp.Add(body1)     # add body to export
    
    stepCreator1.OutputFile = "C:\\Mallit\\DI\\NX\\python\\asdasd.stp"      # set exportt


    stepCreator1.FileSaveFlag = False
    
    stepCreator1.LayerMask = "1-256"
    
    nXObject1 = stepCreator1.Commit()


    stepCreator1.Destroy()
    
