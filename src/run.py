#!/usr/bin/env python2.7
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.    Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.    If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Anomaly Tutorial.)
"""
import importlib
import sys
import csv
import datetime
import os

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

import nupic_anomaly_output


DESCRIPTION = (
    "Starts a NuPIC model from the model params returned by the swarm\n"
    "and pushes each line of input from the gym into the model. Results\n"
    "are written to an output file (default) or plotted dynamically if\n"
    "the --plot option is specified.\n"
)
#CSV_NAME = "anomaly"
CSV_NAME = "normal_converted"
DATA_DIR = "data"
MODEL_DIR = os.getcwd() + "/model"
# 2015-10-14 17:21:33.058979
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def createModel(modelParams):
    """
    Given a model params dictionary, create a CLA Model. Automatically enables
    inference for kw_energy_consumption.
    :param modelParams: Model params dict
    :return: OPF Model object
    """
    model = ModelFactory.create(modelParams)
    model.enableInference({"predictedField": "wavelet_value"})
    return model



def getModelParamsFromName(gymName):
    """
    Given a gym name, assumes a matching model params python module exists within
    the model_params directory and attempts to import it.
    :param gymName: Gym name, used to guess the model params module name.
    :return: OPF Model params dictionary
    """
    importName = "model_params.model_params_normal"
    print "Importing model params from %s" % importName
    try:
        importedModelParams = importlib.import_module(importName).MODEL_PARAMS
    except ImportError:
        raise Exception("No model params exist")
    print importedModelParams
    return importedModelParams



def runIoThroughNupic(inputData, model, gymName, plot, load):
    """
    Handles looping over the input data and passing each row into the given model
    object, as well as extracting the result object and passing it into an output
    handler.
    :param inputData: file path to input data CSV
    :param model: OPF Model object
    :param gymName: Gym name, used for output handler naming
    :param plot: Whether to use matplotlib or not. If false, uses file output.
    """
    inputFile = open(inputData, "rb")
    csvReader = csv.reader(inputFile)
    # skip header rows
    csvReader.next()
    csvReader.next()
    csvReader.next()

    shifter = InferenceShifter()
    if plot:
        output = nupic_anomaly_output.NuPICPlotOutput(gymName)
    else:
        output = nupic_anomaly_output.NuPICFileOutput(gymName)

    counter = 0

    # using dummy time to debug
    timestamp = datetime.datetime.strptime(csvReader.next()[0], DATE_FORMAT)
    print("DEBUG_PRINT: initiali time", timestamp)

    for row in csvReader:
        counter += 1

        if (counter % 100 == 0):
            print "Read %i lines..." % counter

        timestamp = timestamp + datetime.timedelta(microseconds=10000)
        #timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
        consumption = float(row[2])
        result = model.run({
            "timestamp": timestamp,
            "wavelet_value": consumption
        })

        if plot:
            result = shifter.shift(result)

        prediction = result.inferences["multiStepBestPredictions"][1]
        anomalyScore = result.inferences["anomalyScore"]

        # plot half of the data for speed up
        if (counter % 3 != 0):
            continue

        output.write(timestamp, consumption, prediction, anomalyScore)
        
    if not load:
        print("saving model for MODEL_DIR")
        model.save(MODEL_DIR)
    inputFile.close()
    output.close()

    return model


def runModel(gymName, plot=False, load=False):
    """
    Assumes the gynName corresponds to both a like-named model_params file in the
    model_params directory, and that the data exists in a like-named CSV file in
    the current directory.
    :param gymName: Important for finding model params and input CSV file
    :param plot: Plot in matplotlib? Don't use this unless matplotlib is
    installed.
    """

    if load:
        print "Loading model from %s..." % MODEL_DIR
        model = ModelFactory.loadFromCheckpoint(MODEL_DIR)
        model.disableLearning()
        inputData = "%s/%s.csv" % (DATA_DIR, gymName)
        runIoThroughNupic(inputData, model, gymName, plot, load)
    else:
        print "Creating model from %s..." % gymName
        model = createModel(getModelParamsFromName(gymName))

        # read learning file list from learning_list.txt
        f = open(DATA_DIR + "/learning_list.txt")
        files = f.readlines()
        f.close()
        for file in files:
            model.resetSequenceStates()
            filename = file.strip()
            print(filename)
            inputData = "%s/%s.csv" % (DATA_DIR, filename)
            model = runIoThroughNupic(inputData, model, filename, plot, load)

if __name__ == "__main__":
    print DESCRIPTION
    plot = False
    load = False
    args = sys.argv[1:]
    for arg in args:
        print(arg)
        if arg == "--plot":
            plot = True
        elif arg == "--load":
            load = True

    runModel(CSV_NAME, plot=plot, load=load)
