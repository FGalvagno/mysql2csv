#!/usr/bin/env python

#Built-in modules
import os
import warnings
import datetime
from datetime import timedelta
#Third-party modules
import pandas as pd
import mysql.connector as connection


warnings.filterwarnings('ignore')

#Global vars
location = ""
fromYear = 2016
toYear = 2016 
database = ""
user = ""
host = "" #172.17.0.2
passwd = ""

def lastDate(year, month):
    """ Calculates the last day of a month in Y-m-d format

        Parameters
        ----------
        year : int
        month : int
            month and year to get last date    

        Returns
        ----------
        date : string
            string that represents the last day of a month in Y-m-d format

    """
    
    if month == 12:
        last_date = datetime.date(year, month, 31)
    else:
        last_date = datetime.date(year, month + 1, 1) + timedelta(days=-1)
    
    return last_date.strftime("%Y-%m-%d")

def setup():
    """ Initialize the script, asking for DB credentials, checking for basic "export" folder and selecting proper
        location of AWS
    """
    if not os.path.exists('export'):
        os.makedirs('export')
    
    #f = open("locations.txt", "r")
    ## TODO: FINISH LOCATION SELECTOR
    
    '''
    with open('locations.txt') as f:
        for i, line in enumerate(f, 1):
            print ("{0}: {1}".format(i+1,line))
    
    location = f.readline(int(input("Index of location: "))+1)
    print("Location selected: " + location)
    '''
    location = "PIL-CBA-AR"
    host = input("Host (localhost): " or "localhost" )
    database = input("MySQL DB name (mtrackreport): " or "mtrackreport")
    user = input("DB user: " or "root")
    passwd = input("Password (leave blank for none): ")
    fromYear = int(input("From year (2017): ") or "2017") 
    toYear = int(input("To year (2023): ") or "2023")+ 1

    
    

def checkDirectory(year):
    """ Checks for year folder in ./export.
        If said folder doesn't exists, this function will create a new one.
    
        Parameters
        ----------
        year : int
            name of the folder to store data
    """
    if not os.path.exists('./export/' + str(year)):
        os.makedirs('./export/' + str(year))

def collect(year, month):
    """ Collects data from MySQL server, within specified date

        Parameters
        ----------
        year : int
        month : int
            date of data to be retrieved

        Returns
        -------
        df : pandas dataframe
            results from query
    """
    query = "SELECT * FROM historial WHERE timestamp BETWEEN '" + str(year) + "-" + str(month) + "-01 00:00:00' AND '" + lastDate(year, month) + " 23:59:00';"
    print(query)
    df = pd.read_sql(query, mydb) 
    return df

def toCSV(year, month, df):
    """ Exports pandas df into a .csv file. This function also checks if the df param is empty

        Parameters
        ----------
        year : int
        month : int
            date of data
        df : pandas dataframe
            data to be exported to csv
        
    """
    if df.empty:
        print("Database has no data on " + str(month) + "-" + str(year) + " omiting...")
        return
    else:
        print("Saving " + "{:02d}".format(month) + "-" + str(year))
        df.to_csv("export/" + str(year) + "/" + str(year) + "{:02d}".format(month) + "-AR-CBA-PILAR.csv", index=False)
    return

setup()

print("Connecting")

try: 
    mydb = connection.connect(host, database, user, passwd) #connecting to DB
except Exception as e:
    print("Connection failed")
    print(e)


for year in range(fromYear, toYear): #iteration over dates/month
    checkDirectory(year)
    for month in range(1,13):
        toCSV(year, month, collect(year, month))


mydb.close()