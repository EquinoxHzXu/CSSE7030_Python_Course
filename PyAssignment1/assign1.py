
###################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Number: 43400465
#
#   Student Name: Haoze Xu
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign1_support import *

#####################################
# End of support 
#####################################

# Add your code here

def load_dates(stations):
    station = stations[0]
    allDates = []
    fin = open(station+'.txt','r')
    for line in fin:
        line=line.strip()
        date,temperature = line.split()
        allDates.append(date)
    return allDates
###
# Input a list[] of stations from '*.txt'
# Return a list[] of dates
###
def load_station_data(station):
    data = ''
    alldata = []
    fin = open(station+'.txt','r')
    for line in fin:
        date,temperature = line.split()
        alldata.append(float(temperature))
    return alldata
###
# Input a string() of single station
# Return a list[] of temperature of a single station
# need to be used in load_all_stations_data(stations),
# or use a FOR LOOP to select every single station
###
def load_all_stations_data(stations):
    allData = []
    tempList = []
    for station in stations:
        tempList = load_station_data(station)
        allData.append(tempList)            
    return allData
###
# Input a list[] of stations from '*.txt'
# Return a "two-dimensional list[a][b]"
# a refer to 'station'
# b refer to 'dates'
###   
def display_maxs(stations, dates, data, start_date, end_date):
    i = 0
    display_stations(stations, 'Date')
    for date in dates:              
        if date >= start_date and date <= end_date:
            print(date + '    ',end='')       # This are sample dates, which is to print the dates between start_date and end_date

            for station in stations:            
                fin = open (station+'.txt','r') # Open files of stations
                for line2 in fin:               
                    date2,temperature = line2.split()
                    if date2 == date:          # Find the data of the date in every station file that match the sample list of dates
                        i += 1
                        if i < len(stations):   # An indicator "i" and "if" to check whether the program have printed data of all stations in a single day
                            display_temp(float(temperature))
                        else:                   # If all data of a single day have been printed, turn to the next line
                            if float(temperature) == UNKNOWN_TEMP:
                                print("{:<15}".format(" ----"))
                            else:
                                print("{:<15}".format("{:5.1f}".format(float(temperature))))                            
            i = 0                               # Reset the indicator
###
# 1.Print "column0_name" and stations names by using the function: display_stations(stations, column0_name).
# 2.Use load_dates(stations) to print every data line.
# 3.Divided into every line, print dates between start_date and end_date first, by using function: load_dates(stations).
# 4.Check every station file and find the temperature of the dates matched the results of step 3.
# 5.If all temperature in a day have been printed, turn to the next line.
###
def temperature_diffs(data, dates, stations, station1, station2,
start_date, end_date):
    diff = 0.0
    diffsList = []
    for date in dates:                                                                                   
        if date >= start_date and date <=end_date:
            fin1 = open (station1+'.txt','r')
            fin2 = open (station2+'.txt','r')                   # Open two files
            for line2 in fin1:
                dateS1, temp1 = line2.split()                   ###
                if dateS1 == date:                              #
                    for line3 in fin2:                          # To find the data in the same day
                        dateS2, temp2 = line3.split()           #
                        if dateS1 == dateS2:                    ###
                            if float(temp1) == UNKNOWN_TEMP or float(temp2) == UNKNOWN_TEMP:
                                diffsList.append((date, UNKNOWN_TEMP))
                            else:
                                diff = float(temp1) - float(temp2)  # Calculate the differences
                                diffsList.append((date, diff))
    return diffsList
                        
def display_diffs(diffs, station1, station2):
    print ('Temperature differences between ' + station1 + ' and ' + station2 + '\n')
    print ('Date      Temperature Differences')
    i = 0                                                   ###
    for diff in diffs:                                      # Get data from temperature_diffs()
        date1, temp1 = diff                                 # Seperate date and temperature 
        for k in range(len(diff)):                          ###
            if k < len(diff)-1:                             #
                print (format(date1),end='')                # If print date, a new line is not needed
            else:                                           # 
                if float('%.1f'%temp1) == UNKNOWN_TEMP:     # To check if there is an unknown temperature
                    print ("{:>7}".format('----'))          #
                else:                                       # print the difference and turn to a new line
                    print ("{:>7}".format('%.1f'%temp1))    #
        i = 0                                               ###


def yearly_averages(dates, data, start_year, end_year):
    
    annualAvgTemp = []
    allAvgTemp = []
    j = 0
    tempSum = 0.0
    start = 0
    end = 0
    
    years, indicies = get_year_info(dates, start_year, end_year)
                                                                ###
    for s in range(len(data)):                                  # Every station(the last to loop)
        for i in indicies:                                      ###
            if start == 0 or start > i:                         #
                start = int(i)                                  # Every year(the first to loop)
                continue                                        # Construct the index of start and end
            if start != 0 and end == 0:                         # of a single year
                end = int(i)                                    #
            if start != 0 and end != 0:                         ###                   
                for y in range(start,end):                      #             
                    if float(data[s][y]) != UNKNOWN_TEMP:       # 
                        tempSum += float(data[s][y])            # Calculate the average temparatures
                        j += 1                                  #
                yAvgT = tempSum / j                             #
                annualAvgTemp.append(yAvgT)                     ### 
                start = end                                     #
                end = 0                                         # Reset arguments for next time of loop
                tempSum = 0                                     # 
                j = 0                                           ###
        allAvgTemp.append(annualAvgTemp)
        annualAvgTemp = []

    return years, allAvgTemp

            
def display_yearly_averages(years, averages, stations):
    i = 0
    s = 0                                                                               
    display_stations(stations, 'Year')                  # Print the first line
    for year in years:                                  # 
        print(year + '        ',end='')                 # For every line, print the years                 
        if s < len(years):            
            for k in range(len(stations)):              # For every stations, print the average temperature
                i += 1
                if i < len(stations):                   # To check if a new line is needed
                    display_temp(float(averages[k][s]))
                else:
                    print("{:<15}".format("{:5.1f}".format(float(averages[k][s]))))
            s += 1
            i = 0
            
def interact():
    cmd = []
    print ('Welcome to BOM Data','\n')
    stations_file = input ('Please enter the name of the Stations file: ')
    print ('')
    stations = load_stations(stations_file)
    dates = load_dates(stations)
    data = load_all_stations_data(stations)
    while True:                         # Ensure that user can still input other commands after the first input 
        c1 = input ('Command: ')
        cmd = c1.split()
        if cmd[0] == 'dm':
            print ('')
            display_maxs(stations, dates, data, cmd[1], cmd[2])
            print ('')
        elif cmd[0] == 'dd':
            print ('')
            diffs = temperature_diffs(data, dates, stations, cmd[1], cmd[2],
cmd[3],cmd[4])
            display_diffs(diffs, cmd[1],cmd[2])
            print ('')
        elif cmd[0] == 'ya':
            print ('')
            years, averages = yearly_averages(dates, data, cmd[1], cmd[2])
            display_yearly_averages(years, averages, stations)
            print ('')
        elif cmd[0] == 'q':
            exit()
        else:
            print ('Unknown command: ' + cmd[0] + '\n')
     
##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()
