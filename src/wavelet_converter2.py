import pywt
import numpy
import csv

# setting CSV data directory
DATA_DIR = "data/"

# setting file
import argparse
parser = argparse.ArgumentParser(description = "")
parser.add_argument('--target', required=True)
args = parser.parse_args()
t = args.target
targetPath = DATA_DIR + t + ".csv"
outputPath = DATA_DIR + t + "_wavelet.csv"

# setting input file
targetFile = open(targetPath, "r")
csvReader = csv.reader(targetFile)
print("DEBUG: TARGET FILE PATH:", targetPath)

outputFile = open(outputPath, "w")
csvWriter = csv.writer(outputFile, lineterminator='\n')
print("DEBUG: OUTPUT FILE PATH:", outputPath)

dateList = []
waveletList = []
rawList = []
counter = 0
for row in csvReader:
    date, value = row[0], int(row[1])
    dateList.append(date)
    waveletList.append(value)

    # after wavelet transform, value downsize to half size
    if counter % 2 == 0:
        rawList.append(value)
    counter += 1

waveletList = pywt.dwt(waveletList, "db3")[0]
s = sum(waveletList)
offset = 500 - (s / len(waveletList))
print("DEBUG: OFFFSET:", offset)
waveletList  = waveletList + offset


outList = []
for d, r, w in zip(dateList, rawList, waveletList):
    print(w - r)
    outList.append((d, r, w))

# write csv headers
csvWriter.writerow(["timestamp", "raw_value", "wavelet_value"])
csvWriter.writerow(["datetime", "int", "float"])
csvWriter.writerow(["T", "", ""])

# write main data
csvWriter.writerows(outList)

targetFile.close()
outputFile.close()
