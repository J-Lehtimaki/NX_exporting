# NX 12.0.0.27
# Journal created by ett17801 on Wed Apr 14 08:47:15 2021 FLE Daylight Time
#
import math
import NXOpen
import NXOpen.Assemblies
import NXOpen.Assemblies.ProductInterface
import NXOpen.PDM
import NXOpen.Positioning
import NXOpen.Preferences
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: File->Import->STEP214...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    step214Importer1 = theSession.DexManager.CreateStep214Importer()
    
    step214Importer1.SimplifyGeometry = True
    
    step214Importer1.LayerDefault = 1
    
    step214Importer1.InputFile = "C:\\Mallit\\DI\\nTop\\dev\\1-nTpCL\\mySolid_from_NX_10.stp"
    
    step214Importer1.OutputFile = "C:\\Mallit\\DI\\nTop\\dev\\1-nTpCL\\mySolid_from_NX_10.prt"
    
    step214Importer1.SettingsFile = "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\step214ug.def"
    
    step214Importer1.ObjectTypes.Curves = False
    
    step214Importer1.ObjectTypes.Surfaces = False
    
    step214Importer1.ObjectTypes.PmiData = False
    
    step214Importer1.SimplifyGeometry = False
    
    step214Importer1.InputFile = ""
    
    step214Importer1.OutputFile = ""
    
    theSession.SetUndoMarkName(markId1, "Import STEP214 Dialog")
    
    step214Importer1.ImportTo = NXOpen.Step214Importer.ImportToOption.NewPart
    
    step214Importer1.InputFile = "C:\\Mallit\\DI\\NX\\v2\\channels_step_files\\channel_28_194.stp"
    
    step214Importer1.OutputFile = "C:\\Mallit\\DI\\NX\\v2\\channels_step_files\\channel_28_194.prt"
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Import STEP214")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Import STEP214")
    
    step214Importer1.FileOpenFlag = False
    
    nXObject1 = step214Importer1.Commit()
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Import STEP214")
    
    step214Importer1.Destroy()
    
    # ----------------------------------------------
    #   Menu: Assemblies->Components->Add Component...
    # ----------------------------------------------
    markId4 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    addComponentBuilder1 = workPart.AssemblyManager.CreateAddComponentBuilder()
    
    componentPositioner1 = workPart.ComponentAssembly.Positioner
    
    componentPositioner1.ClearNetwork()
    
    componentPositioner1.BeginAssemblyConstraints()
    
    allowInterpartPositioning1 = theSession.Preferences.Assemblies.InterpartPositioning
    
    expression1 = workPart.Expressions.CreateSystemExpressionWithUnits("1.0", NXOpen.Unit.Null)
    
    unit1 = workPart.UnitCollection.FindObject("MilliMeter")
    expression2 = workPart.Expressions.CreateSystemExpressionWithUnits("6.28319", unit1)
    
    expression3 = workPart.Expressions.CreateSystemExpressionWithUnits("0.0", unit1)
    
    unit2 = workPart.UnitCollection.FindObject("Degrees")
    expression4 = workPart.Expressions.CreateSystemExpressionWithUnits("0.0", unit2)
    
    expression5 = workPart.Expressions.CreateSystemExpressionWithUnits("1", NXOpen.Unit.Null)
    
    expression6 = workPart.Expressions.CreateSystemExpressionWithUnits("6.28319", unit1)
    
    expression7 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    expression8 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit2)
    
    network1 = componentPositioner1.EstablishNetwork()
    
    componentNetwork1 = network1
    componentNetwork1.MoveObjectsState = True
    
    componentNetwork1.DisplayComponent = NXOpen.Assemblies.Component.Null
    
    theSession.SetUndoMarkName(markId4, "Add Component Dialog")
    
    componentNetwork1.MoveObjectsState = True
    
    markId5 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Assembly Constraints Update")
    
    addComponentBuilder1.SetComponentAnchor(NXOpen.Assemblies.ProductInterface.InterfaceObject.Null)
    
    addComponentBuilder1.SetInitialLocationType(NXOpen.Assemblies.AddComponentBuilder.LocationType.Snap)
    
    addComponentBuilder1.SetCount(1)
    
    addComponentBuilder1.SetScatterOption(True)
    
    addComponentBuilder1.ReferenceSet = "Unknown"
    
    addComponentBuilder1.Layer = -1
    
    basePart1, partLoadStatus1 = theSession.Parts.OpenBase("C:\\Mallit\\DI\\NX\\v2\\channels_step_files\\channel_28_194.prt")
    
    partLoadStatus1.Dispose()
    addComponentBuilder1.ReferenceSet = "Entire Part"
    
    addComponentBuilder1.Layer = -1
    
    partstouse1 = [NXOpen.BasePart.Null] * 1 
    part1 = basePart1
    partstouse1[0] = part1
    addComponentBuilder1.SetPartsToAdd(partstouse1)
    
    productinterfaceobjects1 = addComponentBuilder1.GetAllProductInterfaceObjects()
    
    arrangement1 = workPart.ComponentAssembly.Arrangements.FindObject("Arrangement 1")
    componentPositioner1.PrimaryArrangement = arrangement1
    
    coordinates1 = NXOpen.Point3d(-49.461433803353231, -56.36232965739498, 0.0)
    point1 = workPart.Points.CreatePoint(coordinates1)
    
    coordinates2 = NXOpen.Point3d(-49.461433803353231, -56.36232965739498, 0.0)
    point2 = workPart.Points.CreatePoint(coordinates2)
    
    origin1 = NXOpen.Point3d(-49.461433803353231, -56.36232965739498, 0.0)
    vector1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    direction1 = workPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    origin2 = NXOpen.Point3d(-49.461433803353231, -56.36232965739498, 0.0)
    vector2 = NXOpen.Vector3d(1.0, 0.0, 0.0)
    direction2 = workPart.Directions.CreateDirection(origin2, vector2, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    origin3 = NXOpen.Point3d(-49.461433803353231, -56.36232965739498, 0.0)
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
    
    point3 = NXOpen.Point3d(-49.461433803353231, -56.36232965739498, 0.0)
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
    
    markId6 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Add Component")
    
    theSession.DeleteUndoMark(markId6, None)
    
    markId7 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Add Component")
    
    markId8 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "AddComponent on_apply")
    
    componentNetwork1.Solve()
    
    componentPositioner1.ClearNetwork()
    
    nErrs1 = theSession.UpdateManager.AddToDeleteList(componentNetwork1)
    
    nErrs2 = theSession.UpdateManager.DoUpdate(markId5)
    
    componentPositioner1.EndAssemblyConstraints()
    
    logicalobjects1 = addComponentBuilder1.GetLogicalObjectsHavingUnassignedRequiredAttributes()
    
    addComponentBuilder1.ComponentName = "CHANNEL_28_194"
    
    nXObject2 = addComponentBuilder1.Commit()
    
    errorList1 = addComponentBuilder1.GetOperationFailures()
    
    errorList1.Dispose()
    theSession.DeleteUndoMark(markId7, None)
    
    theSession.SetUndoMarkName(markId4, "Add Component")
    
    addComponentBuilder1.Destroy()
    
    componentPositioner1.PrimaryArrangement = NXOpen.Assemblies.Arrangement.Null
    
    theSession.DeleteUndoMark(markId5, None)
    
    workPart.Points.DeletePoint(point1)
    
    rotMatrix1 = NXOpen.Matrix3x3()
    
    rotMatrix1.Xx = -0.84794321589370925
    rotMatrix1.Xy = 0.49404801563336581
    rotMatrix1.Xz = -0.19211678965818924
    rotMatrix1.Yx = -0.26061176032206362
    rotMatrix1.Yy = -0.072940571917686242
    rotMatrix1.Yz = 0.96268436330406648
    rotMatrix1.Zx = 0.4615991908589866
    rotMatrix1.Zy = 0.86636956965088119
    rotMatrix1.Zz = 0.19060418615884336
    translation1 = NXOpen.Point3d(-64.052763154437002, -5.3473589125261469, 25.632800765552208)
    workPart.ModelingViews.WorkView.SetRotationTranslationScale(rotMatrix1, translation1, 1.2336309523809526)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()