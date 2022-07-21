import tkinter as tk
from tkinter import filedialog
import os

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # required to automatically end Python process after Tkinter GUI was closed
        # source: https://stackoverflow.com/questions/55201199/the-python-program-is-not-ending-when-tkinter-window-is-closed
        master.protocol("WM_DELETE_WINDOW", self.quit_me) 
        self.pack()

        self.import_filepath = ""
        self.export_directory= ""

        self.file_pathGUI = tk.StringVar()
        self.folder_pathGUI = tk.StringVar()

        _row=0
        self.filepathDescriptionLabel = tk.Label(self,text="1) Open the heart rate raw data file at location ...",font = "Default 10 bold").grid(row=_row,column=0,columnspan=2,sticky="w",padx=10)

        _row+=1
        self.filepathEntry = tk.Entry(self, width=75).grid(row=_row,column=0,columnspan=2,ipady=4,padx=10)
        self.importFilepathButton = tk.Button(self, text='Open', width=6, command=self.openFiledialog).grid(row=_row,column=2)

        _row+=1
        self.filepathDescriptionLabel = tk.Label(self,text="2) Select the export directory ...",font = "Default 10 bold").grid(row=_row,column=0,columnspan=2,sticky="w",padx=10)

        _row+=1
        self.exportPathEntry = tk.Entry(self, width=75).grid(row=_row,column=0,columnspan=2,ipady=4,padx=10)
        self.importFilepathButton = tk.Button(self, text='Select', width=6, command=self.openFolderdialog).grid(row=_row,column=2)

        _row+=1
        self.filepathDescriptionLabel = tk.Label(self,text="Warning: Already existing heart rate analysis data in the specified export directory will be overwriten!",font = "Default 7").grid(row=_row,column=0,columnspan=2,sticky="w",padx=10)

        _row+=1
        self.analysisButton = tk.Button(self, text='Run Analysis', width=25, command=self.runAnalysis).grid(row=_row,column=0, pady=10)
        self.exitButton = tk.Button(self, text='Quit', width=25, command=self.quit_me).grid(row=_row,column=1, pady=10)



    # function to automatically end Python process after Tkinter GUI is closed
    def quit_me(self):
        self.master.quit()
        self.master.destroy()
    
    def openFiledialog(self):
        root = tk.Tk()
        root.withdraw()
        self.import_filepath = filedialog.askopenfilename()
        self.file_pathGUI.set(self.import_filepath)
        
    def openFolderdialog(self):
        root = tk.Tk()
        root.withdraw()
        self.export_directory = filedialog.askdirectory()
        self.folder_pathGUI.set(self.export_directory)

    def runAnalysis(self):
        pass
        # Does not work due to issues of loading modules from subfolder
        # _commandString = "python /home/mane/github/d-sacre/heart-rate-analysis/heart-rate-analysis-cli/heart-rate-analysis-cli.py -i " 
        # _commandString += self.import_filepath + " -o " + self.export_directory
        # os.system(_commandString)


        # print(self.import_filepath, self.export_directory)
        

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

