import os
import subprocess
import json
import sys
from pathlib import Path
import ctypes, sys
import ENVIRONMENT

BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
UNDERLINE = '\033[4m'
RESET = '\033[0m'

class TopologyCaller:

    def __init__(self):
        pass
    # Makes a subprocess for nTopCL -command with parameters being:
    # Param 1: Path to .stp -file lubrication oil channels
    # Param 2: Path where nTopology output .x_t -file will be saved 
    def subProcessRockerArm(self, inputStepLOchannel, outputParasolid, inputfileJSON, outputfileJSON):
        os.system("")
        #Assuming this script, ntop file, and json files will be in the same folder
        Current_Directory = os.path.dirname(os.path.realpath('__file__')) 
        exePath = "C:\\Program Files\\nTopology\\nTop Platform\\nTopCL.exe"  #nTopCL path
        nTopFilePath = ENVIRONMENT.PATH_CB   #nTop notebook file name
        #nTopFilePath = "nTopCL"
        #Input_File_Name = r"C:/SoftwareDevelopment/python/Multithreading-1/input.json"      #JSON input file name to be saved as
        print("INPUTS",

            inputStepLOchannel, inputStepLOchannel[0], "\n",
            outputParasolid, outputParasolid[0], "\n",
            inputfileJSON, inputfileJSON[0], "\n",
            outputParasolid, outputParasolid[0], "\n")
        Input_File_Name = str(Path(inputfileJSON[0]))
        #Output_File_Name = r"C:/SoftwareDevelopment/python/Multithreading-1/out.json"       #JSON output file name to be saved as
        Output_File_Name = str(Path(outputfileJSON))

        Inputs_JSON = {
            "inputs": [
                {
                    "name": "SOLID_LO_Channels_PATH", "type": "text", "value": str(Path(inputStepLOchannel[0]))}, {
                    "name": "SOLID_design_space_enclosed_PATH", "type": "text", "value": str(Path("C:/SoftwareDevelopment/python/Multithreading-1/container/DS-cutoff-cylinder2.stp"))}, {
                    "name": "SOLID_PR_bushing_enclosed_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/SOLID/SOLID_PR_bushing_enclosed.stp"))}, {
                    "name": "SOLID_pin_bushing_enclosed_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/SOLID/SOLID_pin_bushing_enclosed.stp"))}, {
                    "name": "SOLID_V_bushing_enclosed_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/SOLID/SOLID_V_bushing_enclosed.stp"))}, {
                    "name": "SOLID_V_hole_inverse_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/SOLID/SOLID_V_hole_inverse.stp"))}, {
                    "name": "SOLID_PR_hole_inverse_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/SOLID/SOLID_PR_hole_inverse.stp"))}, {
                    "name": "SOLID_pin_hole_inverse_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/SOLID/SOLID_pin_hole_inverse.stp"))}, {
                    "name": "FACE_PR_xy_top_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_PR_xy_top.stp"))}, {
                    "name": "FACE_PR_xy_bottom_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_PR_xy_bottom.stp"))}, {
                    "name": "FACE_PR_hole_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_PR_hole_3.stp"))}, {
                    "name": "FACE_V_xy_top_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_LO_xy_top.stp"))}, {
                    "name": "FACE_V_xy_bottom_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_LO_xy_bottom.stp"))}, {
                    "name": "FACE_V_hole_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_LO_hole_3.stp"))}, {
                    "name": "FACE_pin_hole_PATH", "type": "text", "value": str(Path("C:/Mallit/DI/nTop/miscShit/Input/FACE/FACE_pin_hole_3.stp"))}, {
                    "name": "EXPORT_PATH_ParaSolid", "type": "text", "value": str(Path(outputParasolid[0]))}
            ]
        }

        #nTopCL arguments in a list
        Arguments = [exePath]               #nTopCL path
        #Arguments.append(pythonPath[0])
        Arguments.append("-u")
        Arguments.append(ENVIRONMENT.USER)
        Arguments.append("-w")
        Arguments.append(ENVIRONMENT.PW)
        Arguments.append("-j")              #json input argument
        Arguments.append(Input_File_Name)   #json path
        Arguments.append("-o")              #output argument
        Arguments.append(Output_File_Name)  #output json path
        Arguments.append(nTopFilePath)      #.ntop notebook file path

        #Creating in.json file
        print('{YELLOW}{inputfileJSON}{RESET}'.format(YELLOW=YELLOW, inputfileJSON=inputfileJSON, RESET=RESET))
        print("JEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESUS", inputfileJSON[0])

        with open(Input_File_Name, 'w') as outfile:
            json.dump(Inputs_JSON, outfile, indent=4)

        print('ARGUMENTS BEFORE SP CALL', Arguments)

        sp = subprocess.Popen(Arguments, shell=True ,stdout = subprocess.PIPE, stderr= subprocess.PIPE)
        sp.wait()
        output, error = sp.communicate()

        print(f'{YELLOW} {output} {RESET}')

        if (error != ""):
            print('{s}ERROR in subprocess! - {e} {end}'.
                format(s=RED, e=error, end=RESET))
            print(error)
