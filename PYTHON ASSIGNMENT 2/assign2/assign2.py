
###################################################################
#
#   CSSE1001/7030 - Assignment 2
#
#   Student Number: 43400465
#
#   Student Name: Haoze Xu
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign2_support import *

#####################################
# End of support 
#####################################

# Add your code here

class TemperatureData(object):

    #This class is to construct a basic data model
    
    def __init__(self):
        self._stations = []
        self._data = {}
        self._min_year = 0
        self._max_year = 0
        self._min_temp = 0.0
        self._max_temp = 0.0
        self._is_selected = []
        self._stationfile = []

    def load_data(self, filename):
        self._current_station = Station(filename)
        self._stations.append(self._current_station.get_name())
        self._is_selected.append(True)

    def get_data(self):
        for name in self._stations:
            self._data[name] = self._current_station
        return self._data
    
    def get_stations(self):
        return self._stations

    def get_ranges(self):
        for station in self._stations:
            min_year, max_year = Station(station+".txt").get_year_range()
            min_temp, max_temp = Station(station+".txt").get_temp_range()
            if self._min_year == 0 and self._max_year == 0:
                self._min_year = min_year
                self._max_year = max_year
            if self._min_year != 0 and self._max_year != 0:
                if min_year < self._min_year:
                    self._min_year = min_year
                if max_year > self._max_year:
                    self._max_year = max_year
            if self._min_temp == 0.0 and self._max_temp == 0.0:
                self._min_temp = min_temp
                self._max_temp = max_temp
            if self._min_temp != 0.0 and self._max_temp != 0.0:
                if min_temp < self._min_temp:
                    self._min_temp = min_temp
                if max_temp > self._max_temp:
                    self._max_temp = max_temp
                
        return (self._min_year, self._max_year, self._min_temp, self._max_temp)

    def toggle_selected(self, i):
        if self._is_selected[i] == True:
            self._is_selected[i] = False
        else:
            if self._is_selected[i] == False:
                self._is_selected[i] = True
 
    def is_selected(self, i):
        return self._is_selected[i]

    def get_is_selected(self):
        return self._is_selected

class Plotter(tk.Canvas):

    #The class is used to create an x-y coordinate axis.
    
    def __init__(self, parent, data, canvas):
        super().__init__(parent)
        self._canvas = canvas
        self._width = self._canvas.winfo_width()
        self._height = self._canvas.winfo_height()
        self._points = []
        self._data = data
        self._translator = CoordinateTranslator(self._width, self._height,
                                                self._data.get_ranges()[0],
                                                self._data.get_ranges()[1],
                                                self._data.get_ranges()[2],
                                                self._data.get_ranges()[3])

        #self._canvas.bind("<Configure>", TemperaturePlotApp.draw_all)
        # 'Event' object has no attribute ***

        
    def get_points(self, filename):
        self._points = []
        for x,y in Station(filename).get_data_points():
            self._points.append(self._translator.temperature_coords(x,y))
        return self._points

    def get_translator(self):
        return self._translator
        

class SelectionFrame(tk.Frame):
    
    #The class is used to listen the event of checkbuttons.
    
    def __init__(self, parent, data):
        super().__init__(parent)
        self._data = data
        

    def get_redraw_list(self):
       
        i = 0
        selected_index = []
        filenames = []
        redraw_list = []

        stations = self._data.get_stations()
        is_selected = self._data.get_is_selected()
        
        for selected in is_selected: # get index which is True to show
            if selected == True:
                selected_index.append(i)
            i += 1
        for station in stations: # get filenames that are opened
            filename = station + ".txt"
            filenames.append(filename)

        for index in selected_index:
            redraw_list.append((filenames[index], index))

        return redraw_list
        
    
    def Brisbane_select(self):
        index = self._data.get_stations().index("Brisbane")
        self._data.toggle_selected(index)

    def Adelaide_select(self):
        index = self._data.get_stations().index("Adelaide")
        self._data.toggle_selected(index)

    def Canberra_select(self):
        index = self._data.get_stations().index("Canberra")
        self._data.toggle_selected(index)

    def Darwin_select(self):
        index = self._data.get_stations().index("Darwin")
        self._data.toggle_selected(index)
        
    def Hobart_select(self):
        index = self._data.get_stations().index("Hobart")
        self._data.toggle_selected(index)
        
    def Melbourne_select(self):
        index = self._data.get_stations().index("Melbourne")
        self._data.toggle_selected(index)

    def Perth_select(self):
        index = self._data.get_stations().index("Perth")
        self._data.toggle_selected(index)
        
    def Sydney_select(self):
        index = self._data.get_stations().index("Sydney")
        self._data.toggle_selected(index)




