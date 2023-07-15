
import tkinter as tk
from tkinter import *
import subprocess, os, sys
from PIL import Image, ImageTk
import startCalling


#Global variables
global devices,device,bundle_dir
devices         =   []

class UI(Frame):
    def __init__(self):
        #super().__init__()
        self.initUI()

    def initUI(self):
        wiproImgURL = bundle_dir+r"\data\imgsrc\swipro.jpg"
        #callLogoURL = path+'\\data\imgsrc\\scall.jpg' C:\Users\Chait\OneDrive\WorkSpace\_Phython\data\imgsrc\scall.jpg
        callLogoURL = bundle_dir+r"\data\imgsrc\scall.jpg"

        #updateDeviceList funciton has to be before btgetUEList as this is used as command to it
        def updateDeviceList():
            getDeviceList()

            deviceList = OptionMenu(mainWindow,variable, *devices, command=self.devSelect)
            deviceList.grid(row=2,column=1,columnspan=3,sticky="NSEW")


        #Tk(screenName=None,  baseName=None,  className=’Tk’,  useTk=1): To create a main window, tkinter offers a method ‘Tk(screenName=None,  baseName=None,  className=’Tk’,  useTk=1)’.
        mainWindow = tk.Tk()
        #Change title
        mainWindow.title("MO Calls")
        mainWindow.iconbitmap(bundle_dir+r'\data\imgsrc\cblue.ico')

        mainWindow.geometry("720x280+150+150") # size of the window width x height + starting column + starting row
        mainWindow.resizable(0, 0) # this prevents from resizing the window


        #Wipro and Call image display
        wiproImgCanvas = Canvas(width = 100, height = 90)
        wiproPhtoImg = ImageTk.PhotoImage(Image.open(wiproImgURL))
        wiproImgCanvas.create_image(0, 0, anchor=NW, image=wiproPhtoImg)

        labelMOCalls = tk.Label(text    ='MO CALLS',
                                anchor  ='center',
                                font    =("Forte", 55, "bold",'underline',"roman"),
                                fg      ="#0087D7")

        callImgCanvas   = Canvas(width = 100, height = 90)
        callPhtoImg = ImageTk.PhotoImage(Image.open(callLogoURL))
        callImgCanvas.create_image(0, 0, anchor=NW, image=callPhtoImg)

        #Label to display "Device"
        labelDevice = tk.Label(text='Select a Device', anchor= 'w')

        #Below is a list view to display connected device list. variable from above is used to display default/selected option.
        #a temporary variable to store default value in StringVar
        variable = StringVar()
        variable.set(device) # default value
        deviceList = OptionMenu(mainWindow,variable, *devices, command=self.devSelect)

        btgetUEList     =   tk.Button(text="Get UE List", fg="#870000",activebackground = "gray", command=updateDeviceList)

        lbNumber        =   tk.Label(text="Number:", anchor= 'w')
        etNumber        =   tk.Entry(mainWindow)
        lbNumCalls      =   tk.Label(text="No. of Calls:", anchor= 'w')
        etNumCalls      =   tk.Entry(mainWindow)
        lbCallDuration  =   tk.Label(text="Call Duration(in secconds):",anchor="w")
        etCallDuration  =   tk.Entry(mainWindow)
        btStartCalls    =   tk.Button(text="Start Calls", fg="#000087",activebackground = "gray", command= lambda:self.startCalls(etNumber.get(),etNumCalls.get(),etCallDuration.get()))

        mainWindow.columnconfigure(2,weight=1)

        wiproImgCanvas.grid(row=0,column=0)
        labelMOCalls.grid(row=0,column=1,columnspan=3)
        callImgCanvas.grid(row=0,column=5)
        labelDevice.grid(row=2,sticky="NSEW")
        deviceList.grid(row=2,column=1,columnspan=3,sticky="NSEW") # this grid is again used in updateDeviceList. If changed here, also change there
        btgetUEList.grid(row=2,column=5, sticky =(E), padx=10)

        lbNumber.grid(row=3, sticky = "NSEW",pady=5)
        etNumber.grid(row=3,column=1, sticky = "NSEW",pady=5)
        etNumber.insert(-1,"0297789199")

        lbNumCalls.grid(row=4, sticky = (W),pady=5)
        etNumCalls.grid(row=4,column=1, sticky = "NSEW",pady=5)
        etNumCalls.insert(-1,"2")

        lbCallDuration.grid(row=5,sticky="w",pady=5)
        etCallDuration.grid(row=5,column=1,sticky="W",pady=5)
        etCallDuration.insert(-1,"20")

        btStartCalls.grid(row=6,columnspan=2,pady=5)

        mainWindow.mainloop() #Used to run application in loop, wait for an event to occur and process the event till the window is not closed.

    #startCalls funciton has to be before btStartCalls as this is used as command to it
    def startCalls(self,phoneNumber,noCalls,callTime):
        #print("In Start calls")
        startCalling.calls(phoneNumber,int(noCalls),self.selectedDeviceCode,bundle_dir,int(callTime))

    #This function is called wh+en an option is selected from device list dropdown menu.
    def devSelect(self, e):
        self.selectedDeviceCode = e[:e.find(" ")]
        #print("Selected device is:",self.selectedDeviceCode)


def getDeviceList():
    global devices, device
    devices.clear()
    command = bundle_dir+r'\data\devices -l'
    procVar = subprocess.Popen(command, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #deviceCodeList.append(tmpStr[:tmpStr.find(" ")])

    devices.append("Click and select") #Only when device is selected from list, device code is stored in global variable "selectedDeviceCode"
    while True:
        lineSTDOUT = procVar.stdout.readline()
        lineSTDERR = procVar.stderr.readline()
        if not lineSTDOUT and not lineSTDERR:
            break
        #the real code does filtering here
        #print("out:",lineSTDOUT.rstrip())
        #print("--err:",lineSTDERR.rstrip())
        tmpStr = lineSTDOUT.rstrip().decode("utf-8")
        #print(tmpStr)
        if "device " in tmpStr:
            devices.append(tmpStr)
            #deviceCodeList.append(tmpStr[:tmpStr.find(" ")])

    if len(devices) == 0:
        devices = ["No device is connected"]

    device = devices[0]

#Start if this is main file
if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    getDeviceList()
    uiObj = UI()
