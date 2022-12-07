# Import the required libraries
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image

# ToDo: Attempt to save/read file path from ini or some other file format. Maybe XML??

class GUI:
    def __init__(self):
        # Open file and read background path
        filein = (open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\backgroundconf.txt", "r"))
        self.imagefilename = filein.readline()
        filein.close()

        # Open file and read sensor poll list
        filein = (open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\sensorpollconf.txt", "r"))
        data = filein.read()
        self.sensorpollinfo = data.split(",")

        # Create an instance of Tkinter Frame
        self.win = Tk()
        self.win.title("Weather Station")

        # Grab current screen resolution and set it as the window size
        self.screen_width = self.win.winfo_screenwidth()
        self.screen_height = self.win.winfo_screenheight()
        self.win.geometry(f'{self.screen_width}x{self.screen_height}')

        # Open the Image File
        try:
            self.image = Image.open(self.imagefilename)
            self.resized = self.image.resize((self.screen_width, self.screen_height))
            self.image2 = ImageTk.PhotoImage(self.resized)
        except FileNotFoundError:
            fileout = open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\ErrorLog.txt", "w")
            fileout.write(f'Unable to open the following file path: {self.imagefilename}')
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
    def ExitProgram(self):
        exit()

    def ChangeBackground(self):
        tempimagefilename = filedialog.askopenfilename(initialdir="C:\\Users\\brink\\Pictures", title="Select a File", filetypes=(("Image Files", "*.jpg *.png *.gif"), ("all files", "*.*")))
        # If an image was not selected, don't update the file name
        if not tempimagefilename:
            return
        else:
            self.imagefilename = tempimagefilename
        fileout = open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\backgroundconf.txt", "w")
        fileout.write(self.imagefilename)
        fileout.close()
        self.image = Image.open(self.imagefilename)
        self.resized = self.image.resize((self.screen_width, self.screen_height))
        self.image2 = ImageTk.PhotoImage(self.resized)
        self.canvas.create_image(0, 0, image=self.image2, anchor='nw')

    def ChangeSensors(self):
        templist = []
        changesensorwin = Toplevel(self.win)
        changesensorwin.title("Select Sensor Data to Display")
        changesensorwin.geometry('700x300')

        def get_selection():
            if (selcurintemp.get() == 1):
                templist.append('curintemp')
            if (selcurinhum.get() == 1):
                templist.append('curinhum')

        def save():
            self.sensorpollinfo = []
            for i in templist:
                if i not in self.sensorpollinfo:
                    self.sensorpollinfo.append(i)
            fileout = open("C:\\Users\\brink\\PycharmProjects\\DavisPi\\sensorpollconf.txt", "w")
            fileout.write(",".join(self.sensorpollinfo))
            fileout.close()

            changesensorwin.destroy()

        selcurintemp = IntVar()
        selcurinhum = IntVar()
        c1 = Checkbutton(changesensorwin, text='Current Indoor Temp', variable=selcurintemp, onvalue=1, offvalue=0, command=get_selection)
        c1.pack()
        c2 = Checkbutton(changesensorwin, text='Current Indoor Humidity', variable=selcurinhum, onvalue=1, offvalue=0, command=get_selection)
        c2.pack()
        saveandexit_button = Button(changesensorwin, text="Save", command=save)
        saveandexit_button.pack(pady=20)


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



Window = GUI()
Window.win.mainloop()
