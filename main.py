# Import the required libraries
from tkinter import *
from tkinter.ttk import *
#import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import filedialog
from PIL import ImageTk, Image
import datetime
import json
import os
import serialcompi

# Create Class Instance
GetCurData = serialcompi.SerData()

# Sync Time
GetCurData.updateTime()

# Destroy Class Instance - Run destructor and print all data objects
#del GetCurData

# Get current directory
workingdir = os.getcwd()

# Get current user home directory
home_directory = os.path.expanduser( '~' )

class GUI:
    def __init__(self):

        # Destroy splashscreen
        splash_root.destroy()

        # Open file and read background path
        with open(f'{workingdir}\\Assets\\backgroundconf.json', "r") as read_file:
            self.imagefilename = json.load(read_file)

        # Open file and read sensor poll list
        with open(f'{workingdir}\\Assets\\sensorpollconf.json', "r") as read_file:
            self.sensorpollinfo = json.load(read_file)

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
            label='Save Screen Configuration',
            command=self.saveOnScreenLocation
        )

        # Add the settings menu to the menubar
        self.menubar.add_cascade(
            label="Settings",
            menu=self.settings_menu
        )


        # Event Binds
        self.win.bind("<F11>", self.enableFullscreen)
        self.win.bind("<Escape>", self.disableFullscreen)
        self.win.bind("<Configure>", self.resize_image)
        self.canvas.bind("<Button-1>", self.nearest_item_with_tag)
        self.canvas.bind("<ButtonRelease-1>", self.clear_bind)
        self.canvas.bind("<Button-2>", self.right_click)
        self.canvas.bind("<Button-3>", self.right_click)

        # Call initial function to display sensor data. This function will auto-loop itself
        self.displaySensorData()


