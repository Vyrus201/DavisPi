# Import the required libraries
from tkinter import *
from tkinter.ttk import *

from ttkbootstrap import DateEntry
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import ImageTk, Image
import datetime
import json
import os
import serialcompi
from cryptography.fernet import Fernet
from ftplib import FTP
from threading import Thread
from FTPConnect import SendFTP

# Create Class Instances
GetCurData = serialcompi.SerData()

# Sync Time
GetCurData.updateTime()

# Get current directory
workingdir = os.getcwd()

# Get current user home directory
home_directory = os.path.expanduser( '~' )

class GUI:
    def __init__(self):

        # Destroy splashscreen
        try:
            splash_root.destroy()
        except:
            pass

        # Open file and read background path
        with open(f'{workingdir}\\Assets\\backgroundconf.json', "r") as read_file:
            self.imagefilename = json.load(read_file)

        # Open file and read sensor poll list
        with open(f'{workingdir}\\Assets\\sensorpollconf.json', "r") as read_file:
            self.sensorpollinfo = json.load(read_file)

        # Initialize dictionary as blank
        self.labelinfo = {}

        # Create an instance of Tkinter Frame
        self.win = Tk()

        # Grab current screen resolution and set it as the window size
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.win.geometry(f'{self.screen_width}x{self.screen_height}+0+0')

        # Change window settings
        self.win.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        self.win.title("WXtreme - Davis Vantage Pro 2")

        # Open the Image File
        try:
            self.image = Image.open(self.imagefilename)
            self.resized = self.image.resize((self.screen_width, self.screen_height))
            self.image2 = ImageTk.PhotoImage(self.resized)

        # If file not found, add error message to error log
        except FileNotFoundError:
            fileout = open(f'{workingdir}\\ErrorLog.txt', "a")
            fileout.write(f'{datetime.datetime.now()}: Unable to open the following file path: {self.imagefilename}\n')
            fileout.close()
            self.imagefilename = f'{workingdir}\\Assets\\defaultbackground.png'
            self.image = Image.open(self.imagefilename)
            self.resized = self.image.resize((self.screen_width, self.screen_height))
            self.image2 = ImageTk.PhotoImage(self.resized)

        # Create a Canvas
        self.canvas = Canvas(self.win, width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)

        # Add Image inside the Canvas
        self.image_id = self.canvas.create_image(0, 0, image=self.image2, anchor='nw')

        # Create menubar
        self.menubar = Menu(self.win)
        self.win.config(menu=self.menubar)

        # Create a menu
        self.file_menu = Menu(self.menubar, tearoff=False)

        # Add a menu item to the menu
        self.file_menu.add_command(
            label='Exit',
            command=self.ExitProgram
        )

        # Add the file menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu
        )

        # Create a menu
        self.settings_menu = Menu(self.menubar, tearoff=False)

        # Add a menu item to the menu
        self.settings_menu.add_command(
            label='Change Background',
            command=self.ChangeBackground
        )

        # Add a menu item to the menu
        self.settings_menu.add_command(
            label='Change Sensors to Poll',
            command=self.ChangeSensors
        )

        # Add a menu item to the menu
        self.settings_menu.add_command(
            label='Add On-Screen Text',
            command=self.AddTextLabel
        )

        # Add a menu item to the menu
        self.settings_menu.add_command(
            label='Remove All On-Screen Text',
            command=self.RemoveTextLabel
        )

        # Add the settings menu to the menubar
        self.menubar.add_cascade(
            label="Settings",
            menu=self.settings_menu
        )

        # Create a menu
        self.graph_menu = Menu(self.menubar, tearoff=False)

        # Add a menu item to the menu
        self.graph_menu.add_command(
            label='Create Graph',
            command=self.CreateGraph
        )

        # Add the settings menu to the menubar
        self.menubar.add_cascade(
            label="Graph",
            menu=self.graph_menu
        )

        # Create a menu
        self.ftp_menu = Menu(self.menubar, tearoff=False)

        # Add a menu item to the menu
        self.ftp_menu.add_command(
            label='Configure FTP',
            command=self.ConfigFTP
        )

        # Add the settings menu to the menubar
        self.menubar.add_cascade(
            label="FTP",
            menu=self.ftp_menu
        )

        # Event Binds
        self.win.bind("<F11>", self.enableFullscreen)
        self.win.bind("<Escape>", self.disableFullscreen)
        self.win.bind("<Configure>", self.resize_image)
        self.canvas.bind("<Button-1>", self.nearest_item_with_tag)
        self.canvas.bind("<ButtonRelease-1>", self.clear_bind)
        self.canvas.bind("<Button-2>", self.right_click)
        self.canvas.bind("<Button-3>", self.right_click)

        # Call function to create labels
        self.spawnLabels()
        # Call initial function to display sensor data. This function will auto-loop itself
        self.spawnItems()


