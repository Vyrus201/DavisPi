# Import the required libraries
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image
import datetime
import json
import serialcompi

# ToDo: If background file is not found, need to add code to default to a different background file, otherwise the GUI window won't launch

# Create Class Instance
#GetCurData = serialcompi.SerData()

# Destroy Class Instance - Run destructor and print all data objects
#del GetCurData



class GUI:
    def __init__(self):

        # Destroy splashscreen
        splash_root.destroy()

        # Open file and read background path
        with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\backgroundconf.json", "r") as read_file:
            self.imagefilename = json.load(read_file)

        # Open file and read sensor poll list
        with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\sensorpollconf.json", "r") as read_file:
            self.sensorpollinfo = json.load(read_file)

        # Create an instance of Tkinter Frame
        self.win = Tk()
        self.win.iconbitmap('icon.ico')
        self.win.title("WXtreme - Davis Vantage Pro 2")

        # Grab current screen resolution and set it as the window size
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.win.geometry(f'{self.screen_width}x{self.screen_height}')

        # Open the Image File
        try:
            self.image = Image.open(self.imagefilename)
            self.resized = self.image.resize((self.screen_width, self.screen_height))
            self.image2 = ImageTk.PhotoImage(self.resized)

        # If file not found, add error message to error log
        except FileNotFoundError:
            fileout = open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\ErrorLog.txt", "a")
            fileout.write(f'{datetime.datetime.now()}: Unable to open the following file path: {self.imagefilename}\n')
            fileout.close()
            exit()

        # Create a Canvas
        self.canvas = Canvas(self.win, width=800, height=600)
        self.canvas.pack(fill=BOTH, expand=True)

        # Add Image inside the Canvas
        self.canvas.create_image(0, 0, image=self.image2, anchor='nw')

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

        # Add the settings menu to the menubar
        self.menubar.add_cascade(
            label="Settings",
            menu=self.settings_menu
        )

        # Event Binds
        self.win.bind("<F11>", self.enableFullscreen)
        self.win.bind("<Escape>", self.disableFullscreen)
        self.win.bind("<Configure>", self.resize_image)




