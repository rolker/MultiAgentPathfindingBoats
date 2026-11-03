from datetime import datetime
import tkinter as tk
from tkinter import *
import formulator
from tkinter.filedialog import askopenfilename
from pypdf import PdfWriter
import os

def readFromFileLabel():
    if selectReadFromFileVar.get():
        solveButton.config(text="Solve Problem From File")
    else:
        solveButton.config(text="Solve a Generated Problem")

def readTextFile():
    #reading settings from text file
    try:
        with open(textPathText.get(1.0, "end-1c")) as file:
            errorLabel.config(text="")
            for line in file:
                toLower = line.lower()
                split = toLower.split()
                if "numBoats" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"numBoats\" parameters in file")   
                        return
                    try:
                        numBoats = int(split[1])
                        errorLabel.config(text="")
                        boatsText.insert(tk.END, numBoats)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid number of boats")
                        return
                elif "numLines" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"numLines\" parameters in file")   
                        return
                    try:
                        numLines = int(split[1])
                        errorLabel.config(text="")
                        linesText.insert(tk.END, numLines)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid number of lines")
                        return
                elif "weights" in toLower:
                    if len(split) < 2:
                        errorLabel.config(text="Invalid number of \"weights\" parameters in file")   
                        return
                    for i in range(1, len(split)):
                        try:
                            weight = int(split[i])
                            errorLabel.config(text="")
                            weightText.insert(tk.END, weight)
                        except ValueError:
                            errorLabel.config(text=f"{split[i]} is not a valid weight")
                            return
                elif "survey" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"survey\" parameters in file")   
                        return
                    try:
                        survey = int(split[1])
                        errorLabel.config(text="")
                        surveyText.insert(tk.END, survey)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid survey speed")
                        return
                elif "transit" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"transit\" parameters in file")   
                        return
                    try:
                        transit = int(split[1])
                        errorLabel.config(text="")
                        transitText.insert(tk.END, transit)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid transit speed")
                        return
                elif "radius" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"radius\" parameters in file")   
                        return
                    try:
                        radius = int(split[1])
                        errorLabel.config(text="")
                        radiusText.insert(tk.END, radius)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid radius")
                        return
                elif "generation" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"generation\" parameters in file")   
                        return
                    try:
                        generationType = int(split[1])
                        errorLabel.config(text="")
                        generationText.insert(tk.END, generationType)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid generation type")
                        return
                elif "steps" in toLower:
                    if len(split) != 2:
                        errorLabel.config(text="Invalid number of \"steps\" parameters in file")   
                        return
                    try:
                        steps = int(split[1])
                        errorLabel.config(text="")
                        stepsText.insert(tk.END, steps)
                    except ValueError:
                        errorLabel.config(text=f"{split[1]} is not a valid number of steps")
                        return
    except FileNotFoundError as e:
        errorLabel.config(text=f"File {textPathText.get(1.0, "end-1c")} not found")   
        return


def selectFileName(text):
    text.delete("1.0", tk.END)
    text.insert(tk.END, askopenfilename())
    