# Insert Menu Buttons here

    # Exit
    def ExitProgram(self):
        exit()

    def CreateGraph(self):

        def savearcstate():
            startselect = startcal.entry.get()
            endselect = endcal.entry.get()
            arcselect = radioSelection.get()
            creategraphwin.destroy()

            firstslash = startselect.find("/")
            secondslash = startselect.find("/", startselect.find("/") + 1)
            startmonth = startselect[:firstslash]
            startday = startselect[firstslash+1:secondslash]
            startyear = startselect[secondslash+3:]


            firstslash = endselect.find("/")
            secondslash = endselect.find("/", endselect.find("/") + 1)
            endmonth = endselect[:firstslash]
            endday = endselect[firstslash+1:secondslash]
            endyear = endselect[secondslash+3:]

            startminute = 0
            endminute = 30

            starthour = 0
            endhour = 23


            ArcGraph = serialcompi.graphArchiveData(GetCurData, startday, startmonth, startyear, starthour,
            startminute, endday, endmonth, endyear, endhour, endminute)
            ArcGraph.createGraph(arcselect)
            self.close_GUI()
            ArcGraph.show_Graph()


        # Open new window
        creategraphwin = Toplevel(self.win)
        creategraphwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        creategraphwin.title("Select Time Range and Sensor to Graph")
        creategraphwin.geometry('475x400')

        radioSelection = StringVar(creategraphwin, "ArcOutTemp")


        l0 = Label(creategraphwin, text='')
        l0.grid(row=1, column=0, sticky='W', ipady=5, ipadx=5)
        l1 = Labelframe(creategraphwin, text='Select Date Ranges')
        l1.grid(row=1, column=1, sticky='W', ipady=5, ipadx=5)
        l2 = Label(l1, text="Choose Beginning Archive Date")
        l2.grid(row=2, column=1, sticky='W', ipady=5, ipadx=5)
        startcal = DateEntry(l1)
        startcal.grid(row=3, column=1, sticky='W', ipady=5, ipadx=5)
        l3 = Label(l1, text="Choose Ending Archive Date")
        l3.grid(row=4, column=1, sticky='W', ipady=5, ipadx=5)
        endcal = DateEntry(l1)
        endcal.grid(row=5, column=1, sticky='W', ipady=5, ipadx=5)

        l4 = Labelframe(creategraphwin, text='Select Sensor to Graph')
        l4.grid(row=1, column=3, sticky='W', ipady=5, ipadx=5)

        values = {"Outdoor Temperature": "ArcOutTemp",
                  "High Outdoor Temperature": "ArcOutTempHigh",
                  "Low Outdoor Temperature": "ArcOutTempLow",
                  "Rainfall": "ArcRainfall",
                  "Indoor Temperature": "ArcInTemp",
                  "Indoor Humidity": "ArcInHum",
                  "Outdoor Humidity": "ArcOutHum",
                  "Average Wind Speed": "ArcAvWindSpeed",
                  "High Wind Speed": "ArcHighWindSpeed",
                  "High Wind Direction": "ArcDirHi",
                  "Prevailing Wind Direction": "ArcPrevWind"}

        i = 0
        for (text, value) in values.items():
            Radiobutton(l4, text=text, variable=radioSelection,
                        value=value).grid(row=i, column=3, sticky='W', ipady=5, ipadx=5)
            i = i + 1

        lspacer = Label(creategraphwin, text='')
        lspacer.grid(row=11, column=2)

        # Add Save Button
        savebutton = Button(creategraphwin, text="Graph!", command=savearcstate)
        savebutton.grid(row=12, column=2, sticky='W', ipady=5, ipadx=5)

    def ConfigFTP(self):

        templist = []

        # Update list with each selection
        def get_selection():
            if (selcurintemp.get() == 1):
                templist.append('curintemp')
            if (selcurinhum.get() == 1):
                templist.append('curinhum')
            if (selcurouttemp.get() == 1):
                templist.append('curouttemp')
            if (selcurwinspeed.get() == 1):
                templist.append('curwinspeed')
            if (selcurwindir.get() == 1):
                templist.append('curwindir')
            if (selcurouthum.get() == 1):
                templist.append('curouthum')
            if (selcurdailrain.get() == 1):
                templist.append('curdailrain')
            if (selcurraterain.get() == 1):
                templist.append('curraterain')

            if (selhiwinspeed.get() == 1):
                templist.append('hiwinspeed')
            if (selhiintemp.get() == 1):
                templist.append('hiintemp')
            if (sellointemp.get() == 1):
                templist.append('lointemp')
            if (selhiinhum.get() == 1):
                templist.append('hiinhum')
            if (selloinhum.get() == 1):
                templist.append('loinhum')
            if (selhiouttemp.get() == 1):
                templist.append('hiouttemp')
            if (selloouttemp.get() == 1):
                templist.append('loouttemp')

        # Save selections to file
        def save():

            retserver = FTPServerEntry.get()
            retusername = UsernameEntry.get()
            retpassword = PasswordEntry.get()
            retport = PortEntry.get()

            ftpList = []

            # Generate new encryption key
            self.key = Fernet.generate_key()
            self.fernet = Fernet(self.key)

            ftpList.append(retserver)
            ftpList.append(retusername)
            ftpList.append(retpassword)
            if not retport:
                retport = '21'
                ftpList.append(retport)
            else:
                ftpList.append(retport)

            # Encrypt dictionary and save to file
            enclist = str(ftpList)
            enclist = self.fernet.encrypt(enclist.encode()).decode()
            with open(f'{workingdir}\\Assets\\FTPCred.json', "w") as write_file:
                json.dump(enclist, write_file)

            # Decode key and save to file
            self.key = self.key.decode()
            with open(f'{workingdir}\\Assets\\key.json', "w") as write_file:
                json.dump(self.key, write_file)

            # Clear list
            self.ftpinfo = {}

            # Clear out any repeated selections
            for i in templist:
                if i not in self.ftpinfo:
                    self.ftpinfo.update({i: ['placeholder']})

            # Save to file
            with open(f'{workingdir}\\Assets\\ftpsensorconf.json', "w") as write_file:
                json.dump(self.ftpinfo, write_file)

            # Create FTP instance
            ftp = FTP()

            # Connect to and log in to FTP server according to saved information
            try:
                ftp.connect(retserver, int(retport))
                ftp.login(retusername, retpassword)

                # Close window
                configFTPwin.destroy()

                FTPThread = Thread(target = SendFTP)
                FTPThread.start()
            except:
                def tryagain():
                    FTPErrorwin.destroy()

                # Open new window
                FTPErrorwin = Toplevel(configFTPwin)
                FTPErrorwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
                FTPErrorwin.title("Error")
                FTPErrorwin.geometry('150x100')

                l = Label(FTPErrorwin, text='Invalid FTP configuration')
                l.place(relx=.5, rely=.25, anchor=CENTER)
                exitbutton = Button(FTPErrorwin, text="Okay", command=tryagain)
                exitbutton.place(relx=.5, rely=.75, anchor=CENTER)


        # Open new window
        configFTPwin = Toplevel(self.win)
        configFTPwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        configFTPwin.title("Configure FTP settings")
        configFTPwin.geometry('625x560')

        # Initialize each variable
        selcurintemp = IntVar()
        selcurinhum = IntVar()
        selcurouttemp = IntVar()
        selcurwinspeed = IntVar()
        selcurwindir = IntVar()
        selcurouthum = IntVar()
        selcurdailrain = IntVar()
        selcurraterain = IntVar()

        selhiwinspeed = IntVar()
        selhiintemp = IntVar()
        sellointemp = IntVar()
        selhiinhum = IntVar()
        selloinhum = IntVar()
        selhiouttemp = IntVar()
        selloouttemp = IntVar()

        # Create check boxes
        l0 = Label(configFTPwin, text='')
        l0.grid(row=1, column=0, sticky='W', ipady=5, ipadx=5)
        l1 = Labelframe(configFTPwin, text='Current Sensor Values')
        l1.grid(row=1, column=1, sticky='W', ipady=5, ipadx=5)
        c1 = Checkbutton(l1, text='Current Indoor Temp', variable=selcurintemp, onvalue=1, offvalue=0, command=get_selection)
        c1.grid(row=2, column=1, ipadx=5, ipady=5, sticky='W')
        c2 = Checkbutton(l1, text='Current Indoor Humidity', variable=selcurinhum, onvalue=1, offvalue=0, command=get_selection)
        c2.grid(row=3, column=1, ipadx=5, ipady=5, sticky='W')
        c3 = Checkbutton(l1, text='Current Outdoor Temp', variable=selcurouttemp, onvalue=1, offvalue=0, command=get_selection)
        c3.grid(row=4, column=1, ipadx=5, ipady=5, sticky='W')
        c4 = Checkbutton(l1, text='Current Wind Speed', variable=selcurwinspeed, onvalue=1, offvalue=0, command=get_selection)
        c4.grid(row=5, column=1, ipadx=5, ipady=5, sticky='W')
        c5 = Checkbutton(l1, text='Current Wind Direction', variable=selcurwindir, onvalue=1, offvalue=0, command=get_selection)
        c5.grid(row=6, column=1, ipadx=5, ipady=5, sticky='W')
        c6 = Checkbutton(l1, text='Current Outdoor Humidity', variable=selcurouthum, onvalue=1, offvalue=0, command=get_selection)
        c6.grid(row=7, column=1, ipadx=5, ipady=5, sticky='W')
        c7 = Checkbutton(l1, text='Current Daily Rain', variable=selcurdailrain, onvalue=1, offvalue=0, command=get_selection)
        c7.grid(row=8, column=1, ipadx=5, ipady=5, sticky='W')
        c8 = Checkbutton(l1, text='Current Rain Rate', variable=selcurraterain, onvalue=1, offvalue=0, command=get_selection)
        c8.grid(row=9, column=1, ipadx=5, ipady=5, sticky='W')

        l2 = Labelframe(configFTPwin, text='High/Low Sensor Values')
        l2.grid(row=1, column=3, sticky='W', ipady=5, ipadx=5)
        c9 = Checkbutton(l2, text='Daily Peak Wind Speed', variable=selhiwinspeed, onvalue=1, offvalue=0, command=get_selection)
        c9.grid(row=2, column=3, ipadx=5, ipady=5, sticky='W')
        c10 = Checkbutton(l2, text='High Indoor Daily Temp', variable=selhiintemp, onvalue=1, offvalue=0, command=get_selection)
        c10.grid(row=3, column=3, ipadx=5, ipady=5, sticky='W')
        c11 = Checkbutton(l2, text='Low Indoor Daily Temp', variable=sellointemp, onvalue=1, offvalue=0, command=get_selection)
        c11.grid(row=4, column=3, ipadx=5, ipady=5, sticky='W')
        c12 = Checkbutton(l2, text='High Indoor Daily Humidity', variable=selhiinhum, onvalue=1, offvalue=0, command=get_selection)
        c12.grid(row=5, column=3, ipadx=5, ipady=5, sticky='W')
        c13 = Checkbutton(l2, text='Low Indoor Daily Humidity', variable=selloinhum, onvalue=1, offvalue=0, command=get_selection)
        c13.grid(row=6, column=3, ipadx=5, ipady=5, sticky='W')
        c14 = Checkbutton(l2, text='High Outdoor Daily Temperature', variable=selhiouttemp, onvalue=1, offvalue=0, command=get_selection)
        c14.grid(row=7, column=3, ipadx=5, ipady=5, sticky='W')
        c15 = Checkbutton(l2, text='Low Outdoor Daily Temperature', variable=selloouttemp, onvalue=1, offvalue=0, command=get_selection)
        c15.grid(row=8, column=3, ipadx=5, ipady=5, sticky='W')
        l16 = Label(l2, text='')
        l16.grid(row=9, column=3, ipadx=5, ipady=5, sticky='W')

        l3 = Labelframe(configFTPwin, text='FTP Connection Settings')
        l3.grid(row=2, column=2, sticky='N', ipady=5, ipadx=0)
        l7 = Label(l3, text='')
        l7.grid(row=1, column=0)
        l4 = Label(l3, text='FTP Server')
        l4.grid(row=1, column=1, sticky='N', ipady=5, ipadx=5)
        FTPServerEntry = Entry(l3)
        FTPServerEntry.grid(row=2, column=1, sticky='N')
        l5 = Label(l3, text='Username')
        l5.grid(row=3, column=1, sticky='N', ipady=5, ipadx=5)
        UsernameEntry = Entry(l3)
        UsernameEntry.grid(row=4, column=1, sticky='N')
        l6 = Label(l3, text='Password')
        l6.grid(row=5, column=1, sticky='N', ipady=5, ipadx=5)
        PasswordEntry = Entry(l3)
        PasswordEntry.grid(row=6, column=1, sticky='N')
        l8 = Label(l3, text='Port (Leave blank for default of 21)')
        l8.grid(row=7, column=1, sticky='N', ipady=5, ipadx=5)
        PortEntry = Entry(l3)
        PortEntry.grid(row=8, column=1, sticky='N')

        spacer = Label(configFTPwin, text="")
        spacer.grid(row=10, column=2)
        saveandexit_button = Button(configFTPwin, text="Save", command=save)
        saveandexit_button.grid(row=11, column=2, columnspan=1)

    # Prompt for new background
    def ChangeBackground(self):

        # Open file explorer
        tempimagefilename = filedialog.askopenfilename(initialdir=f'{home_directory}\\Pictures', title="Select a File", filetypes=(("Image Files", "*.jpg *.png *.gif"), ("all files", "*.*")))

        # If an image was not selected, don't update the file name
        if not tempimagefilename:
            return
        else:
            self.imagefilename = tempimagefilename

        # Save image path to file for reference later
        with open(f'{workingdir}\\Assets\\backgroundconf.json', "w") as write_file:
            json.dump(self.imagefilename, write_file)

        # Set new image as background
        self.image = Image.open(self.imagefilename)
        self.resized = self.image.resize((self.screen_width, self.screen_height))
        self.image2 = ImageTk.PhotoImage(self.resized)
        self.canvas.itemconfig(self.image_id, image=self.image2)

    # Open prompt to request new sensors to poll
    def ChangeSensors(self):

        # Initialize list
        templist = []

        # Open new window
        changesensorwin = Toplevel(self.win)
        changesensorwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        changesensorwin.title("Select Sensor Data to Display")
        changesensorwin.geometry('475x285')

        # Update list with each selection
        def get_selection():
            if (selcurintemp.get() == 1):
                templist.append('curintemp')
            if (selcurinhum.get() == 1):
                templist.append('curinhum')
            if (selcurouttemp.get() == 1):
                templist.append('curouttemp')
            if (selcurwinspeed.get() == 1):
                templist.append('curwinspeed')
            if (selcurwindir.get() == 1):
                templist.append('curwindir')
            if (selcurouthum.get() == 1):
                templist.append('curouthum')
            if (selcurdailrain.get() == 1):
                templist.append('curdailrain')
            if (selcurraterain.get() == 1):
                templist.append('curraterain')

            if (selhiwinspeed.get() == 1):
                templist.append('hiwinspeed')
            if (selhiintemp.get() == 1):
                templist.append('hiintemp')
            if (sellointemp.get() == 1):
                templist.append('lointemp')
            if (selhiinhum.get() == 1):
                templist.append('hiinhum')
            if (selloinhum.get() == 1):
                templist.append('loinhum')
            if (selhiouttemp.get() == 1):
                templist.append('hiouttemp')
            if (selloouttemp.get() == 1):
                templist.append('loouttemp')

        # Save selections to file
        def save():

            # Clear list
            self.sensorpollinfo = {}

            # Clear out any repeated selections
            for i in templist:
                if i not in self.sensorpollinfo:
                    self.sensorpollinfo.update({i: [50, 50, 'Arial', 12, 'black']})

            # Save to file
            with open (f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
                json.dump(self.sensorpollinfo, write_file)

            # Close window
            changesensorwin.destroy()

            self.displayNewSensors()

        # Initialize each variable
        selcurintemp = IntVar()
        selcurinhum = IntVar()
        selcurouttemp = IntVar()
        selcurwinspeed = IntVar()
        selcurwindir = IntVar()
        selcurouthum = IntVar()
        selcurdailrain = IntVar()
        selcurraterain = IntVar()

        selhiwinspeed = IntVar()
        selhiintemp = IntVar()
        sellointemp = IntVar()
        selhiinhum = IntVar()
        selloinhum = IntVar()
        selhiouttemp = IntVar()
        selloouttemp = IntVar()

        # Create check boxes
        l0 = Label(changesensorwin, text='')
        l0.grid(row=1, column=0, sticky='W', ipady=5, ipadx=5)
        l1 = Labelframe(changesensorwin, text='Current Sensor Values')
        l1.grid(row=1, column=1, sticky='W', ipady=5, ipadx=5)
        c1 = Checkbutton(l1, text='Current Indoor Temp', variable=selcurintemp, onvalue=1, offvalue=0, command=get_selection)
        c1.grid(row=2, column=1, ipadx=5, ipady=5, sticky='W')
        c2 = Checkbutton(l1, text='Current Indoor Humidity', variable=selcurinhum, onvalue=1, offvalue=0, command=get_selection)
        c2.grid(row=3, column=1, ipadx=5, ipady=5, sticky='W')
        c3 = Checkbutton(l1, text='Current Outdoor Temp', variable=selcurouttemp, onvalue=1, offvalue=0, command=get_selection)
        c3.grid(row=4, column=1, ipadx=5, ipady=5, sticky='W')
        c4 = Checkbutton(l1, text='Current Wind Speed', variable=selcurwinspeed, onvalue=1, offvalue=0, command=get_selection)
        c4.grid(row=5, column=1, ipadx=5, ipady=5, sticky='W')
        c5 = Checkbutton(l1, text='Current Wind Direction', variable=selcurwindir, onvalue=1, offvalue=0, command=get_selection)
        c5.grid(row=6, column=1, ipadx=5, ipady=5, sticky='W')
        c6 = Checkbutton(l1, text='Current Outdoor Humidity', variable=selcurouthum, onvalue=1, offvalue=0, command=get_selection)
        c6.grid(row=7, column=1, ipadx=5, ipady=5, sticky='W')
        c7 = Checkbutton(l1, text='Current Daily Rain', variable=selcurdailrain, onvalue=1, offvalue=0, command=get_selection)
        c7.grid(row=8, column=1, ipadx=5, ipady=5, sticky='W')
        c8 = Checkbutton(l1, text='Current Rain Rate', variable=selcurraterain, onvalue=1, offvalue=0, command=get_selection)
        c8.grid(row=9, column=1, ipadx=5, ipady=5, sticky='W')

        l2 = Labelframe(changesensorwin, text='High/Low Sensor Values')
        l2.grid(row=1, column=3, sticky='W', ipady=5, ipadx=5)
        c9 = Checkbutton(l2, text='Daily Peak Wind Speed', variable=selhiwinspeed, onvalue=1, offvalue=0, command=get_selection)
        c9.grid(row=2, column=3, ipadx=5, ipady=5, sticky='W')
        c10 = Checkbutton(l2, text='High Indoor Daily Temp', variable=selhiintemp, onvalue=1, offvalue=0, command=get_selection)
        c10.grid(row=3, column=3, ipadx=5, ipady=5, sticky='W')
        c11 = Checkbutton(l2, text='Low Indoor Daily Temp', variable=sellointemp, onvalue=1, offvalue=0, command=get_selection)
        c11.grid(row=4, column=3, ipadx=5, ipady=5, sticky='W')
        c12 = Checkbutton(l2, text='High Indoor Daily Humidity', variable=selhiinhum, onvalue=1, offvalue=0, command=get_selection)
        c12.grid(row=5, column=3, ipadx=5, ipady=5, sticky='W')
        c13 = Checkbutton(l2, text='Low Indoor Daily Humidity', variable=selloinhum, onvalue=1, offvalue=0, command=get_selection)
        c13.grid(row=6, column=3, ipadx=5, ipady=5, sticky='W')
        c14 = Checkbutton(l2, text='High Outdoor Daily Temperature', variable=selhiouttemp, onvalue=1, offvalue=0, command=get_selection)
        c14.grid(row=7, column=3, ipadx=5, ipady=5, sticky='W')
        c15 = Checkbutton(l2, text='Low Outdoor Daily Temperature', variable=selloouttemp, onvalue=1, offvalue=0, command=get_selection)
        c15.grid(row=8, column=3, ipadx=5, ipady=5, sticky='W')
        l16 = Label(l2, text='')
        l16.grid(row=9, column=3, ipadx=5, ipady=5, sticky='W')

        spacer = Label(changesensorwin, text="")
        spacer.grid(row=10, column=2)
        saveandexit_button = Button(changesensorwin, text="Save", command=save)
        saveandexit_button.grid(row=11, column=2, columnspan=1)

    # Add new label on-screen
    def AddTextLabel(self):
        # Add new label item to dictionary
        self.labelinfo.update({(len(self.label) + 1): [75, 75, 'Arial', 12, 'black', "Right Click To Change"]})

        # Save dictionary to file
        with open(f'{workingdir}\\Assets\\textlabelconf.json', "w") as write_file:
            json.dump(self.labelinfo, write_file)

        # Spawn labels again
        self.spawnLabels()

    # Remove all on-screen text labels
    def RemoveTextLabel(self):
        # Delete all on-screen objects with tag of label
        self.canvas.delete('label')

        # Empty dictionary
        self.labelinfo = {}

        # Save empty dictionary to file
        with open(f'{workingdir}\\Assets\\textlabelconf.json', "w") as write_file:
            json.dump(self.labelinfo, write_file)



# Insert Update Events Here

    def resize_image(self,e):

        # open image to resize it
        self.image = Image.open(self.imagefilename)

        # resize the image with width and height of root
        self.resized = self.image.resize((e.width, e.height))
        self.image2 = ImageTk.PhotoImage(self.resized)
        self.canvas.itemconfig(self.image_id, image=self.image2)

    # Change text properties for a label
    def labelChange(self):
        # Destroy a single label
        def destroylabel():

            # Read text file
            with open(f'{workingdir}\\Assets\\textlabelconf.json', "r") as read_file:
                self.labelinfo = json.load(read_file)

            # If the selected item matches, delete it from the dictionary
            for key, value in self.labelinfo.items():
                if self.res[0] == self.label[key]:
                    del self.labelinfo[key]
                    break

            # Save the dictionary to file
            with open(f'{workingdir}\\Assets\\textlabelconf.json', "w") as write_file:
                json.dump(self.labelinfo, write_file)

            # Close sub window
            changelabelwin.destroy()

            # Recreate on-screen labels
            self.spawnLabels()

        # Save label settings
        def savelabel():

            # Get the user entered text
            self.rettext = entry.get()

            # If the text box was left blank, set to default
            if self.rettext == "":
                self.rettext = "Right Click to Change"

            # Open label config file
            with open(f'{workingdir}\\Assets\\textlabelconf.json', "r") as read_file:
                self.labelinfo = json.load(read_file)

            # Iterate through dictionary
            for key, value in self.labelinfo.items():
                filex, filey, filefont, filesize, filecolor, filetext = [value[i] for i in (0, 1, 2, 3, 4, 4)]

                # If the dictionary item matches the selected item, update the dictionary with the new text settings
                if self.res[0] == self.label[key]:
                    templist = [filex, filey, self.retfont, self.retsize, self.retcolor, self.rettext]
                    self.labelinfo.update({key: templist})

            # Save dictionary to file
            with open(f'{workingdir}\\Assets\\textlabelconf.json', "w") as write_file:
                json.dump(self.labelinfo, write_file)

            # Destroy sub-window
            changelabelwin.destroy()

            # Recreate label items
            self.spawnLabels()

        # Get current coordinates of the selected label item
        templist = self.canvas.coords(self.res[0])
        self.objectx, self.objecty = [templist[i] for i in (0, 1)]

        # Create list of different size options
        sizeoptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                       26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                       49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
                       72, 73, 74, 75
                       ]

        # Create list of different font options
        fontoptions = ['Arial', 'Helvetica', 'Times', 'Calibri']

        # Create list of different color options
        coloroptions = ["Black", "White", "Gray", "Light Gray", "Pink", "Red", "Orange", "Yellow", "Lime", "Green",
                        "Cyan", "Blue", "Purple", "Brown"]

        # Open new window
        changelabelwin = Toplevel(self.win)
        changelabelwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        changelabelwin.title("Modify Text Properties")
        changelabelwin.geometry('335x265')

        # Set size select variable as Int
        sizeselect = IntVar(changelabelwin)

        # Set font select variable as String
        fontselect = StringVar(changelabelwin)

        # Set color select variable as String
        colorselect = StringVar(changelabelwin)

        # Create GUI widgets
        l0 = Label(changelabelwin, text='')
        l0.grid(row=1, column=0, sticky='W', ipady=5, ipadx=5)
        l1 = Labelframe(changelabelwin, text='Change Label Settings')
        l1.grid(row=1, column=1, sticky='W', ipady=5, ipadx=5)

        spacer = Label(l1, text="")
        spacer.grid(row=1, column=2)

        sizeoption = OptionMenu(l1, sizeselect, 12, *sizeoptions)
        sizeoption.grid(row=2, column=1, sticky='W', ipady=5, ipadx=5)

        spacer1 = Label(l1, text="")
        spacer1.grid(row=2, column=2)

        coloroption = OptionMenu(l1, colorselect, "Black", *coloroptions)
        coloroption.grid(row=2, column=3, sticky='N', ipady=5, ipadx=5)

        spacer2 = Label(l1, text="")
        spacer2.grid(row=2, column=4)

        fontoption = OptionMenu(l1, fontselect, "Arial", *fontoptions)
        fontoption.grid(row=2, column=5, sticky='E', ipady=5, ipadx=5)

        spacer3 = Label(l1, text="")
        spacer3.grid(row=3, column=2)

        l2 = Label(l1, text='Enter Label Text')
        l2.grid(row=4, column=3, sticky='N')

        entry = Entry(l1)
        entry.grid(row=5, column=3, sticky='N')

        spacer4 = Label(l1, text="")
        spacer4.grid(row=6, column=1)

        saveandexit_button = Button(l1, text="Save", command=savelabel)
        saveandexit_button.grid(row=11, column=3, columnspan=1, sticky='N')

        spacer5 = Label(l1, text ="")
        spacer5.grid(row=12, column=1)

        destroy_button = Button(l1, text="Delete", command=destroylabel)
        destroy_button.grid(row=22, column=3, columnspan=1, sticky='N')

        # Get the size selection
        def change_size_dropdown(*args):
            self.retsize = sizeselect.get()

        # Get the font selection
        def change_font_dropdown(*args):
            self.retfont = fontselect.get()

        # Get the color selection
        def change_color_dropdown(*args):
            self.retcolor = colorselect.get()

        # If size is changed, call change_size_dropdown
        sizeselect.trace('w', change_size_dropdown)

        # If font is changed, call change_font_dropdown
        fontselect.trace('w', change_font_dropdown)

        # If color is changed, call change_color_dropdown
        colorselect.trace('w', change_color_dropdown)

    def right_click(self, event):

        # Set default return value. Will change if the user changes the selection, but sets the variable if the user
        # doesn't select something
        self.retfont = "Arial"
        self.retsize = 12
        self.retcolor = "Black"

        def savefont():

            # Read text file
            with open(f'{workingdir}\\Assets\\sensorpollconf.json', "r") as read_file:
                self.sensorpollinfo = json.load(read_file)

            # Iterate through dictionary
            for key, value in self.sensorpollinfo.items():
                filex, filey, filefont, filesize, filecolor = [value[i] for i in (0, 1, 2, 3, 4)]

                # If the dictionary value matches the selected item, update it with the new information
                if self.res[0] == self.dataDisplay[key]:
                    templist = [filex, filey, self.retfont, self.retsize, self.retcolor]
                    self.sensorpollinfo.update({key: templist})

            # Save the dictionary to file
            with open(f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
                json.dump(self.sensorpollinfo, write_file)

            # Destroy sub-window
            changefontwin.destroy()

            # Re-create items
            self.spawnItems()

        # Get the ID of the nearest items
        self.res = self.canvas.find_closest(event.x, event.y, halo=0)
        # If it's the ID of the background, dont do anything
        if self.res[0] == 1:
            return

        # Checks if it's a label value that was right clicked
        if self.res[0] in self.label.values():
            self.labelChange()
            return

        # Get the current coordinates of the selected item
        templist = self.canvas.coords(self.res[0])
        self.objectx, self.objecty = [templist[i] for i in (0, 1)]

        # Create list with size options
        sizeoptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                       26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                       49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
                       72, 73, 74, 75
                      ]

        # Create list with font options
        fontoptions = ['Arial', 'Helvetica', 'Times', 'Calibri']

        # Create list with color options
        coloroptions = ["Black", "White", "Gray", "Light Gray", "Pink", "Red", "Orange", "Yellow", "Lime", "Green", "Cyan", "Blue", "Purple", "Brown"]

        # Open new window
        changefontwin = Toplevel(self.win)
        changefontwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        changefontwin.title("Modify Text Properties")
        changefontwin.geometry('285x150')

        # Set size select variable as Int
        sizeselect = IntVar(changefontwin)

        # Set font select variable as String
        fontselect = StringVar(changefontwin)

        # Set color select variable as String
        colorselect = StringVar(changefontwin)

        # Create window widgets
        l0 = Label(changefontwin, text='')
        l0.grid(row=1, column=0, sticky='W', ipady=5, ipadx=5)
        l1 = Labelframe(changefontwin, text='Change Font Settings')
        l1.grid(row=1, column=1, sticky='W', ipady=5, ipadx=5)

        spacer = Label(l1, text="")
        spacer.grid(row=1, column=2)

        sizeoption = OptionMenu(l1, sizeselect, 12, *sizeoptions)
        sizeoption.grid(row=2, column=1, sticky='W', ipady=5, ipadx=5)

        spacer1 = Label(l1, text="")
        spacer1.grid(row=2, column=2)

        coloroption = OptionMenu(l1, colorselect, "Black", *coloroptions)
        coloroption.grid(row=2, column=3, sticky='W', ipady=5, ipadx=5)

        spacer2 = Label(l1, text="")
        spacer2.grid(row=2, column=4)

        fontoption = OptionMenu(l1, fontselect, "Arial", *fontoptions)
        fontoption.grid(row=2, column=5, sticky='W', ipady=5, ipadx=5)

        spacer3 = Label(l1, text="")
        spacer3.grid(row=3, column=2)

        saveandexit_button = Button(l1, text="Save", command=savefont)
        saveandexit_button.grid(row=11, column=3, columnspan=1)

        # Get size selection
        def change_size_dropdown(*args):
            self.retsize = sizeselect.get()

        # Get font selection
        def change_font_dropdown(*args):
            self.retfont = fontselect.get()

        # Get color selection
        def change_color_dropdown(*args):
            self.retcolor = colorselect.get()

        # If size is changed, call change_size_dropdown
        sizeselect.trace('w', change_size_dropdown)

        # If font is changed, call change_font_dropdown
        fontselect.trace('w', change_font_dropdown)

        # If color is changed, call change_color_dropdown
        colorselect.trace('w', change_color_dropdown)

    def enableFullscreen(self,e):

        self.win.attributes('-fullscreen', True)

        # Get rid of menubar
        self.win.config(menu="")

    def disableFullscreen(self,e):

        self.win.attributes('-fullscreen', False)

        # Add menubar
        self.win.config(menu=self.menubar)

    def displayNewSensors(self):
        # In here, CREATE each text display

        # If an after statement as been generated, kill it
        try:
            self.afterid
            self.win.after_cancel(self.afterid)
        except AttributeError:
            pass

        # Delete all on-screen items with tag sensor
        self.canvas.delete('sensor')

        # Initialize Dictionary (Only way to create new canvas items in a loop, as seen below)
        self.dataDisplay = {}

        # Populate dictionary with sensor data
        self.dataDict = GetCurData.getData()

        # Iterate through dictionary. If the sensor data was selected in dataDict, then create a canvas item
        i = 50
        for key, value in self.dataDict.items():
            if key in self.sensorpollinfo:
                templist = self.sensorpollinfo.get(key)
                x, y, font, size, color = [templist[i] for i in (0, 1, 2, 3, 4)]

                if key == 'curintemp':
                    sensorname = 'Current In. Temp.'
                if key == 'curinhum':
                    sensorname = 'Current In. Hum.'
                if key == 'curouttemp':
                    sensorname = 'Current Out. Temp.'
                if key == 'curwinspeed':
                    sensorname = 'Current Wind Speed'
                if key == 'curwindir':
                    sensorname = 'Current Wind Dir.'
                if key == 'curouthum':
                    sensorname = 'Current Out. Hum.'
                if key == 'curdailrain':
                    sensorname = 'Daily Rain'
                if key == 'curraterain':
                    sensorname = 'Rain Rate'
                if key == 'hiwinspeed':
                    sensorname = 'High Wind Speed'
                if key == 'hiintemp':
                    sensorname = 'High In. Temp.'
                if key == 'lointemp':
                    sensorname = 'Low In. Temp.'
                if key == 'hiinhum':
                    sensorname = 'High In. Hum.'
                if key == 'loinhum':
                    sensorname = 'Low In. Hum.'
                if key == 'hiouttemp':
                    sensorname = 'High Out. Temp.'
                if key == 'loouttemp':
                    sensorname = 'Low Out. Temp.'


                self.dataDisplay[key] = self.canvas.create_text(x + i, y, text=sensorname, tags="sensor", font=(font, size), fill=color)
                i = i + 130

        # After 10 seconds, update sensors
        self.afterid = self.win.after(10000, self.updateSensorData)

    def spawnLabels(self):

        # Remove all on-screen items with tag label
        self.canvas.delete('label')

        # Empty dictionary
        self.label = {}

        # Read file
        with open(f'{workingdir}\\Assets\\textlabelconf.json', "r") as read_file:
            self.labelinfo = json.load(read_file)

        # Iterate through dictionary, spawning label items
        for key, value in self.labelinfo.items():
            templist = self.labelinfo.get(key)
            x, y, font, size, color, filetext = [templist[i] for i in (0, 1, 2, 3, 4, 5)]
            self.label[key] = self.canvas.create_text(x, y, text=filetext, tags='label', font=(font, size), fill=color)

    def spawnItems(self):
        # In here, CREATE each text display

        # If an after statement as been generated, kill it
        try:
            self.afterid
            self.win.after_cancel(self.afterid)
        except AttributeError:
            pass

        # Delete all items with tag sensor
        self.canvas.delete('sensor')

        # Initialize Dictionary (Only way to create new canvas items in a loop, as seen below)
        self.dataDisplay = {}

        # Populate dictionary with sensor data
        self.dataDict = GetCurData.getData()

        # Iterate through dictionary. If the sensor data was selected in dataDict, then create a canvas item
        i = 0
        for key, value in self.dataDict.items():
            if key in self.sensorpollinfo:
                templist = self.sensorpollinfo.get(key)
                x, y, font, size, color = [templist[i] for i in (0, 1, 2, 3, 4)]
                self.dataDisplay[key] = self.canvas.create_text(x, y, text=value, tags="sensor", font=(font, size), fill=color)
                i = i + 75

        # After 1 second, update sensors
        self.afterid = self.win.after(1000, self.updateSensorData)


    def updateSensorData(self):
        # In here, UPDATE each text display

        # Populate dictionary with sensor data
        self.dataDict = GetCurData.getData()

        # Iterate through dictionary, updating each on-screen value
        for key, value in self.dataDict.items():
            if key in self.sensorpollinfo:
                self.canvas.itemconfigure(self.dataDisplay[key], text=value)

        # Update again after 1 second
        self.afterid = self.win.after(1000, self.updateSensorData)

    # Clear mouse bind to canvas item
    def clear_bind(self, event):

        self.canvas.unbind("<B1-Motion>")

        # Read file
        with open(f'{workingdir}\\Assets\\sensorpollconf.json', "r") as read_file:
            self.sensorpollinfo = json.load(read_file)

        # Read file
        with open(f'{workingdir}\\Assets\\textlabelconf.json', "r") as read_file:
            self.labelinfo = json.load(read_file)

        # Iterate through dictionary
        for key, value in self.sensorpollinfo.items():
            filex, filey, filefont, filesize, filecolor = [value[i] for i in (0, 1, 2, 3, 4)]

            # If selected item matches dictionary key, update dictionary with current status
            if self.res[0] == self.dataDisplay[key]:
                templist = [self.objectx, self.objecty, filefont, filesize, filecolor]
                self.sensorpollinfo.update({key: templist})

        # After an item is initially created (not on program start, but if sensor selection is changes), this updates the displayed text when the item is drug around the screen
        for key, value in self.sensorpollinfo.items():
            if self.res[0] == self.dataDisplay[key]:
                self.canvas.itemconfigure(self.dataDisplay[key], text=self.dataDict[key])

        # Iterate through dictionary
        for key, value in self.labelinfo.items():
            filex, filey, filefont, filesize, filecolor, filetext = [value[i] for i in (0, 1, 2, 3, 4, 5)]

            # If selected item matches dictionary key, update dictionary with current status
            if self.res[0] == self.label[key]:
                templist = [self.objectx, self.objecty, filefont, filesize, filecolor, filetext]
                self.labelinfo.update({key: templist})

        # Save to file
        with open(f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
            json.dump(self.sensorpollinfo, write_file)

        # Save to file
        with open(f'{workingdir}\\Assets\\textlabelconf.json', "w") as write_file:
            json.dump(self.labelinfo, write_file)

    # Find the nearest canvas item when mouse is clicked, bind that item to the mouse motion, making it draggable
    def nearest_item_with_tag(self, event):
        self.res = self.canvas.find_closest(event.x, event.y, halo=0)
        if self.res[0] == 1:
            return
        cmd = lambda x: self.relocate(self.res[0])
        self.canvas.bind("<B1-Motion>", cmd)

    # Use the mouse coordinates as the new location for the canvas item
    def relocate(self, id):
        x0, y0 = self.canvas.winfo_pointerxy()
        x0 -= self.canvas.winfo_rootx()
        y0 -= self.canvas.winfo_rooty()

        self.objectx = x0
        self.objecty = y0

        self.canvas.coords(id, x0, y0,)

    def close_GUI(self):
        self.win.destroy()

# Create splash screen
splash_root = Tk()

# Clear title bar
splash_root.overrideredirect(1)

# Set screen geometry values to be 1/4 of the screen width
screen_width = int(splash_root.winfo_screenwidth() / 4)
screen_height = screen_width

# Find the center of the screen, then adjust for the size of the window. Used to create the window in the exact center of the screen
screen_centerx = int((splash_root.winfo_screenwidth() / 2) - screen_width / 2)
screen_centery = int((splash_root.winfo_screenheight() / 2) - screen_height / 2)

# Change size of window to previously calculated values, and at previously calculated position
splash_root.geometry(f'{screen_width}x{screen_height}+{screen_centerx}+{screen_centery}')

# Grab splashscreen image file and resize
image = Image.open(f'{workingdir}\\Assets\\logo.png')
resized = image.resize((screen_width, screen_height))
image2 = ImageTk.PhotoImage(resized)

# Create canvas
canvas = Canvas(splash_root, width=400, height=400)
canvas.pack(fill=BOTH, expand=True)

# Add image to canvas
canvas.create_image(0, 0, image=image2, anchor='nw')

# After x amount of milliseconds, create instance of GUI class (which destroys splashscreen)
splash_root.after(30, GUI)


mainloop()