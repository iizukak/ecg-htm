import sys
import csv
import datetime
import os

# setting CSV data directory
DATA_DIR = "data/"

# setting file
import argparse
parser = argparse.ArgumentParser(description = "Lovelive MaU Manual Generator")
parser.add_argument('--target', required=True)
args = parser.parse_args()
t = args.target
targetPath = DATA_DIR + t + ".csv"
outputPath = DATA_DIR + t + "_averaged.csv"

# setting input file
targetFile = open(targetPath, "r")
csvReader = csv.reader(targetFile)
print("DEBUG: TARGET FILE PATH:", targetPath)

# setting input file
averageFile = open(targetPath, "r")
averageReader = csv.reader(averageFile)
print("DEBUG: TARGET FILE PATH:", averageReader)

# setting output file
outputFile = open(outputPath, "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT FILE PATH:", outputPath)

# Skip Header File
csvReader.next()
csvReader.next()
csvReader.next()

averageReader.next()
averageReader.next()
averageReader.next()

tmpList = []
for d, v in averageReader:
    tmpList.append(int(v))

print(sum(tmpList) / len(tmpList))
offset = 500 - (sum(tmpList) / len(tmpList))

targetFile.close()
outputFile.close()
averageFile.close()
