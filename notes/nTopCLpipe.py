import os
import subprocess
import json
import sys

import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    #Assuming this script, ntop file, and json files will be in the same folder
    Current_Directory = os.path.dirname(os.path.realpath('__file__')) 
    exePath = r"C:/Program Files/nTopology/nTop Platform/nTopCL.exe"  #nTopCL path
    nTopFilePath = r"C:/Mallit/DI/nTop/dev/1-nTpCL/python/CB_smoothen_input_step.ntop"   #nTop notebook file name
    Input_File_Name = r"C:/Users/Public/Documents/ntopTest/input.json"      #JSON input file name to be saved as
    Output_File_Name = r"C:/Users/Public/Documents/ntopTest/out.json"       #JSON output file name to be saved as

    #Input variables in JSON structure
    Inputs_JSON = {
        "inputs": [
            {
                "name": "inputFileLocation",
                "type": "text",
                "value": sys.argv[1]           # example "C:\\Mallit\\DI\\nTop\\dev\\1-nTpCL\\mySolid_from_NX_9.stp"
            },
            {
                "name": "outputFileDestination",
                "type": "text",
                "value": sys.argv[2]           # example "C:\\Mallit\\DI\\nTop\\dev\\1-nTpCL\\smoothen\\mySolid_from_nTop_9.stp"
            }
        ]
    }

    #nTopCL arguments in a list
    Arguments = [exePath]               #nTopCL path
    Arguments.append("-u")
    Arguments.append("license@email.com")
    Arguments.append("-w")
    Arguments.append("password")
    Arguments.append("-j")              #json input argument
    Arguments.append(Input_File_Name)   #json path
    Arguments.append("-o")              #output argument
    Arguments.append(Output_File_Name)  #output json path
    Arguments.append(nTopFilePath)      #.ntop notebook file path

    #Creating in.json file
    with open(Input_File_Name, 'w') as outfile:
        json.dump(Inputs_JSON, outfile, indent=4)

    output,error = subprocess.Popen(Arguments,stdout = subprocess.PIPE, 
                stderr= subprocess.PIPE).communicate()

else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)