class DataFrame(tk.Frame):
    def __init__(self, parent, data, canvas, plot):
        super().__init__(parent)
        self._data = data
        self._canvas = canvas
        self._plot = plot

    def _get_year(self, x):
        return self._plot.get_translator().get_year(x)

class TemperaturePlotApp(object):
    def __init__(self, master):
        self._data = TemperatureData()
        # Create the main interface
        self._master = master
        master.title("Max Temperature Plotter")
        
        
        # Create the station label
        self._frm2 = tk.Frame(master)
        self._frm2.pack(side=tk.BOTTOM, anchor=tk.W)      
        self._stationlbl = tk.Label(self._frm2,
                                    text="Station Selection:    ")
        self._stationlbl.pack(side=tk.LEFT)        
        
        # Create the menu
        menubar = tk.Menu(master)
        master.config(menu=menubar)

        filemenu = tk.Menu(menubar)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Open", command=self.open_file)


        # Create the Canvas
        self._canvas = tk.Canvas(master, bg="white", bd=2,
                                 relief=tk.SUNKEN)
        self._canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        self._canvas.bind("<Button-1>", self.get_year_changed)
        self._canvas.bind("<B1-Motion>", self.get_year_changed)
        self._canvas.bind_all("<Key>", self.key_pressed)
        
        

        # Create the temperature label
        self._frm1 = tk.Frame(master)
        self._frm1.pack(side=tk.TOP, anchor=tk.W)      
        self._yearlbl = tk.Label(self._frm1, text=" ")
        self._yearlbl.pack(side=tk.LEFT)

        self._selection = SelectionFrame(master, self._data)
                
        self._filename = ''
        self._filenames = []
        self._brisbane_points = []
        self._brisbane_points2 = []
        self._best_brisbane_points = []
        self._adelaide_points = []
        self._adelaide_points2 = []
        self._best_adelaide_points = []
        self._canberra_points = []
        self._canberra_points2 = []
        self._best_canberra_points = []
        self._darwin_points = []
        self._darwin_points2 = []
        self._best_darwin_points = []
        self._hobart_points = []
        self._hobart_points2 = []
        self._best_hobart_points = []
        self._melbourne_points = []
        self._melbourne_points2 = []
        self._best_melbourne_points = []        
        self._perth_points = []
        self._perth_points2 = []
        self._best_perth_points = []
        self._sydney_points = []
        self._sydney_points2 = []
        self._best_sydney_points = []

        self._i = 0        
        self._year = 0



    def open_file(self):      
        self._filename = filedialog.askopenfilename()
        self._filenames = self._filename.split("/")
        self._this_filename = self._filenames[-1]
        try:
            self._data.load_data(self._this_filename)
        except UnicodeDecodeError:
            messagebox.showerror("Invalid File",
                                 "This is not a '.txt\' file.")
        except ValueError:
            messagebox.showerror("Invalid Data", "Data is invalid")
        except IndexError:
            messagebox.showerror("Invalid Data", "Data is invalid")
        
       
      
        
        if self._this_filename == "Brisbane.txt":
            self.add_Brisbane_checkbutton(len(self._data.get_stations())-1)
            self.add_Brisbane_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Adelaide.txt":
            self.add_Adelaide_checkbutton(len(self._data.get_stations())-1)
            self.add_Adelaide_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Canberra.txt":
            self.add_Canberra_checkbutton(len(self._data.get_stations())-1)
            self.add_Canberra_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Darwin.txt":
            self.add_Darwin_checkbutton(len(self._data.get_stations())-1)
            self.add_Darwin_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Hobart.txt":
            self.add_Hobart_checkbutton(len(self._data.get_stations())-1)
            self.add_Hobart_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Melbourne.txt":
            self.add_Melbourne_checkbutton(len(self._data.get_stations())-1)
            self.add_Melbourne_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Perth.txt":
            self.add_Perth_checkbutton(len(self._data.get_stations())-1)
            self.add_Perth_temperature(len(self._data.get_stations())-1)
        if self._this_filename == "Sydney.txt":
            self.add_Sydney_checkbutton(len(self._data.get_stations())-1)
            self.add_Sydney_temperature(len(self._data.get_stations())-1)

        
        self.draw_all()
        self._df = DataFrame(self._master, self._data, self._canvas, self._plot)
        
        
    def draw(self, filename, i):
        self._plot = Plotter(self._master, self._data, self._canvas)
        self._canvas.create_line(self._plot.get_points(filename),
                                     fill=COLOURS[i])
    def draw_all(self):
        self._canvas.delete(tk.ALL)
        for station in self._data.get_stations():
            filename = station + ".txt"
            self.draw(filename, self._data.get_stations().index(station))


    # Events
    def get_year_changed(self,event): 
        if len(self._data.get_stations()) != 0:
            self.draw_all()     # Clean the line created when canvas is clicked
            self._canvas.create_line([(event.x, 0),
                                      (event.x, self._canvas.winfo_height())])
            self._year = self._df._get_year(event.x)
            self._yearlbl.config(text="Data for "+str(self._year)+":   ")

            for station in self._data.get_stations():
                if station == "Brisbane":
                    min_year, max_year = Station("Brisbane.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._brisbanelbl.config(text=
                                                 Station("Brisbane.txt").
                                                 get_temp(self._year))
                    else:
                        self._brisbanelbl.config(text="   ")                        
                if station == "Adelaide":
                    min_year, max_year = Station("Adelaide.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._adelaidelbl.config(text=
                                                 Station("Adelaide.txt").
                                                 get_temp(self._year))
                    else:
                        self._adelaidelbl.config(text="   ") 
                if station == "Canberra":
                    min_year, max_year = Station("Canberra.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._canberralbl.config(text=
                                                 Station("Canberra.txt").
                                                 get_temp(self._year))
                    else:
                        self._canberralbl.config(text="   ")
                if station == "Darwin":
                    min_year, max_year = Station("Darwin.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._darwinlbl.config(text=
                                                 Station("Darwin.txt").
                                                 get_temp(self._year))
                    else:
                        self._darwinlbl.config(text="   ")
                if station == "Hobart":
                    min_year, max_year = Station("Hobart.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._hobartlbl.config(text=
                                                 Station("Hobart.txt").
                                                 get_temp(self._year))
                    else:
                        self._hobartlbl.config(text="   ") 

                if station == "Melbourne":
                    min_year, max_year = Station("Melbourne.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._melbournelbl.config(text=
                                                 Station("Melbourne.txt").
                                                 get_temp(self._year))
                    else:
                        self._melbournelbl.config(text="   ") 

                if station == "Perth":
                    min_year, max_year = Station("Perth.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._perthlbl.config(text=
                                                 Station("Perth.txt").
                                                 get_temp(self._year))
                    else:
                        self._perthlbl.config(text="   ") 
                if station == "Sydney":
                    min_year, max_year = Station("Sydney.txt").get_year_range()
                    if self._year > min_year and self._year < max_year:
                        self._sydneylbl.config(text=
                                                 Station("Sydney.txt").
                                                 get_temp(self._year))
                    else:
                        self._sydneylbl.config(text="   ") 

    def key_pressed(self,event):
        self._i += 1

        if self._i == 1:
            for station in self._data.get_stations():
                if station == "Brisbane":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Brisbane.txt").get_temp(self._year))
                    for point in self._plot.get_points("Brisbane.txt"):
                        if x < point[0]:
                            self._brisbane_points.append(point)
                if station == "Adelaide":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Adelaide.txt").get_temp(self._year))
                    for point in self._plot.get_points("Adelaide.txt"):
                        if x < point[0]:
                            self._adelaide_points.append(point)                            
                if station == "Canberra":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Canberra.txt").get_temp(self._year))
                    for point in self._plot.get_points("Canberra.txt"):
                        if x < point[0]:
                            self._canberra_points.append(point) 
                if station == "Darwin":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Darwin.txt").get_temp(self._year))
                    for point in self._plot.get_points("Darwin.txt"):
                        if x < point[0]:
                            self._darwin_points.append(point) 
                if station == "Hobart":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Hobart.txt").get_temp(self._year))
                    for point in self._plot.get_points("Hobart.txt"):
                        if x < point[0]:
                            self._hobart_points.append(point) 
                if station == "Melbourne":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Melbourne.txt").get_temp(self._year))
                    for point in self._plot.get_points("Melbourne.txt"):
                        if x < point[0]:
                            self._melbourne_points.append(point) 
                if station == "Perth":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Perth.txt").get_temp(self._year))
                    for point in self._plot.get_points("Perth.txt"):
                        if x < point[0]:
                            self._perth_points.append(point) 
                if station == "Sydney":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Sydney.txt").get_temp(self._year))
                    for point in self._plot.get_points("Sydney.txt"):
                        if x < point[0]:
                            self._sydney_points.append(point) 
        if self._i == 2:
            for station in self._data.get_stations():
                if station == "Brisbane":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Brisbane.txt").get_temp(self._year))
                    for point in self._brisbane_points:
                        if x > point[0]:
                            self._brisbane_points2.append(point)
                    self._best_brisbane_points.append(best_fit(self.
                                                               _brisbane_points2)[0])
                    self._best_brisbane_points.append(best_fit(self.
                                                               _brisbane_points2)[1])
                    self._canvas.create_line(self._best_brisbane_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Brisbane")])
                if station == "Adelaide":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Adelaide.txt").get_temp(self._year))
                    for point in self._adelaide_points:
                        if x > point[0]:
                            self._adelaide_points2.append(point)
                    self._best_adelaide_points.append(best_fit(self.
                                                               _adelaide_points2)[0])
                    self._best_adelaide_points.append(best_fit(self.
                                                               _adelaide_points2)[1])
                    self._canvas.create_line(self._best_adelaide_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Adelaide")])
                if station == "Canberra":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Canberra.txt").get_temp(self._year))
                    for point in self._canberra_points:
                        if x > point[0]:
                            self._canberra_points2.append(point)
                    self._best_canberra_points.append(best_fit(self.
                                                               _canberra_points2)[0])
                    self._best_canberra_points.append(best_fit(self.
                                                               _canberra_points2)[1])
                    self._canvas.create_line(self._best_canberra_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Canberra")])

                if station == "Darwin":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Darwin.txt").get_temp(self._year))
                    for point in self._darwin_points:
                        if x > point[0]:
                            self._darwin_points2.append(point)
                    self._best_darwin_points.append(best_fit(self.
                                                               _darwin_points2)[0])
                    self._best_darwin_points.append(best_fit(self.
                                                               _darwin_points2)[1])
                    self._canvas.create_line(self._best_darwin_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Darwin")])
                if station == "Hobart":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Hobart.txt").get_temp(self._year))
                    for point in self._hobart_points:
                        if x > point[0]:
                            self._hobart_points2.append(point)
                    self._best_hobart_points.append(best_fit(self.
                                                               _hobart_points2)[0])
                    self._best_hobart_points.append(best_fit(self.
                                                               _hobart_points2)[1])
                    self._canvas.create_line(self._best_hobart_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Hobart")])
                if station == "Melbourne":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Melbourne.txt").get_temp(self._year))
                    for point in self._melbourne_points:
                        if x > point[0]:
                            self._melbourne_points2.append(point)
                    self._best_melbourne_points.append(best_fit(self.
                                                               _melbourne_points2)[0])
                    self._best_melbourne_points.append(best_fit(self.
                                                               _melbourne_points2)[1])
                    self._canvas.create_line(self._best_melbourne_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Melbourne")])
                if station == "Perth":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Perth.txt").get_temp(self._year))
                    for point in self._perth_points:
                        if x > point[0]:
                            self._perth_points2.append(point)
                    self._best_perth_points.append(best_fit(self.
                                                               _perth_points2)[0])
                    self._best_perth_points.append(best_fit(self.
                                                               _perth_points2)[1])
                    self._canvas.create_line(self._best_perth_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Perth")])
                if station == "Sydney":
                    x,y = self._plot.get_translator().temperature_coords(
                        self._year, Station("Sydney.txt").get_temp(self._year))
                    for point in self._sydney_points:
                        if x > point[0]:
                            self._sydney_points2.append(point)
                    self._best_sydney_points.append(best_fit(self.
                                                               _sydney_points2)[0])
                    self._best_sydney_points.append(best_fit(self.
                                                               _sydney_points2)[1])
                    self._canvas.create_line(self._best_sydney_points, width=2,
                                             fill=COLOURS[self._data.get_stations().
                                                          index("Sydney")])




        if self._i == 3:
            self.draw_all()
            self._i = 0
            self._brisbane_points = []
            self._brisbane_points2 = []
            self._best_brisbane_points = []

            self._adelaide_points = []
            self._adelaide_points2 = []
            self._best_adelaide_points = []

            self._canberra_points = []
            self._canberra_points2 = []
            self._best_canberra_points = []

            self._darwin_points = []
            self._darwin_points2 = []
            self._best_darwin_points = []

            self._hobart_points = []
            self._hobart_points2 = []
            self._best_hobart_points = []
            
            self._melbourne_points = []
            self._melbourne_points2 = []
            self._best_melbourne_points = []

            self._perth_points = []
            self._perth_points2 = []
            self._best_perth_points = []

            self._sydney_points = []
            self._sydney_points2 = []
            self._best_sydney_points = []    
        
        


    # If the checkbutton is deselected, clear all lines in self._canvas
    # and redraw lines excluding the station that is deselected.
    # At the same time change the text of labels
    def redraw_Brisbane(self):
        self._canvas.delete(tk.ALL)
        self._selection.Brisbane_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Brisbane")) == False:
            self._brisbanelbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Brisbane")) == True:
            self._brisbanelbl.config(text=Station("Brisbane.txt").
                                                 get_temp(self._year))
    def redraw_Adelaide(self):
        self._canvas.delete(tk.ALL)
        self._selection.Adelaide_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Adelaide")) == False:
            self._adelaidelbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Adelaide")) == True:
            self._adelaidelbl.config(text=Station("Adelaid.txt").
                                                 get_temp(self._year))
    def redraw_Canberra(self):
        self._canvas.delete(tk.ALL)
        self._selection.Canberra_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Canberra")) == False:
            self._canberralbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Canberra")) == True:
            self._canberralbl.config(text=Station("Canberra.txt").
                                                 get_temp(self._year))
    def redraw_Darwin(self):
        self._canvas.delete(tk.ALL)
        self._selection.Darwin_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Darwin")) == False:
            self._darwinlbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Darwin")) == True:
            self._darwinlbl.config(text=Station("Darwin.txt").
                                                 get_temp(self._year))
    def redraw_Hobart(self):
        self._canvas.delete(tk.ALL)
        self._selection.Hobart_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Hobart")) == False:
            self._hobartlbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Hobart")) == True:
            self._hobartlbl.config(text=Station("Hobart.txt").
                                                 get_temp(self._year))
    def redraw_Melbourne(self):
        self._canvas.delete(tk.ALL)
        self._selection.Melbourne_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Melbourne")) == False:
            self._melbournelbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Melbourne")) == True:
            self._melbournelbl.config(text=Station("Melbourne.txt").
                                                 get_temp(self._year))
    def redraw_Perth(self):
        self._canvas.delete(tk.ALL)
        self._selection.Perth_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Perth")) == False:
            self._perthlbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Perth")) == True:
            self._perthlbl.config(text=Station("Perth.txt").
                                                 get_temp(self._year))
    def redraw_Sydney(self):
        self._canvas.delete(tk.ALL)
        self._selection.Sydney_select()
        redraw_list = self._selection.get_redraw_list()
        for filename, i in redraw_list:
            self.draw(filename, i)
        if self._data.is_selected(self._data.get_stations().index("Sydney")) == False:
            self._sydneylbl.config(text="   ")
        if self._data.is_selected(self._data.get_stations().index("Sydney")) == True:
            self._sydneylbl.config(text=Station("Sydney.txt").
                                                 get_temp(self._year))




    #Add labels to show the temerature for selected year 
    def add_Brisbane_temperature(self, i):
        self._brisbanelbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._brisbanelbl.pack(side=tk.LEFT)        
    def add_Adelaide_temperature(self, i):
        self._adelaidelbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._adelaidelbl.pack(side=tk.LEFT)
    def add_Canberra_temperature(self, i):
        self._canberralbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._canberralbl.pack(side=tk.LEFT)
    def add_Darwin_temperature(self, i):
        self._darwinlbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._darwinlbl.pack(side=tk.LEFT)
    def add_Hobart_temperature(self, i):
        self._hobartlbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._hobartlbl.pack(side=tk.LEFT)
    def add_Melbourne_temperature(self, i):
        self._melbournelbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._melbournelbl.pack(side=tk.LEFT)
    def add_Perth_temperature(self, i):
        self._perthlbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._perthlbl.pack(side=tk.LEFT)
    def add_Sydney_temperature(self, i):
        self._sydneylbl = tk.Label(self._frm1, text="   ", fg=COLOURS[i])
        self._sydneylbl.pack(side=tk.LEFT)





        




    #Add checkbuttons of every single station       
    def add_Brisbane_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Brisbane", fg=COLOURS[i],
                                     command=self.redraw_Brisbane)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Adelaide_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Adelaide", fg=COLOURS[i],
                                     command=self.redraw_Adelaide)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Canberra_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Canberra", fg=COLOURS[i],
                                     command=self.redraw_Canberra)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Darwin_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Darwin", fg=COLOURS[i],
                                     command=self.redraw_Darwin)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Hobart_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Hobart", fg=COLOURS[i],
                                     command=self.redraw_Hobart)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Melbourne_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Melbourne", fg=COLOURS[i],
                                     command=self.redraw_Melbourne)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Perth_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Perth", fg=COLOURS[i],
                                     command=self.redraw_Perth)
        cbx.pack(side=tk.LEFT)
        cbx.select()
    def add_Sydney_checkbutton(self, i):
        cbx = tk.Checkbutton(self._frm2,
                                   text="Sydney", fg=COLOURS[i],
                                     command=self.redraw_Sydney)
        cbx.pack(side=tk.LEFT)
        cbx.select()




    
##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
###################################################

def main():
    root = tk.Tk()
    app = TemperaturePlotApp(root)
    root.geometry("800x400")
    root.mainloop()

if __name__ == '__main__':
    main()
