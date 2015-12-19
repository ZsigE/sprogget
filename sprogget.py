"""Sprogget

Baby name analysis for (nearly) all live births in England and Wales"""

import csv
import argparse
import os

# Constants
RESOURCE_DIR = "res"
GIRL = 1
BOY = 2

def get_baby_data():
    """Pull in the baby name data from the resource CSV files"""
    
    baby_data = {}
    for filename in os.listdir(RESOURCE_DIR):
        if not filename.endswith(".csv"):
            # Not a CSV, don't bother
            continue
        path = os.path.join(RESOURCE_DIR, filename)
        filename_no_ex = filename.rpartition(".")[0]
        
        year = int(filename[:4])
        if year not in baby_data:
            baby_data[year] = {}
            
        sex = GIRL if filename_no_ex.endswith("g") else BOY
        if sex not in baby_data[year]:
            baby_data[year][sex] = {}

        with open(path, "r") as csvfile:
            reader = csv.reader(csvfile)
            for line in reader:
                name = line[0].strip()
                count = int(line[1].strip())
                baby_data[year][sex][name] = count
                
    return baby_data
        

def sprogget():
    """Load in the data and do some awesome analysis"""
    
    parser = argparse.ArgumentParser(description="Baby name analysis")
    parser.add_argument("name", action="store", nargs="*")
    args = parser.parse_args()
    
    baby_data = get_baby_data()

    name_year_data = {}
    for name in args.name:
        name = name.upper()
        year_data = {}
        name_year_data[name] = year_data
        for year in sorted(baby_data.keys()):
            year_data[year] = 0
            for sex in baby_data[year]:
                if name in baby_data[year][sex]:
                    year_data[year] += baby_data[year][sex][name]
    
    print "Year," + ",".join(["Babies called {0}".format(n) for n in 
                                                 sorted(name_year_data.keys())])    
    for year in sorted(baby_data.keys()): 
        print "{0},".format(year) + ",".join([str(name_year_data[n][year]) for 
                                            n in sorted(name_year_data.keys())])
        
if __name__ == "__main__":
    sprogget()