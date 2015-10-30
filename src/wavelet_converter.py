import sys
import csv
import datetime
import os
import pywt
from collections import deque

# setting for wavelet conversion
WAVELET_SEGMENT_SIZE = 200
WAVELET_UPDATE_SIZE = 1
WAVELET_DB = "db2"

SMOOTHING_SIZE = 100

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
print("DEBUG: TARGET FILE PATH:", targetPath)

# setting output file
outputFile = open(outputPath, "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT FILE PATH:", outputPath)

# make initial segment
currentSegment = deque(maxlen = WAVELET_SEGMENT_SIZE)
for i in range(WAVELET_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(value)

cA, cD = pywt.dwt(currentSegment, WAVELET_DB)

print("DEBUG: SAMPLE CONVERTED ROW: ", cA)
print("DEBUG: SAMPLE CONVERTED ROW SIZE:" , len(cA))

waveletList = []
waveletList.append([date, int(value), cA[1]])

iteration_size = ((sum(1 for line in open(targetPath, "r")) \
                    - WAVELET_SEGMENT_SIZE) \
                    / WAVELET_UPDATE_SIZE) - 1

print("DEBUG: LOOP_NUM:", iteration_size)
smoothingSegment = deque([500.0] * SMOOTHING_SIZE, maxlen=SMOOTHING_SIZE)
for i in range(iteration_size):
    for j in range(WAVELET_UPDATE_SIZE):
        date, value = csvReader.next()
        currentSegment.append(value)

    cA, cD = pywt.dwt(sorted(currentSegment), WAVELET_DB)

    # do smoothing
    smoothingSegment.append(cA[1])
    smoothedValue = sum(smoothingSegment) / SMOOTHING_SIZE

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
