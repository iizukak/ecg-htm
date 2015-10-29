import csv
import datetime
import os
import pywt
from collections import deque

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

WAVELET_SEGMENT_SIZE = 250
WAVELET_UPDATE_SIZE = 1
WAVELET_DB = "db1"
WAVELET_MODE = "sp1"
TARGET_FILE = "healthy_person1"
DATA_DIR = "data/"

# setting input file
inputFile = open(DATA_DIR + TARGET_FILE + ".csv", "r")
csvReader = csv.reader(inputFile)
print("DEBUG: INPUT_FILE:", inputFile)

# setting output file
outputFile = open(DATA_DIR + TARGET_FILE + "_converted.csv", "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT_FILE:", outputFile)

csvReader.next()
csvReader.next()
csvReader.next()

# make initial segment
currentSegment = deque(maxlen = WAVELET_SEGMENT_SIZE)
for i in range(WAVELET_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(value)

cA, cD = pywt.dwt(currentSegment, WAVELET_DB, mode=WAVELET_MODE)

print(cA)
print(len(cA))

csvWriter.writerow(cA)

iteration_size = ((sum(1 for line in open(DATA_DIR + TARGET_FILE + ".csv", "r")) \
                    - WAVELET_SEGMENT_SIZE) \
                    / WAVELET_UPDATE_SIZE) - 4

print(iteration_size)
for i in range(iteration_size):
    for j in range(WAVELET_UPDATE_SIZE):
        date, value = csvReader.next()
        currentSegment.append(value)

    cA, cD = pywt.dwt(sorted(currentSegment), WAVELET_DB, mode=WAVELET_MODE)
    csvWriter.writerow(cA)

inputFile.close()
outputFile.close()
