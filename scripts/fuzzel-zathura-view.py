#!/usr/bin/python3
from fuzzel import fuzzel
from utils import generate_short_title, MAX_LEN
import os
import subprocess


def select_pdf(dir = os.getcwd()):
    # List all files in current working directory that can be viewed using zathura pdf viewer (i.e. .pdf files)
    # List names of pdf files in working directory 
    pdflist = []
    subdirlist = []
    dirEntries = os.scandir(dir)
    for entry in dirEntries:
        if entry.is_file() and entry.name.endswith(".pdf"):
            pdflist.append(entry.name)                
        elif entry.is_dir():
            subdirlist.append(entry.name)
        #else:
            #donothing
    # sort by files in current directory first, then subdirectories
    # add fixed length string to start of entries, either a file indicator or a directory icon
    prefixLength = 4
    pdfIconList = [ str(" - " + p) for p in pdflist]
    dirIconList = [ str(" - " + d) for d in subdirlist ]
    options = pdfIconList + dirIconList
         
    key, index, selected = fuzzel('Select PDF:', options, [
        '--lines', 5, 
    ])
    # Recurse if selection is a directory, otherwise return the selection with its file extension added back in 
    # Initialise return string
    pdfSelection = ""
    if len(selected) > prefixLength:
        selected = selected[prefixLength:] # remove icon string
        if selected in subdirlist:
            subdirPath = dir+"/"+selected 
            pdfSelection = select_pdf(dir=subdirPath)
        else:
            pdfSelection = str(dir+"/"+selected)
        return pdfSelection
    return "Invalid Selection"

def view_pdf(selection):
    # Open file in new viewer window
    print(selection + " is the selected file")
    if os.path.isfile(str(selection)):
        print(selection + " is the selected file")
        result = subprocess.run(
            ['zathura', str(selection)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=str(os.getcwd())
        )
    else: 
        print("oh no!")
        return "File not found"
    return result.returncode

if __name__ == "__main__":
    selected_pdf = select_pdf()
    view_pdf(selected_pdf)