# Insert Menu Buttons here

    # Exit
    def ExitProgram(self):
        exit()

    # Save each object location to text file
    def saveOnScreenLocation(self):
        # Iterate through dictionary, getting the coordinates of each item
        for key in self.sensorpollinfo:
            templist = self.canvas.coords(self.dataDisplay[key])
            x, y = [templist[i] for i in (0, 1)]
            self.sensorpollinfo.update({key: [x, y, 'Arial', 12]})

            with open (f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
                json.dump(self.sensorpollinfo, write_file)

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
                    self.sensorpollinfo.update({i: [50, 50, 'Arial', 12]})

            # Save to file
            with open (f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
                json.dump(self.sensorpollinfo, write_file)

            # Close window
            changesensorwin.destroy()

            self.displaySensorData()

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


# Insert Update Events Here

    def resize_image(self,e):

        # open image to resize it
        self.image = Image.open(self.imagefilename)

        # resize the image with width and height of root
        self.resized = self.image.resize((e.width, e.height))
        self.image2 = ImageTk.PhotoImage(self.resized)
        self.canvas.itemconfig(self.image_id, image=self.image2)

    def right_click(self, event):

        # Set default return value. Will change if the user changes the selection, but sets the variable if the user
        # doesn't select something
        self.retfont = "Arial"
        self.retsize = "12"

        def savefont():

            with open(f'{workingdir}\\Assets\\sensorpollconf.json', "r") as read_file:
                self.sensorpollinfo = json.load(read_file)

            for key, value in self.sensorpollinfo.items():
                filex, filey, filefont, filesize = [value[i] for i in (0, 1, 2, 3)]
                if filex == self.objectx and filey == self.objecty:
                    templist = [filex, filey, self.retfont, self.retsize]
                    self.sensorpollinfo.update({key: templist})

            with open (f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
                json.dump(self.sensorpollinfo, write_file)

            changefontwin.destroy()

            self.displaySensorData()




        res = self.canvas.find_closest(event.x, event.y, halo=0)
        if res[0] == 1:
            return
        templist = self.canvas.coords(res[0])
        self.objectx, self.objecty = [templist[i] for i in (0, 1)]


        sizeoptions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                       26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
                       49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
                       72, 73, 74, 75
                      ]

        fontoptions = ['Arial', 'Helvetica']

        # Open new window
        changefontwin = Toplevel(self.win)
        changefontwin.iconbitmap(f'{workingdir}\\Assets\\icon.ico')
        changefontwin.title("Modify Text Properties")
        changefontwin.geometry('230x150')

        sizeselect = IntVar(changefontwin)

        fontselect = StringVar(changefontwin)

        l0 = Label(changefontwin, text='')
        l0.grid(row=1, column=0, sticky='W', ipady=5, ipadx=5)
        l1 = Labelframe(changefontwin, text='Change Font Settings')
        l1.grid(row=1, column=1, sticky='W', ipady=5, ipadx=5)

        spacer = Label(l1, text="")
        spacer.grid(row=1, column=2)

        sizeoption = OptionMenu(l1, sizeselect, 12, *sizeoptions)
        sizeoption.grid(row=2, column=1, sticky='W', ipady=5, ipadx=5)
        sizeoption = OptionMenu(l1, fontselect, "Arial", *fontoptions)
        sizeoption.grid(row=2, column=3, sticky='W', ipady=5, ipadx=5)

        spacer1 = Label(l1, text="")
        spacer1.grid(row=3, column=2)

        saveandexit_button = Button(l1, text="Save", command=savefont)
        saveandexit_button.grid(row=11, column=2, columnspan=1)


        def change_size_dropdown(*args):
            self.retsize = sizeselect.get()

        def change_font_dropdown(*args):
            self.retfont = fontselect.get()

        sizeselect.trace('w', change_size_dropdown)

        fontselect.trace('w', change_font_dropdown)

    def enableFullscreen(self,e):

        self.win.attributes('-fullscreen', True)

        # Get rid of menubar
        self.win.config(menu="")

    def disableFullscreen(self,e):

        self.win.attributes('-fullscreen', False)

        # Add menubar
        self.win.config(menu=self.menubar)

    def displaySensorData(self):
        # In here, CREATE each text display

        # If an after statement as been generated, kill it
        try:
            self.afterid
            self.win.after_cancel(self.afterid)
        except AttributeError:
            pass

        self.canvas.delete('sensor')

        # Initialize Dictionary (Only way to create new canvas items in a loop, as seen below)
        self.dataDisplay = {}

        # Populate dictionary with sensor data
        dataDict = GetCurData.getData()

        # Iterate through dictionary. If the sensor data was selected in dataDict, then create a canvas item
        for key, value in dataDict.items():
            if key in self.sensorpollinfo:
                templist = self.sensorpollinfo.get(key)
                x, y, font, size = [templist[i] for i in (0, 1, 2, 3)]
                self.dataDisplay[key] = self.canvas.create_text(x, y, text=value, tags=("sensor", key), font=(font, size))


        # After 1 second, update sensors
        self.win.after(1000, self.updateSensorData)


    def updateSensorData(self):
        # In here, UPDATE each text display

        # Populate dictionary with sensor data
        dataDict = GetCurData.getData()

        # Iterate through dictionary, updating each on-screen value
        for key, value in dataDict.items():
            if key in self.sensorpollinfo:
                self.canvas.itemconfigure(self.dataDisplay[key], text=value)

        # Update again after 1 second
        self.afterid = self.win.after(1000, self.updateSensorData)

    # Clear mouse bind to canvas item
    def clear_bind(self, event):

        with open(f'{workingdir}\\Assets\\sensorpollconf.json', "r") as read_file:
            self.sensorpollinfo = json.load(read_file)

        for key, value in self.sensorpollinfo.items():
            filex, filey, filefont, filesize = [value[i] for i in (0, 1, 2, 3)]
            if self.res[0] == self.dataDisplay[key]:
                templist = [self.objectx, self.objecty, filefont, filesize]
                self.sensorpollinfo.update({key: templist})

        with open(f'{workingdir}\\Assets\\sensorpollconf.json', "w") as write_file:
            json.dump(self.sensorpollinfo, write_file)

        self.canvas.unbind("<B1-Motion>")

    # Find the nearest canvas item when mouse is clicked, bind that item to the mouse motion, making it draggable
    def nearest_item_with_tag(self, event):
        self.res = self.canvas.find_closest(event.x, event.y, halo=0)
        if self.res[0] == 1:
            return
        cmd = lambda x: self.relocate(self.res[0])
        self.canvas.bind("<B1-Motion>", cmd)

    # Use the mouse coordinates as the new location for the canvas item
    def relocate (self, id):
        x0, y0 = self.canvas.winfo_pointerxy()
        x0 -= self.canvas.winfo_rootx()
        y0 -= self.canvas.winfo_rooty()

        self.objectx = x0
        self.objecty = y0

        self.canvas.coords(id, x0, y0,)

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
canvas.create_image(0,0, image=image2, anchor='nw')

# After x amount of milliseconds, create instance of GUI class (which destroys splashscreen)
splash_root.after(30, GUI)


mainloop()
