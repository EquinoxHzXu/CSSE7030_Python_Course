class Plotter(tk.Canvas):
    
    def __init__(self, parent, data):
        super().__init__(parent)
        self._width = self.winfo_width()
        self._height = self.winfo_height()
        self._points = []
        self._data = data

    def get_points(self, filename):
        self._points = []
        self._translator = CoordinateTranslator(430, 200,
                                    Station(filename).get_year_range()[0],
                                                Station(filename).get_year_range()[1],
                                                Station(filename).get_temp_range()[0],
                                                Station(filename).get_temp_range()[1])                   
        for x,y in Station(filename).get_data_points():
            self._points.append(self._translator.temperature_coords(x,y))
        return self._points


class TemperaturePlotApp(object):
    def __init__(self, master):
        self._data = TemperatureData()
        # Create the main interface
        self._master = master
        master.title("Max Temperature Plotter")
        master.minsize(430,200)
        
        # Create the station label
        self._frm2 = tk.Frame(master)
        self._frm2.pack(side=tk.BOTTOM, anchor=tk.W)      
        self._stationlbl = tk.Label(self._frm2, text="Station Selection:    ")
        self._stationlbl.pack(side=tk.LEFT)        
        
        # Create the menu
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.open_file)

        # Create the Canvas
        self._plotter = Plotter(master, self._data)
        self._canvas = tk.Canvas(master, bg="white", bd=2, relief=tk.SUNKEN)
        self._canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)


        # Create the temperature label
        self._frm1 = tk.Frame(master)
        self._frm1.pack(side=tk.TOP, anchor=tk.W)      
        self._datalbl = tk.Label(self._frm1, text=" ")
        self._datalbl.pack(side=tk.LEFT)



                
        self._filename = ''
        self._filenames = []
        
        self._year = 1970 # to set by Canvas event
        
    def open_file(self):      
        self._filename = filedialog.askopenfilename()
        self._filenames = self._filename.split("/")
        self._this_filename = self._filenames[-1]
        try:
            self._data.load_data(self._filename)
        except UnicodeDecodeError:
            messagebox.showerror("Invalid File",
                                 "This is not a '.txt\' file.")
        except ValueError:
            messagebox.showerror("Invalid Data", "Data is invalid")
        except IndexError:
            messagebox.showerror("Invalid Data", "Data is invalid")
        
       
        self.add_temperature(self._year, len(self._data.get_stations())-1) 
        self.add_checkbutton(self._filename,
                             len(self._data.get_stations())-1)
        self.draw(len(self._data.get_stations())-1)


    def draw(self,i):
        self._canvas.create_line(self._plotter.get_points(self._this_filename),
                                 fill=COLOURS[i])
    
    def add_temperature(self, year, i):
        templbl = tk.Label(self._frm1,
                                 text=Station(self._filename).get_temp(year),
                           fg=COLOURS[i])
        templbl.pack(side=tk.LEFT) 
        self._datalbl.config(text="Data for "+str(self._year)+":   ")    

    def add_checkbutton(self, filename, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text=Station(filename).get_name(),
                             fg=COLOURS[i])
        cbx.pack(side=tk.LEFT)
        cbx.select()
