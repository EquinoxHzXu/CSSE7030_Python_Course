
#
# Support for assignment 2
#

# Imports for use in your assignment
import tkinter as tk
import os.path
from tkinter import filedialog
from tkinter import messagebox

# colours for drawing lines and text
COLOURS = ['#f90909', '#ffa405', '#c0c203', '#1abd04', '#058096', '#042ee1', 
           '#d30af1','#ec06b3']

def load_data_points(filename):
    """Return the data contained in the given file.

    load_data_points(str) -> dict(int:float)
    """
    fd = open(filename, 'r')
    data = {}
    for line in fd:
        parts = line.split(',')
        data[int(parts[0])] = float(parts[1])
    return data


class FileExtensionException(Exception):
    pass

class Station(object):
    """A class for storing yearly average temperature data for a given station
    """
    def __init__(self, stationfile):
        """ Constructor: Station(str)"""
        self._data = load_data_points(stationfile)
        keys = self._data.keys()
        self._min_year = min(keys)
        self._max_year = max(keys)
        temps = self._data.values()
        self._min_temp = min(temps)
        self._max_temp = max(temps)
        base = os.path.basename(stationfile)
        if not base.endswith('.txt'):
            raise(FileExtensionException())
        self._name = base.replace(".txt", "")

    def get_temp(self, year):
        """Return the temperature average for the given year.

        get_temp(int) -> float
        """
        return self._data.get(year)

    def get_data_points(self):
        """Return the data as a list of points in year order

        get_data_points() -> list((int, float))
        """
        return [(year, self._data[year]) for year in sorted(self._data.keys())]

    def get_year_range(self):
        """ Return the range of years in the data

        get_year_range() -> (int, int)
        """
        return (self._min_year, self._max_year)

    def get_temp_range(self):
        """Return the range of temperatures in the data

        get_temp_range() -> (float, float)
        """
        return (self._min_temp, self._max_temp)

    def get_name(self):
        return self._name

    def __repr__(self):
        return "Station({0})".format(self._name)

class CoordinateTranslator(object):
    """A class which manages translation of data values into (x, y) coordinates.

    The application manages real-world data (year, temp), but the Canvas 
    drawings require (x, y) coordinates. This class
    converts between the two.

    """

    def __init__(self, width, height, min_year, max_year, min_temp, max_temp):
        """
        Create a CoordinateTranslator with the given canvas width/height,
        the smallest and largest years and 
        the smallest and largest temperatures

        Constructor: CoordinateTranslator(int, int, int, int, float, float)
        """
        self._min_year = min_year
        self._max_year = max_year
        self._min_temp = min_temp
        self._max_temp = max_temp
        self.resize(width, height)

    def resize(self, width, height):
        """Adjust the scaling factors to account for a new width/height.

        After the Canvas resizes, call this method to fix the scaling.
        """
        self._xscale = (self._max_year - self._min_year) / width
        self._yscale = (self._max_temp - self._min_temp) / height
        self._width = width
        self._height = height


    def temperature_coords(self, year, temperature):
        """Given a year and a temperature,
           return (x, y) coordinates to plot.

        temperature_coords(int, float) -> (float, float)
        """
        return ((year - self._min_year)/ self._xscale,
                self._height - (temperature - self._min_temp) / self._yscale)

    def get_year(self, x):
        """Given an x coordinate on the Canvas, return the year that it
           corresponds to.

        get_year(float) -> int
        """
        return int(x * self._xscale + 0.5) + self._min_year


## CSSE7030

def best_fit(points):
    """Given points are a list of (x,y) points ordered by x
    this function computes the best line fit over that range and 
    returns the coords of end points of the line.

    best_fit(list((floatt, float)) -> ((float, float), (float, float))
    """
    count = len(points)
    if count == 0:
        # needed to avoid division by zero
        # return something that will not appear on screen if drawn
        return ((-1,-1), (-1, -1))
    x_values = [x for x, _ in points]
    y_values = [y for _, y in points]
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_x2 = sum(x**2 for x in x_values)
    sum_y2 = sum(y**2 for y in y_values)
    sum_xy = sum(x*y for x,y in points)
    x_mean = sum_x/count
    y_mean = sum_y/count
    slope = (sum_xy - sum_x * y_mean) / (sum_x2 - sum_x * x_mean)
    y_inter = y_mean - slope * x_mean
    return ((x_values[0], slope * x_values[0]  + y_inter),
            (x_values[-1], slope * x_values[-1]  + y_inter))
