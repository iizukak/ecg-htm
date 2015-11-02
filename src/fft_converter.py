import sys
import csv
import datetime
import os
import pywt
import numpy
from collections import deque

# setting for fft conversion
FFT_SEGMENT_SIZE = 250

# setting CSV data directory
DATA_DIR = "data/"

# setting file
import argparse
parser = argparse.ArgumentParser(description = "")
parser.add_argument('--target', required=True)
args = parser.parse_args()
t = args.target
targetPath = DATA_DIR + t + ".csv"
outputPath = DATA_DIR + t + "_fft_converted.csv"

# setting input file
targetFile = open(targetPath, "r")
csvReader = csv.reader(targetFile)
print("DEBUG: TARGET FILE PATH:", targetPath)

outputFile = open(outputPath, "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT FILE PATH:", outputPath)

currentSegment = deque(maxlen = FFT_SEGMENT_SIZE)

# make initial segment
for i in range(FFT_SEGMENT_SIZE):
    date, value = csvReader.next()
    currentSegment.append(int(value))
print(currentSegment)

# write csv headers
'''
csvWriter.writerow(["timestamp", "raw_value", "wavelet_value"])
csvWriter.writerow(["datetime", "int", "float"])
csvWriter.writerow(["T", "", ""])
'''

hamm = numpy.hamming(FFT_SEGMENT_SIZE)
for row in csvReader:
    date, value = row[0], int(row[1])
    currentSegment.append(value)
    window = currentSegment * hamm
    # FFTValue = numpy.log(numpy.abs(numpy.fft.fft(window).real))
    # FFTValue = numpy.abs(numpy.fft.fft(window).real)
    # FFTValue = pywt.dwt(currentSegment ,"db1")[0]
    FFTValue = numpy.log([numpy.sqrt(c.real ** 2 + c.imag ** 2) for c in numpy.fft.fft(window)][0:(FFT_SEGMENT_SIZE/2)])
    csvWriter.writerow(FFTValue)
    # csvWriter.writerow((date, value, FFTValue))
