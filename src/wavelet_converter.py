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

# Skip Header File
csvReader.next()
csvReader.next()
csvReader.next()

# make initial segment
currentSegment = deque(maxlen = WAVELET_SEGMENT_SIZE)
for i in range(WAVELET_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(value)

cA, cD = pywt.dwt(currentSegment, WAVELET_DB)

print("DEBUG: SAMPLE CONVERTED ROW: ", cA)
print("DEBUG: SAMPLE CONVERTED ROW SIZE:" , len(cA))

waveletList = []
waveletList.append([date, cA[1]])

iteration_size = ((sum(1 for line in open(targetPath, "r")) \
                    - WAVELET_SEGMENT_SIZE) \
                    / WAVELET_UPDATE_SIZE) - 4

print("DEBUG: LOOP_NUM:", iteration_size)
for i in range(iteration_size):
    for j in range(WAVELET_UPDATE_SIZE):
        date, value = csvReader.next()
        currentSegment.append(value)

    cA, cD = pywt.dwt(sorted(currentSegment), WAVELET_DB)
    # csvWriter.writerow(cA)
    waveletList.append([date, cA[1]])

s = sum(map(lambda l:l[1], waveletList))
offset = 500 - (s / len(waveletList))
print("DEBUG: OFFFSET:", offset)
waveletList  = map(lambda l: [l[0] ,(l[1] + offset)], waveletList)

csvWriter.writerows(waveletList)

targetFile.close()
outputFile.close()