# Insert Menu Buttons here

    # Exit
    def ExitProgram(self):
        exit()

    # Prompt for new background
    def ChangeBackground(self):

        # Open file explorer
        tempimagefilename = filedialog.askopenfilename(initialdir="C:\\Users\\brink\\Pictures", title="Select a File", filetypes=(("Image Files", "*.jpg *.png *.gif"), ("all files", "*.*")))

        # If an image was not selected, don't update the file name
        if not tempimagefilename:
            return
        else:
            self.imagefilename = tempimagefilename

        # Save image path to file for reference later
        with open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\backgroundconf.json", "w") as write_file:
            json.dump(self.imagefilename, write_file)

        # Set new image as background
        self.image = Image.open(self.imagefilename)
        self.resized = self.image.resize((self.screen_width, self.screen_height))
        self.image2 = ImageTk.PhotoImage(self.resized)
        self.canvas.create_image(0, 0, image=self.image2, anchor='nw')

    # Open prompt to request new sensors to poll
    def ChangeSensors(self):

        # Initialize list
        templist = []

        # Open new window
        changesensorwin = Toplevel(self.win)
        changesensorwin.title("Select Sensor Data to Display")
        changesensorwin.geometry('475x325')

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
            self.sensorpollinfo = []

            # Clear out any repeated selections
            for i in templist:
                if i not in self.sensorpollinfo:
                    self.sensorpollinfo.append(i)

            # Save to file
            with open ("C:\\Users\\brink\\PycharmProjects\\DavisPi\\sensorpollconf.json", "w") as write_file:
                json.dump(self.sensorpollinfo, write_file)

            # Close window
            changesensorwin.destroy()

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
        l1 = Label(changesensorwin, text='Current Sensor Values')
        l1.grid(row=1, column=1, sticky='W', ipady=5)
        c1 = Checkbutton(changesensorwin, text='Current Indoor Temp', variable=selcurintemp, onvalue=1, offvalue=0, command=get_selection)
        c1.grid(row=2, column=1, ipadx=50, ipady=5, sticky='W')
        c2 = Checkbutton(changesensorwin, text='Current Indoor Humidity', variable=selcurinhum, onvalue=1, offvalue=0, command=get_selection)
        c2.grid(row=3, column=1, ipadx=50, ipady=5, sticky='W')
        c3 = Checkbutton(changesensorwin, text='Current Outdoor Temp', variable=selcurouttemp, onvalue=1, offvalue=0, command=get_selection)
        c3.grid(row=4, column=1, ipadx=50, ipady=5, sticky='W')
        c4 = Checkbutton(changesensorwin, text='Current Wind Speed', variable=selcurwinspeed, onvalue=1, offvalue=0, command=get_selection)
        c4.grid(row=5, column=1, ipadx=50, ipady=5, sticky='W')
        c5 = Checkbutton(changesensorwin, text='Current Wind Direction', variable=selcurwindir, onvalue=1, offvalue=0, command=get_selection)
        c5.grid(row=6, column=1, ipadx=50, ipady=5, sticky='W')
        c6 = Checkbutton(changesensorwin, text='Current Outdoor Humidity', variable=selcurouthum, onvalue=1, offvalue=0, command=get_selection)
        c6.grid(row=7, column=1, ipadx=50, ipady=5, sticky='W')
        c7 = Checkbutton(changesensorwin, text='Current Daily Rain', variable=selcurdailrain, onvalue=1, offvalue=0, command=get_selection)
        c7.grid(row=8, column=1, ipadx=50, ipady=5, sticky='W')
        c8 = Checkbutton(changesensorwin, text='Current Rain Rate', variable=selcurraterain, onvalue=1, offvalue=0, command=get_selection)
        c8.grid(row=9, column=1, ipadx=50, ipady=5, sticky='W')

        l1 = Label(changesensorwin, text='High/Low Sensor Values')
        l1.grid(row=1, column=2, sticky='W', ipady=5)
        c9 = Checkbutton(changesensorwin, text='Daily Peak Wind Speed', variable=selhiwinspeed, onvalue=1, offvalue=0, command=get_selection)
        c9.grid(row=2, column=2, ipadx=50, ipady=5, sticky='W')
        c10 = Checkbutton(changesensorwin, text='High Indoor Daily Temp', variable=selhiintemp, onvalue=1, offvalue=0, command=get_selection)
        c10.grid(row=3, column=2, ipadx=50, ipady=5, sticky='W')
        c11 = Checkbutton(changesensorwin, text='Low Indoor Daily Temp', variable=sellointemp, onvalue=1, offvalue=0, command=get_selection)
        c11.grid(row=4, column=2, ipadx=50, ipady=5, sticky='W')
        c12 = Checkbutton(changesensorwin, text='High Indoor Daily Humidity', variable=selhiinhum, onvalue=1, offvalue=0, command=get_selection)
        c12.grid(row=5, column=2, ipadx=50, ipady=5, sticky='W')
        c13 = Checkbutton(changesensorwin, text='Low Indoor Daily Humidity', variable=selloinhum, onvalue=1, offvalue=0, command=get_selection)
        c13.grid(row=6, column=2, ipadx=50, ipady=5, sticky='W')
        c14 = Checkbutton(changesensorwin, text='High Outdoor Daily Temperature', variable=selhiouttemp, onvalue=1, offvalue=0, command=get_selection)
        c14.grid(row=7, column=2, ipadx=50, ipady=5, sticky='W')
        c15 = Checkbutton(changesensorwin, text='Low Outdoor Daily Temperature', variable=selloouttemp, onvalue=1, offvalue=0, command=get_selection)
        c15.grid(row=8, column=2, ipadx=50, ipady=5, sticky='W')

        saveandexit_button = Button(changesensorwin, text="Save", command=save)
        saveandexit_button.grid(row=10, column=1, columnspan=2)


# Insert Update Events Here

    def resize_image(self,e):

        # open image to resize it
        self.image = Image.open(self.imagefilename)

        # resize the image with width and height of root
        self.resized = self.image.resize((e.width, e.height))
        self.image2 = ImageTk.PhotoImage(self.resized)
        self.canvas.create_image(0, 0, image=self.image2, anchor='nw')

    def enableFullscreen(self,e):

        self.win.attributes('-fullscreen', True)

        # Get rid of menubar
        self.win.config(menu="")

    def disableFullscreen(self,e):

        self.win.attributes('-fullscreen', False)

        # Add menubar
        self.win.config(menu=self.menubar)

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
image = Image.open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\logo.png")
resized = image.resize((screen_width, screen_height))
image2 = ImageTk.PhotoImage(resized)

# Create canvas
canvas = Canvas(splash_root, width=400, height=400)
canvas.pack(fill=BOTH, expand=True)

# Add image to canvas
canvas.create_image(0,0, image=image2, anchor='nw')

# After x amount of milliseconds, create instance of GUI class (which destroys splashscreen)
splash_root.after(3500, GUI)

# Loop
mainloop()

