import csv
import datetime
import os
import pywt
import numpy as np
from collections import deque

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

FFT_SEGMENT_SIZE = 256
FFT_UPDATE_SIZE = 1

TARGET_FILE = "healthy_person1"
DATA_DIR = "data/"

# setting input file
inputFile = open(DATA_DIR + TARGET_FILE + ".csv", "r")
csvReader = csv.reader(inputFile)
print("DEBUG: INPUT_FILE:", inputFile)

# setting output file
outputFile = open(DATA_DIR + TARGET_FILE + "_converted_fft.csv", "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT_FILE:", outputFile)

csvReader.next()
csvReader.next()
csvReader.next()

# make initial segment
currentSegment = deque(maxlen = FFT_SEGMENT_SIZE)
for i in range(FFT_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(value)

cA = np.fft.hfft(currentSegment)

print(cA)
print(len(cA))

csvWriter.writerow(cA)

iteration_size = ((sum(1 for line in open(DATA_DIR + TARGET_FILE + ".csv", "r")) \
                    - FFT_SEGMENT_SIZE) \
                    / FFT_UPDATE_SIZE) - 4

print(iteration_size)
for i in range(iteration_size):
    for j in range(FFT_UPDATE_SIZE):
        date, value = csvReader.next()
        currentSegment.append(value)

    cA = np.fft.hfft(sorted(currentSegment))
    csvWriter.writerow(cA)

inputFile.close()
outputFile.close()
