import sys
import csv
import datetime
import os
import pywt
from collections import deque

# setting for wavelet conversion
WAVELET_SEGMENT_SIZE = 256
WAVELET_UPDATE_SIZE = 1
WAVELET_DB = "db2"
WAVELET_MODE = "sp1"

# setting CSV data directory
DATA_DIR = "data/"

# setting file
import argparse
parser = argparse.ArgumentParser(description = "Lovelive MaU Manual Generator")
parser.add_argument('--target', required=True)
args = parser.parse_args()
t = args.target
targetPath = DATA_DIR + t + ".csv"
outputPath = DATA_DIR + t + "_converted.csv"

# setting input file
targetFile = open(targetPath, "r")
csvReader = csv.reader(targetFile)
print("DEBUG: TARGET FILE PATH:", targetFile)

# setting output file
outputFile = open(outputPath, "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT FILE PATH:", outputFile)

# Skip Header File
csvReader.next()
csvReader.next()
csvReader.next()

# make initial segment
currentSegment = deque(maxlen = WAVELET_SEGMENT_SIZE)
for i in range(WAVELET_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(value)

cA, cD = pywt.dwt(currentSegment, WAVELET_DB, mode=WAVELET_MODE)

print("DEBUG: SAMPLE CONVERTED ROW: ", cA)
print("DEBUG: SAMPLE CONVERTED ROW SIZE:" , len(cA))

csvWriter.writerow(cA)

iteration_size = ((sum(1 for line in open(targetPath, "r")) \
                    - WAVELET_SEGMENT_SIZE) \
                    / WAVELET_UPDATE_SIZE) - 4

print("DEBUG: LOOP_NUM:", iteration_size)
for i in range(iteration_size):
    for j in range(WAVELET_UPDATE_SIZE):
        date, value = csvReader.next()
        currentSegment.append(value)

    cA, cD = pywt.dwt(sorted(currentSegment), WAVELET_DB, mode=WAVELET_MODE)
    csvWriter.writerow(cA)

targetFile.close()
outputFile.close()
