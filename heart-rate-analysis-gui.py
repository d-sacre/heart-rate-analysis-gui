import tkinter as tk
from tkinter import filedialog
import os
import sys

# source: https://stackoverflow.com/questions/739993/how-do-i-get-a-list-of-locally-installed-python-modules
import pkg_resources
installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}


import modules.complete_processing_module as cpm

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # required to automatically end Python process after Tkinter GUI was closed
        # source: https://stackoverflow.com/questions/55201199/the-python-program-is-not-ending-when-tkinter-window-is-closed
        master.protocol("WM_DELETE_WINDOW", self.quit_me) 
        self.pack()

        self.requiredPythonVersion = (3,10,0)
        self.required_standardPackages = ['pkg_resources','tkinter','os','sys','datetime','csv','json']
        self.required_nonStandardPackages = ['scipy','numpy','matplotlib']
        self.generalLogWarningsAndErrors = {"fatal": "\n\n=> A FATAL ERROR occured; no data/plots were exported!"}

        self.import_filepath = ""
        self.export_directory= ""
        self.logText = ""

        self.file_pathGUI = tk.StringVar()
        self.folder_pathGUI = tk.StringVar()

        _row=0
        self.filepathDescriptionLabel, self.filepathEntry, self.importFilepathButton, _row = self.descriptionEntryFieldButtonTemplate(_row,"1) Open the heart rate raw data file at location ...",self.file_pathGUI,'Open',self.openFiledialog)

        _row+=1
        self.exportPathDescriptionLabel, self.exportPathEntry, self.importFilepathButton, _row = self.descriptionEntryFieldButtonTemplate(_row, "2) Select the export directory ...",self.folder_pathGUI,'Select',self.openFolderdialog)

        _row+=1
        self.exportPathWarningLabel = tk.Label(self,text="Warning: Already existing heart rate analysis data in the specified export directory will be overwriten!",font = "Default 7").grid(row=_row,column=0,columnspan=2,sticky="w",padx=10)

        _row+=1
        self.analysisButton = tk.Button(self, text='Run Analysis', width=25, command=self.runAnalysis).grid(row=_row,column=0, pady=10)
        self.exitButton = tk.Button(self, text='Quit', width=25, command=self.quit_me).grid(row=_row,column=1, pady=10)

        _row+=1
        self.logLabel = tk.Label(self, text="Program Log",font = "Default 10 bold").grid(row=_row,column=0, columnspan=2,sticky="w",padx=10)

        _row+=1
        self.logTextGUI = tk.StringVar()
        self.logTextLabel = tk.Label(self, width = 75, height=15,textvariable=self.logTextGUI, anchor="nw", justify=tk.LEFT).grid(row = _row, column = 0, columnspan = 2, padx=10)



    # Templates
    def descriptionEntryFieldButtonTemplate(self,row,labelText,entryFieldTextvar,buttonText,buttonFunction):
        _label = tk.Label(self,text=labelText,font = "Default 10 bold").grid(row=row,column=0,columnspan=2,sticky="w",padx=10)

        row+=1
        _entryField = tk.Entry(self, width=75,textvariable=entryFieldTextvar,state='disabled').grid(row=row,column=0,columnspan=2,ipady=4,padx=10)
        _button = tk.Button(self, text=buttonText, width=6, command=buttonFunction).grid(row=row,column=2)

        return _label, _entryField, _button, row

    # function to automatically end Python process after Tkinter GUI is closed
    def quit_me(self):
        self.master.quit()
        self.master.destroy()
    
    def openFiledialog(self):
        root = tk.Tk()
        root.withdraw()
        self.import_filepath = filedialog.askopenfilename(title = "Select the heart rate data file ...",filetypes = (("CSV Files","*.csv"),))
        self.file_pathGUI.set(self.import_filepath)
        
    def openFolderdialog(self):
        root = tk.Tk()
        root.withdraw()
        self.export_directory = filedialog.askdirectory(title = "Select the export directory ...")
        self.folder_pathGUI.set(self.export_directory)

    def updateProgramLogGUI(self,old,add,log):
        _update = old + add
        log.set(_update)

        return _update

    def runAnalysis(self):
        self.logText = self.updateProgramLogGUI(self.logText,"Starting Analysis Routine ...",self.logTextGUI)
        self.logText = self.updateProgramLogGUI(self.logText,"\n\t(1) Verification Phase ...",self.logTextGUI)
        self.logText = self.updateProgramLogGUI(self.logText,"\n\t\t-> Python Version ... ",self.logTextGUI)

        # Check for Python version
        if sys.version_info >= self.requiredPythonVersion: 
            self.logText = self.updateProgramLogGUI(self.logText,"OK",self.logTextGUI)
            self.logText = self.updateProgramLogGUI(self.logText,"\n\t\t-> Required Non-Standard Python Modules ... ",self.logTextGUI)

            # Check whether all the required modules are installed
            _lenRequiredModules = len(self.required_nonStandardPackages)
            _verifiedModules = []
            _missingModules = []

            for key in self.required_nonStandardPackages:
                if key in installed_packages:
                    _verifiedModules.append(key)
                    # _missingModules.append(key) # debug only
                else:
                    _missingModules.append(key)
            
            if _lenRequiredModules == len(_verifiedModules):
                self.logText = self.updateProgramLogGUI(self.logText,"OK",self.logTextGUI)
                cpm.dataProcessingExportingAndPlotting(self.import_filepath,self.export_directory+"/")
            else:
                self.logText = self.updateProgramLogGUI(self.logText,"FATAL ERROR",self.logTextGUI)
                _errorString = "FATAL ERROR: Not all the required Python modules are installed on the system."
                _errorString += "\n\t          The following modules are missing:"

                for element in _missingModules:
                    _errorString += "\n\t\t" + element

                _errorString += "\n\t          To prevent any problems, the analysis was aborted."
                _errorString += self.generalLogWarningsAndErrors["fatal"]
                self.logText = self.updateProgramLogGUI(self.logText,"\n\n"+_errorString,self.logTextGUI)
        else:
            self.logText = self.updateProgramLogGUI(self.logText,"FATAL ERROR",self.logTextGUI)
            _errorString = "FATAL ERROR: The detected Python installation is version " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "."
            _errorString += "\n\t          This program requires Python " + str(self.requiredPythonVersion[0]) + "." + str(self.requiredPythonVersion[1])+ " or higher to function properly."
            _errorString += "\n\t          To prevent any problems, the analysis was aborted."
            _errorString += self.generalLogWarningsAndErrors["fatal"]
            self.logText = self.updateProgramLogGUI(self.logText,"\n\n"+_errorString,self.logTextGUI)   

root = tk.Tk()
myapp = App(root)
# here are method calls to the window manager class
#
myapp.master.title("Heart Rate Analysis GUI (alpha-2022-07-21)")
myapp.master.iconphoto(False, tk.PhotoImage(file='./img/heart-rate-analysis_icon.png'))
myapp.master.minsize(640, 480)
myapp.master.maxsize(640, 480)
# myapp.master.maxsize(1920, 1080)

myapp.mainloop()