def formulateProblem(): 
    #default settings
    numBoats = 1
    numLines = 0
    weights = [1]
    transitSpeeds = [1]
    surveySpeeds = [1]
    minimumRadii = [0]
    whatIfs = []
    generationType = 0
    numSteps = 0
    fileName = None
    writeToFileName = None

    # Error Checking For Inputs
    if (selectReadFromFileVar.get()):   
        fileName = filePathText.get(1.0, "end-1c")
         
    if (selectWriteToFileVar.get()):   
        writeToFileName = writePathText.get(1.0, "end-1c")
    
    
    if (len(boatsText.get(1.0, "end-1c")) != 0):   
        try:
            numBoats = int(boatsText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{boatsText.get(1.0, "end-1c")} is not a valid number of boats")
            return
    else:
        errorLabel.config(text="Please enter a number of boats")   
        return
    

    if (len(linesText.get(1.0, "end-1c")) != 0):
        try:
            numLines = int(linesText.get(1.0, "end-1c"))
            errorLabel.config(text="")
        except ValueError:
            errorLabel.config(text=f"{linesText.get(1.0, "end-1c")} is not a valid number of lines")
            return    
    elif selectReadFromFileVar.get() != True:
        errorLabel.config(text=f"Please a number of lines")
        return    


    if (len(weightText.get(1.0, "end-1c")) != 0):
        weights = []
        strings = weightText.get(1.0, "end-1c").split(" ")
        for i, string in enumerate(strings):
            try:
                weights.append(float(string))
                errorLabel.config(text="")
            except ValueError:
                errorLabel.config(text=f"{string} is not a valid weight")
                return
        

    if (len(transitText.get(1.0, "end-1c")) != 0):
        transitSpeeds = []
        
        strings = transitText.get(1.0, "end-1c").split(" ")
        
        if len(strings) == 1:
            try:
                transitSpeed = float(strings[0])
                if transitSpeed <= 0:
                    errorLabel.config(text=f"{strings[0]} is not a valid transit speed")
                    return
                transitSpeeds.append(transitSpeed)
                transitSpeeds = transitSpeeds * numBoats
                errorLabel.config(text="")
            except ValueError:
                errorLabel.config(text=f"{strings[0]} is not a valid transit speed")
                return
            
        elif len(strings) != numBoats:
            errorLabel.config(text=f"Please enter one transit speed per boat")
            return

        else:
            for i, string in enumerate(strings):
                try:
                    transitSpeed = float(string)
                    if transitSpeed <= 0:
                        errorLabel.config(text=f"{string} is not a valid transit speed")
                        return
                    transitSpeeds.append(transitSpeed)
                    errorLabel.config(text="")
                except ValueError:
                    errorLabel.config(text=f"{string} is not a valid transit speed")
                    return
    else:
        transitSpeeds = [1] * numBoats

    if (len(surveyText.get(1.0, "end-1c")) != 0):
        surveySpeeds = []
                
        strings = surveyText.get(1.0, "end-1c").split(" ")

        if len(strings) == 1:
            try:
                surveySpeed = float(strings[0])
                if surveySpeed <= 0:
                    errorLabel.config(text=f"{strings[0]} is not a valid survey speed")
                    return
                surveySpeeds.append(surveySpeed)
                surveySpeeds = surveySpeeds * numBoats
                errorLabel.config(text="")
            except ValueError:
                errorLabel.config(text=f"{strings[0]} is not a valid survey speed")
                return
            
        elif len(strings) != numBoats:
            errorLabel.config(text=f"Please enter one survey speed per boat")
            return

        else:
            for i, string in enumerate(strings):
                try:
                    surveySpeed = float(string)
                    if surveySpeed <= 0:
                        errorLabel.config(text=f"{string} is not a valid survey speed")
                        return
                    surveySpeeds.append(surveySpeed)
                    errorLabel.config(text="")
                except ValueError:
                    errorLabel.config(text=f"{string} is not a valid survey speed")
                    return
    else:
        surveySpeeds = [1] * numBoats
    
    if (len(radiusText.get(1.0, "end-1c")) != 0):
        minimumRadii = []

        strings = radiusText.get(1.0, "end-1c").split(" ")

        if len(strings) == 1:
            try:
                minimumRadius = float(strings[0])
                if minimumRadius < 0:
                    errorLabel.config(text=f"{strings[0]} is not a valid radius")
                    return
                minimumRadii.append(minimumRadius)
                minimumRadii = minimumRadii * numBoats
                errorLabel.config(text="")
            except ValueError:
                errorLabel.config(text=f"{strings[0]} is not a valid radius")
                return
        
        elif len(strings) != numBoats:
            errorLabel.config(text=f"Please enter one minimum radius per boat")
            return

        else:
            for i, string in enumerate(strings):
                try:
                    minimumRadius = float(string)
                    if minimumRadius < 0:
                        errorLabel.config(text=f"{string} is not a valid radius")
                        return
                    minimumRadii.append(minimumRadius)
                    errorLabel.config(text="")
                except ValueError:
                    errorLabel.config(text=f"{string} is not a valid radius")
                    return
    else:
        minimumRadii = [0] * numBoats    

    if (len(whatIfText.get(1.0, "end-1c")) != 0):
        strings = whatIfText.get(1.0, "end-1c").split()
        if (len(strings)%3!=0):
            errorLabel.config(text="Please enter What Ifs in the correct format")
            return
        
        trio = []
        for i, string in enumerate(strings):
            try:
                val = int(string)
                errorLabel.config(text="")
                trio.append(val)
                if i % 3 == 2:
                    whatIfs.append(trio)
                    trio = []
            except ValueError:
                errorLabel.config(text=f"{string} is not a valid number")
                return    
        for tri in whatIfs:
            print(f"{tri[0]}, {tri[1]}, {tri[2]}")

    if (len(generationText.get(1.0, "end-1c")) != 0):   
        try:
            generationType = int(generationText.get(1.0, "end-1c"))
            errorLabel.config(text="")
            if generationType > 5 or generationType < 0:
                errorLabel.config(text=f"{generationText.get(1.0, "end-1c")} is not a valid generation type")
                return
        except ValueError:
            errorLabel.config(text=f"{generationText.get(1.0, "end-1c")} is not a valid generation type")
            return
    
    if (len(stepsText.get(1.0, "end-1c")) != 0):   
        try:
            numSteps = int(stepsText.get(1.0, "end-1c"))
            errorLabel.config(text="")
            if numSteps < 0:
                errorLabel.config(text=f"{stepsText.get(1.0, "end-1c")} is not a valid number of steps")
                return
        except ValueError:
            errorLabel.config(text=f"{stepsText.get(1.0, "end-1c")} is not a valid number of steps")
            return
            
    #array to be filled with file names of pdfs
    pdfs = []

    #sending problem to formulator
    # print(f"{len(minimumRadii)} MR, {len(surveySpeeds)} {len(transitSpeeds)}")
    outputs = formulator.formulate(fileName, numBoats, weights, surveySpeeds, transitSpeeds, numLines, toPDFVar.get(), whatIfs, generationType, writeToFileName, numSteps, 0, minimumRadii)

    #output format: [[status], [pdfFileName], [trueObjectiveValue], [solutionLines]]
    for i, output in enumerate(outputs):
        if (output[0][0] == 0):
            if (toPDFVar.get()):
                pdfs.append(output[1])
        elif (output[0][0] == 1):
            errorLabel.config(text=f"No solution found")  
        elif (output[0][0] == 2):
            errorLabel.config(text=f"{output[0][1]}") 

    
    if (toPDFVar.get()):
        merger = PdfWriter()
        for pdf in pdfs:
            merger.append(pdf)
            os.remove(pdf)

        whatIfStr = ""
        if len(whatIfs) > 0:
            whatIfStr = "WithWhatIfs"
        if len(fileName) < 0:
            finalPlotName = f"{fileName[:-4]}{numBoats}B{int(minimumRadii[0])}MR{whatIfStr}.pdf"
        else:
            finalPlotName = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "_finalPlot" + whatIfStr + ".pdf"
        merger.write(finalPlotName)
        merger.close()
        
    # for purposes of producing multiple solutions-----------------------------------------------------------------------------------------------------------------------
    # num = 0
    # while num < 4:
    #     outputs = formulator.formulate(fileName, numBoats, weights, surveySpeeds, transitSpeeds, numLines, toPDFVar.get(), whatIfs, generation, writeToFileName, numSteps, num)

    # #output format: [[status], [pdfFileName], [trueObjectiveValue], [solutionLines]]
    #     for i, output in enumerate(outputs):
    #         if (output[0][0] == 0):
    #             if (toPDFVar.get()):
    #                 pdfs.append(output[1])
    #         elif (output[0][0] == 1):
    #             errorLabel.config(text=f"No solution found")  
    #         elif (output[0][0] == 2):
    #             errorLabel.config(text=f"{output[0][1]}") 
            
    #     num += 1
        
    # if (toPDFVar.get()):
    #         merger = PdfWriter()
    #         for pdf in pdfs:
    #             merger.append(pdf)
    #             os.remove(pdf)

    #         if len(whatIfs) > 0:
    #             merger.write("finalPlotWithWhatIfs.pdf")
    #         else:   
    #             merger.write("finalPlot.pdf")
    #         merger.close()

    # for purposes of testing what ifs----------------------------------------------------------------------------------------------------------------------------
    # point1 = 0
    # point2 = 0
    # boat = 0
    # while numLines < 50:
    #     outputs = formulator.formulate(fileName, numBoats, weights, surveySpeeds, transitSpeeds, numLines, toPDFVar.get(), whatIfs, generation, writeToFileName, numSteps, 0)
    #     originalObjectiveValue = outputs[0][2]
    #     while boat < numBoats:
    #         while point1 < numLines * 2:
    #             while point2 < numLines * 2:
    #                 point1comp = point1 + 1 if point1 % 2 == 0 else point1 - 1
    #                 if point1 != point2 and point1comp != point2:
    #                     whatIfs = [[boat, point1, point2]]
    #                     outputs = formulator.formulate(fileName, numBoats, weights, surveySpeeds, transitSpeeds, numLines, toPDFVar.get(), whatIfs, generation, writeToFileName, numSteps, 0)

    #                     #output format: [[status], [pdfFileName], [trueObjectiveValue], [solutionLines]]
    #                     for i, output in enumerate(outputs):
    #                         if (output[0][0] == 0):
    #                             if (toPDFVar.get()):
    #                                 pdfs.append(output[1])
    #                             if output[2] < originalObjectiveValue:
    #                                 with open(f"foo.txt", "a") as f:
    #                                     f.write(f"Better solution found with what if: Boat {boat}, Point {point1}, Point {point2}, numBoats {boats}, numLines {numLines}: ORIGINAL {originalObjectiveValue} OJECTIVE VAL: {output[2]}\n")
    #                         elif (output[0][0] == 1):
    #                             errorLabel.config(text=f"No solution found")  
    #                             with open(f"foo.txt", "a") as f:
    #                                 f.write(f"No solution found for what if: Boat {boat}, Point {point1}, Point {point2}, numBoats {boats}, numLines {numLines}\n")
    #                         elif (output[0][0] == 2):
    #                             errorLabel.config(text=f"{output[0][1]}") 
    #                 point2 += 1
    #             point2 = 0
    #             point1 += 1
    #         point1 = 0
    #         boat += 1
    #     boat = 0
    #     numLines += 1       
    #     whatIfs = []
            

    # # for purposes of producing scaling plots-------------------------------------------------------------------------------------------------------------------------
    # timeLimits = [10, 20, 60]
    # for timeLimit in timeLimits:
    #     with open(f"foo.txt", "a") as f:
    #         f.write(f"{timeLimit} SECOND TIME LIMIT\n")
       
    #     while numBoats < 6:
    #         with open(f"foo.txt", "a") as f:
    #             f.write(f"{numBoats} boats!\n")
    #         while numLines < 101:
    #             outputs = formulator.formulate(fileName, numBoats, weights, surveySpeeds*numBoats, transitSpeeds*numBoats, numLines, toPDFVar.get(), whatIfs, generationType, writeToFileName, numSteps, 0, minimumRadii*numBoats, timeLimit=timeLimit)

    #             #output format: [[status], [pdfFileName], [trueObjectiveValue], [solutionLines]]
    #             for i, output in enumerate(outputs):
    #                 if (output[0][0] == 0):
    #                     if (toPDFVar.get()):
    #                         pdfs.append(output[1])
    #                 elif (output[0][0] == 1):
    #                     errorLabel.config(text=f"No solution found")  
    #                 elif (output[0][0] == 2):
    #                     errorLabel.config(text=f"{output[0][1]}") 
                
    #             numLines += 1
    #         numBoats += 1
    #         numLines = numBoats
    #     numBoats = 1
    #     numLines = 1

    # # for purposes of producing file plots-------------------------------------------------------------------------------------------------------------------------
    # while numBoats < 6:
    #     print(f"{len(minimumRadii)} MR, {len(surveySpeeds)} {len(transitSpeeds)}")
    #     outputs = formulator.formulate(fileName, numBoats, weights, surveySpeeds*numBoats, transitSpeeds*numBoats, numLines, toPDFVar.get(), whatIfs, generationType, writeToFileName, numSteps, 0, minimumRadii*numBoats)

    #     #output format: [[status], [pdfFileName], [trueObjectiveValue], [solutionLines]]
    #     for i, output in enumerate(outputs):
    #         if (output[0][0] == 0):
    #             if (toPDFVar.get()):
    #                 pdfs.append(output[1])
    #         elif (output[0][0] == 1):
    #             errorLabel.config(text=f"No solution found")  
    #         elif (output[0][0] == 2):
    #             errorLabel.config(text=f"{output[0][1]}") 

    #     if (toPDFVar.get()):
    #         merger = PdfWriter()
    #         for pdf in pdfs:
    #             merger.append(pdf)
    #             os.remove(pdf)
    
    #         if len(whatIfs) > 0:
    #             merger.write("finalPlotWithWhatIfs.pdf")
    #         else:   
    #             merger.write(f"{fileName[:-4]}{numBoats}B{int(minimumRadii[0])}MR.pdf")
    #         merger.close()
    #     pdfs = []
    #     numBoats += 1


    # for purposes of testing examples-------------------------------------------------------------------------------------------------------------------------
    # timeLimits = [10, 20, 60]
    # for timeLimit in timeLimits:
    #     with open(f"foo.txt", "a") as f:
    #         f.write(f"{timeLimit} SECOND TIME LIMIT\n")
    #     for i in range(1,6):
    #         with open(f"foo.txt", "a") as f:
    #             f.write(f"{i} boats!\n")
    #         numBoats = i
    #         with open("fileNames.txt", "r", encoding="utf-8") as file:
    #             for exampleName in file:
    #                 outputs = formulator.formulate(exampleName.strip(), numBoats, weights, surveySpeeds*numBoats, transitSpeeds*numBoats, numLines, toPDFVar.get(), whatIfs, generationType, writeToFileName, numSteps, 0, minimumRadii*numBoats, timeLimit=timeLimit)

    #                 #output format: [[status], [pdfFileName], [trueObjectiveValue], [solutionLines]]
    #                 for i, output in enumerate(outputs):
    #                     if (output[0][0] == 0):
    #                         if (toPDFVar.get()):
    #                             pdfs.append(output[1])
    #                     elif (output[0][0] == 1):
    #                         errorLabel.config(text=f"No solution found")  
    #                     elif (output[0][0] == 2):
    #                         errorLabel.config(text=f"{output[0][1]}") 

    #                 if (toPDFVar.get()):
    #                     merger = PdfWriter()
    #                     for pdf in pdfs:
    #                         merger.append(pdf)
    #                         os.remove(pdf)
                
    #                     if len(whatIfs) > 0:
    #                         merger.write("finalPlotWithWhatIfs.pdf")
    #                     else:   
    #                         merger.write(f"{exampleName[:-4]}{numBoats}B{int(minimumRadii[0])}MR.pdf")
    #                     merger.close()
    #                 pdfs = []
        

    
    return
        

# UI Setup
root = Tk()
root.title("Ducklings")
root.geometry('800x400')

row = 0

filePathLabel = tk.Label(root, text="Enter path of CSV File with Coordinates")
filePathLabel.grid(row=row, column=0, sticky=E, padx=10)

filePathText = tk.Text(master=root, height=1, width=30, )
filePathText.grid(row=row, column=1, sticky=W)

row+=1

filePathButton = tk.Button(root, text="Or upload file", command=lambda: selectFileName(filePathText))
filePathButton.grid(row=row, column=0, sticky=E, padx=10)

selectReadFromFileVar = tk.BooleanVar()
selectReadFromFileVar.set(False)

selectReadFromFile = tk.Checkbutton(
    root,
    text="Read from File",
    variable=selectReadFromFileVar,
    command=readFromFileLabel
)
selectReadFromFile.grid(row=row, column=1, sticky=W)

row+=1

writePathLabel = tk.Label(root, text="Enter path of CSV File to write coordinates")
writePathLabel.grid(row=row, column=0, sticky=E, padx=10)

writePathText = tk.Text(master=root, height=1, width=30, )
writePathText.grid(row=row, column=1, sticky=W)

row+=1

writePathButton = tk.Button(root, text="Or upload file", command=lambda: selectFileName(writePathText))
writePathButton.grid(row=row, column=0, sticky=E, padx=10)

selectWriteToFileVar = tk.BooleanVar()
selectWriteToFileVar.set(False)

selectWriteToFile = tk.Checkbutton(
    root,
    text="Write to File",
    variable=selectWriteToFileVar,
    command=writePathLabel
)
selectWriteToFile.grid(row=row, column=1, sticky=W)

row+=1

textPathLabel = tk.Label(root, text="Enter path of Text File with settings to formulate")
textPathLabel.grid(row=row, column=0, sticky=E, padx=10)

textPathText = tk.Text(master=root, height=1, width=30, )
textPathText.grid(row=row, column=1, sticky=W)

row+=1

textPathButton = tk.Button(root, text="Or upload file", command=lambda: selectFileName(textPathText))
textPathButton.grid(row=row, column=0, sticky=E, padx=10)

textReadButton = tk.Button(root, text="Load Settings", command=lambda: readTextFile())
textReadButton.grid(row=row, column=1, sticky=W)

row+=1

boatsLabel = tk.Label(master=root, text="Enter number of boats:")
boatsLabel.grid(row=row, column=0, sticky=E, padx=10)

boatsText = tk.Text(master=root, height=1, width=30, )
boatsText.grid(row=row, column=1, sticky=W)

row+=1

linesLabel = tk.Label(root, text="Enter Number of Lines to Formulate")
linesLabel.grid(row=row, column=0, sticky=E, padx=10)

linesText = tk.Text(master=root, height=1, width=30, )
linesText.grid(row=row, column=1, sticky=W)

row+=1

weightLabel = tk.Label(root, text="Enter Objective Weight(s) to solve with (default: 1)")
weightLabel.grid(row=row, column=0, sticky=E, padx=10)

weightText = tk.Text(master=root, height=1, width=30, )
weightText.grid(row=row, column=1, sticky=W)

row+=1

surveyLabel = tk.Label(root, text="Enter Survey Speed (default: 1)")
surveyLabel.grid(row=row, column=0, sticky=E, padx=10)

surveyText = tk.Text(master=root, height=1, width=30, )
surveyText.grid(row=row, column=1, sticky=W)

row+=1

transitLabel = tk.Label(root, text="Enter Transit Speed (default: 1)")
transitLabel.grid(row=row, column=0, sticky=E, padx=10)

transitText = tk.Text(master=root, height=1, width=30, )
transitText.grid(row=row, column=1, sticky=W)

row+=1

radiusLabel = tk.Label(root, text="Enter Boat's Minimum Turning Radius for Dubin's (default: None)")
radiusLabel.grid(row=row, column=0, sticky=E, padx=10)

radiusText = tk.Text(master=root, height=1, width=30, )
radiusText.grid(row=row, column=1, sticky=W)

row+=1


whatIfLabel = tk.Label(root, text="Enter \"What-If\" line (\"boatnumber startpoint endpoint\") (default: None)")
whatIfLabel.grid(row=row, column=0, sticky=E, padx=10)

whatIfText = tk.Text(master=root, height=1, width=30, )
whatIfText.grid(row=row, column=1, sticky=W)

row+=1

generationLabel = tk.Label(root, text="Enter line generation type (0 = column, 1 = random, 2 = BC, 3 = SC, 4 = BSC) (default: 0)")
generationLabel.grid(row=row, column=0, sticky=E, padx=10)

generationText = tk.Text(master=root, height=1, width=30, )
generationText.grid(row=row, column=1, sticky=W)

row+=1

stepsLabel = tk.Label(root, text="Enter number of steps to step through solution (default: None)")
stepsLabel.grid(row=row, column=0, sticky=E, padx=10)

stepsText = tk.Text(master=root, height=1, width=30, )
stepsText.grid(row=row, column=1, sticky=W)

row+=1

errorLabel = tk.Label(root, text="")
errorLabel.grid(row=row, column=1, sticky=W)

row+=1

toPDFVar = tk.BooleanVar()
toPDFVar.set(False)

toPDFButton = tk.Checkbutton(
    root,
    text="Print to PDF",
    variable=toPDFVar,
)
toPDFButton.grid(row=row, column=0, sticky=E, padx=10)

solveButton = tk.Button(root, text="Solve a Generated Problem", command=lambda: formulateProblem())
solveButton.grid(row=row, column=1, sticky=W)

root.mainloop()