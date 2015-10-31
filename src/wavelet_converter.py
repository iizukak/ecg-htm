import sys
import csv
import datetime
import os
import pywt
from collections import deque

# setting for wavelet conversion
WAVELET_SEGMENT_SIZE = 20
WAVELET_DB = "db2"
WAVELET_FREQUENCY = 1

SMOOTHING_SIZE = 20

# setting CSV data directory
DATA_DIR = "data/"

# setting file
import argparse
parser = argparse.ArgumentParser(description = "")
parser.add_argument('--target', required=True)
args = parser.parse_args()
t = args.target
targetPath = DATA_DIR + t + ".csv"
outputPath = DATA_DIR + t + "_converted.csv"

# setting input file
targetFile = open(targetPath, "r")
csvReader = csv.reader(targetFile)
print("DEBUG: TARGET FILE PATH:", targetPath)

# setting output file
outputFile = open(outputPath, "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT FILE PATH:", outputPath)

# make initial segment
currentSegment = deque(maxlen = WAVELET_SEGMENT_SIZE)
waveletList = []
for i in range(WAVELET_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(value)

smoothingSegment = deque(maxlen=SMOOTHING_SIZE)

iteration_size = ((sum(1 for line in open(targetPath, "r")) - WAVELET_SEGMENT_SIZE)) - 1
print("DEBUG: LOOP_NUM:", iteration_size)
for i in range(iteration_size):
    date, value = csvReader.next()
    currentSegment.append(value)

    # cA, cD = pywt.dwt(sorted(currentSegment), WAVELET_DB)
    cA, cD = pywt.dwt(currentSegment, WAVELET_DB)

    smoothingSegment.append(cA[WAVELET_FREQUENCY])
    smoothedValue = sum(smoothingSegment) / len(smoothingSegment)

    waveletList.append([date, int(value), smoothedValue])

s = sum(map(lambda l:l[2], waveletList))
offset = 500 - (s / len(waveletList))
print("DEBUG: OFFFSET:", offset)
waveletList  = map(lambda l: [l[0], l[1], (l[2] + offset)], waveletList)

# write csv headers
csvWriter.writerow(["timestamp", "raw_value", "wavelet_value"])
csvWriter.writerow(["datetime", "int", "float"])
csvWriter.writerow(["T", "", ""])


csvWriter.writerows(waveletList)

targetFile.close()
outputFile.close()
