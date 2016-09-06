import csv
from datetime import datetime
import time

con1check=0
con2check=0
con3check=0
fmt = '%d/%m/%Y %H:%M:%S'
max_humid = 0
from collections import OrderedDict

#Reference :
#http://stackoverflow.com/questions/20414562/python-joining-csv-files-where-key-is-first-column-value
#http://stackoverflow.com/questions/3096953/difference-between-two-time-intervals-in-python

#this will read excel file containing humidity data
with open('export_cavelab.10.humidity_2016-08-04.csv') as f:
    r = csv.reader(f, delimiter=',')
    dict2 = {row[0]: row[1:] for row in r}
    
#this will read excel file containing temperature data
with open('export_cavelab.10.temperature_2016-08-04.csv') as f:
    r = csv.reader(f, delimiter=',')
    dict1 = OrderedDict((row[0], row[1:]) for row in r)
    
result = OrderedDict()
for d in (dict1, dict2):
    for tag, value in d.iteritems():
       
        result.setdefault(tag, []).extend(value)
        
#This will merge both dictionaries
with open('ab_combined.csv', 'wb') as f:
    w = csv.writer(f)
    for tag, value in result.iteritems():
        w.writerow([tag] + value)
counter = 0
#this will read new CSV file containing both temperature and humidity data with respect to Time stamps
with open('ab_combined.csv', 'rb') as csvfile1:
    spamreader1 = csv.reader(csvfile1, delimiter=';', quotechar='|')
    for row in spamreader1:
        if (counter > 0):
            newrow = ', '.join(row)
            index = newrow.find(',')
            index2 = newrow.find(',',index+1)
            humiditycheck = float(newrow[index2 +1 : len(newrow)])
            #this will find maximum humidity value for calculating relative humidity
            if humiditycheck > max_humid:
                max_humid = humiditycheck
                #print max_humid
        counter = counter +1
counter = 0
with open('ab_combined.csv', 'rb') as csvfile1:
    spamreader1 = csv.reader(csvfile1, delimiter=';', quotechar='|')
    for row in spamreader1:
        if (counter > 0):
            newrow = ', '.join(row)
            index = newrow.find(',')
            index2 = newrow.find(',',index+1)
            time = newrow[0:index]
            #this will extract DateTime in python standard form
            time = datetime.strptime(time, fmt)
            #Temperature Value
            temperature = float(newrow[index+1 : index2])
            #humidity value
            humidity = float(newrow[index2 +1 : len(newrow)])

            #Checking condition for first disease
            if (con1check == 0):
                if (humidity > 90):
                    humidity_timestamp1=time
                    con1check = 1
            elif (con1check == 1):
                if (humidity < 90):
                    humidity_timestamp2=time
                    v1 = ((humidity_timestamp2 - humidity_timestamp1).days * 24 * 60) + ((humidity_timestamp2 - humidity_timestamp1).seconds)
                    print humidity_timestamp1
                    print humidity_timestamp2
                    print "disease 1",v1/60,"minutes"
                    if (v1/60 > 60):
                        print "Sporulation Oidium occured at time ",humidity_timestamp1," to ",humidity_timestamp2
                    con1check = 0
            #Checking condition for 2nd disease
            if (con2check == 0):
                if ((humidity > 90) and (temperature>15 and temperature<20)):
                    temperature_timestamp1 = time
                    con2check = 1
            elif (con2check == 1):
                if ((humidity > 90) and (temperature>15 and temperature<20)) == 0:
                    temperature_timestamp2 = time
                    v2 = ((temperature_timestamp2 - temperature_timestamp1).days * 24 * 60) + ((temperature_timestamp2 - temperature_timestamp1).seconds)
                    print temperature_timestamp1
                    print temperature_timestamp2
                    print "disease 2",v2/60,"minutes"
                    if (v2 > 360):
                        print "Botrytis occured at time ",temperature_timestamp1," to ",temperature_timestamp2
                    con2check = 0
            #checking condition for 3rd disease
            if (con3check == 0):
                if ((((humidity > 90) and ((humidity / max_humid)*100)<70)) and (temperature>20)):
                    temp_hum_timestamp1 = time 
                    con2check = 1
            elif (con2check == 1):
                if ((((humidity > 90) and ((humidity / max_humid)*100)<70)) and (temperature>20)) == 0:
                    temp_hum_timestamp2 = time
                    v3 = ((temp_hum_timestamp2 - temp_hum_timestamp1).days * 24 * 60) + ((temp_hum_timestamp2 - temp_hum_timestamp1).seconds)
                    print temp_hum_timestamp1
                    print temp_hum_timestamp2
                    print "disease 3",v3/60,"minutes"
                    if (v3/60 > 900):
                        print"Risque developpement oidium occured at :",temp_hum_timestamp1," to ",temp_hum_timestamp2
                    con3check = 0    
        counter = counter +1
print "finished"
                
            
            
