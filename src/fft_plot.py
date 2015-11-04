#coding: UTF-8
import csv
import math
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import animation
 
# setting CSV data directory
DATA_DIR = "data/"

# setting file
import argparse
parser = argparse.ArgumentParser(description = "")
parser.add_argument('--target', required=True)
args = parser.parse_args()
t = args.target
targetPath = DATA_DIR + t + ".csv"

# setting input file
targetFile = open(targetPath, "r")
csvReader = csv.reader(targetFile)
print("DEBUG: TARGET FILE PATH:", targetPath)

# skip header rows
csvReader.next()
csvReader.next()
testrow = csvReader.next()

print("MAX_VALUE",max(testrow))
# plt.plot(testrow[1:])
# plt.show()

fig, ax = plt.subplots()
plt.title("FFT-converted ECG")
plt.xlabel("frequency index(not Hz)")
plt.ylabel("value")

line, = ax.plot(testrow)

def update(data):
    line.set_ydata(data)
    return line,

def data_gen():
    for row in csvReader:
        yield row

ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
plt.show()
