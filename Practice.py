
import csv
import datetime

import random
currenttime = datetime.datetime.now()
currenttime = str(currenttime)
currenttime_array = currenttime.split(' ')
date = currenttime_array[0]
time = currenttime_array[1][:8]
filename = time
filename += '_'
filename += date
filename += '.csv'

print('[INFO] Name of File created : ' + filename)

filename = os.path.join('/home/udooer/Desktop/aetdrone/Image-Processing-in-UAV/new_output', filename)

with open(filename, 'w+') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Date", "Time", "PM1", "PM2.5", "PM10", "NO2", "CO2", "CO", "Humidity", "Temperature"])

# file1 = open("/gpio/pin25/value","r")
# t_old = file1.read()
# t_old = int(t_old)

while True:

    currenttime = datetime.datetime.now()
    currenttime = str(currenttime)
    currenttime_array = currenttime.split(' ')
    date = currenttime_array[0]
    time = currenttime_array[1][:8]

    PM1 = range(15,40,1)
    PM2_5 = range(30,70,1)
    PM10 = range(30,80,1)
    NO2 = range()
    print('[INFO] Date ' + date + '  ,Time ' + time + '  ,PM1 ' + str(PM1) + '  ,PM2_5 ' + str(PM2_5) + '  ,PM10 ' + str(
        PM10) + '  ,NO2 ' + str(NO2) + '  ,CO2 ' + str(CO2) + '  ,CO ' + str(CO) + '  ,$
    with open(filename, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
    csv_writer.writerow([date, time, PM1, PM2_5, PM10, NO2, CO2, CO, humi, temp])
