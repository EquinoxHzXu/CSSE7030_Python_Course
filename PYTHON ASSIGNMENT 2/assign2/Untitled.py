from assign2_support import *
import tkinter as tk
import os.path
from tkinter import filedialog
from tkinter import messagebox

class TemperatureData(object):
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


def get_points(data):
    points = []
    filenames = []
    ranges = data.get_ranges()
    for station in data.get_stations():
        filename = station + ".txt"
        filenames.append(filename)
    translator = CoordinateTranslator(400, 200,
                                    ranges[0], ranges[1], ranges[2], ranges[3])
                  
    for filename in filenames:
        for x,y in Station(filename).get_data_points():
            points.append(translator.temperature_coords(x,y))
    return points


'''
class Plotter(tk.Canvas):
    
    def __init__(self, parent):
        super().__init__(parent)
        self._width = self.winfo_width()
        self._height = self.winfo_height()
        self._points = []

    def draw(self, filename):
        self._plot = CoordinateTranslator(self._width, self._height,
                                    Station(filename).get_year_range()[0],
                                    Station(filename).get_year_range()[1],
                                    Station(filename).get_temp_range()[0],
                                    Station(filename).get_temp_range()[1])
                    
        for x, y in Station(filename).get_data_points():
            self._points.append(self._plot.temperature_coords(x,y))
        self.create_line(self._points)

    def resize(self):
        #self._plot.resize()
        pass


class SelectionFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def select(self, data):
        pass
        
        
        
    

class DataFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

    def get_year(self):
        # mouse position
        pass

    def display(self, i):
        pass
        #if TemperaturePlotApp.get_data().is_selected(i) == True:

        #if TemperaturePlotApp.get_data().is_selected(i) == False:
            


class TemperaturePlotApp(object):
    def __init__(self, master):
        self._data = TemperatureData()
        # Create the main interface
        self._master = master
        master.title("Max Temperature Plotter")
        
        # Create the Canvas
        self._plotter = Plotter(self._master)
        self._plotter.pack(side=tk.TOP, expand=True, fill=tk.BOTH)        


        # Create the temperature label
        self._frm1 = tk.Frame(master)
        self._frm1.pack(side=tk.TOP, anchor=tk.W)      
        self._datalbl = tk.Label(self._frm1, text=" ")
        self._datalbl.pack(side=tk.LEFT)
        
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


        self._filename = ''
        #self._cbxlist=[]
        #self._filenames = []
        
        self._year = 1970 # to set by Canvas event
        
    def open_file(self):      
        self._filename = filedialog.askopenfilename()
        try:
            self._data.load_data(self._filename)
            #self._filenames.append(self._filename)
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

        self._plotter.draw(self._filename)

    
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
        #self._cbxlist.append(cbx)
        cbx.select()

    #def get_checkbutton(self):
        #return self._cbxlist

    #def get_filenames(self):
        #return self._filenames
        
#    def button_pressed(self):
#        self._lll.config(text=self._data.get_data())
           
        

# add_checkbutton & add_temperature and related labels to other two method
# Canvas clear and draw all curves everytime
# add_checkbutton first, create data



def main():
    root = tk.Tk()
    app = TemperaturePlotApp(root)
    root.geometry("800x400")
    root.mainloop()

if __name__ == '__main__':
    main()

'''
