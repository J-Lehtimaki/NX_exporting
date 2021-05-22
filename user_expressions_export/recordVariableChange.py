# NX 12.0.0.27
# Journal created by ett17801 on Sat Apr 10 23:53:16 2021 FLE Daylight Time
#
import math
import NXOpen
import NXOpen.Preferences
def main():
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    expression = workPart.Expressions.FindObject("channelPRAngle")
    unit = workPart.UnitCollection.FindObject("Degrees")
    workPart.Expressions.EditWithUnits(expression, unit, "-100")

if __name__ == '__main__':
    main()
