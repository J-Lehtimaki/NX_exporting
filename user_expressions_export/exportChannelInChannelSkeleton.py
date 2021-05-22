stepCreator1.SettingsFile = "C:\\Program Files\\Siemens\\NX 12.0\\step214ug\\ugstep214.def"
stepCreator1.InputFile = "C:\\Mallit\\DI\\NX\\v2\\channel_inverse.prt"
stepCreator1.OutputFile = "C:\\Mallit\\DI\\nTop\\miscShit\\Input\\SOLID\\channel_inverse.stp"


component1 = displayPart.ComponentAssembly.RootComponent.FindObject("COMPONENT channel_skeleton 1")
component2 = component1.FindObject("COMPONENT channel_inverse 1")
body1 = component2.FindObject("PROTO#.Bodies|CABLE(4)")
body2 = component2.FindObject("PROTO#.Bodies|CABLE(5)")
added1 = stepCreator1.ExportSelectionBlock.SelectionComp.Add(body1)
added2 = stepCreator1.ExportSelectionBlock.SelectionComp.Add(body2)

stepCreator1.OutputFile = "C:\\Mallit\\DI\\NX\\python\\channel_inverse.stp"
