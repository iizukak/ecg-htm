"""
A simple client to create a CLA anomaly detection model for coordinate data.
"""

import csv
import datetime
import sys
import numpy

from nupic.frameworks.opf.modelfactory import ModelFactory

import model_params.model_params_coordinate as model_params



DEFAULT_DATA_PATH = "data/healthy_person1_fft_converted.csv"
DEFAULT_OUTPUT_PATH = "data/anomaly_scores.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
RADIUS = 5 # Change this value to valid

'''
def addTimeEncoders(params):
  params["modelParams"]["sensorParams"]["encoders"]["timestamp_timeOfDay"] = {
    "fieldname": u"timestamp",
    "name": u"timestamp_timeOfDay",
    "timeOfDay": (51, 9.5),
    "type": "DateEncoder"
  }
  return params
'''


def createModel(verbose):
  params = model_params.MODEL_PARAMS
  if verbose:
    print "Model parameters:"
    print params
  model = ModelFactory.create(params)
  model.enableInference({"predictedField": "vector"})
  return model


def runCoordinateAnomaly(dataPath, outputPath,
                         verbose=True):

  model = createModel(verbose)

  with open (dataPath) as fin:
    reader = csv.reader(fin)
    csvWriter = csv.writer(open(outputPath,"wb"))
    csvWriter.writerow(["timestamp",
                       "anomaly_score",])

    reader.next()
    reader.next()
    reader.next()

    # it's dummy value. use valid value
    timestamp = datetime.datetime.strptime("2015-10-17 21:05:57.033917", DATE_FORMAT)
    for _, record in enumerate(reader, start=1):
      '''
      timestamp = datetime.datetime.fromtimestamp(int(record[1]) / 1e3)
      '''
      print(record)
      values = numpy.array(map(lambda x:int(x), record))
      # TODO: THIS IS DEBUG DUMMY VALUES
      values = numpy.array(range(3))
      print("DEBUG RUN MODEL")
      
      timestamp = timestamp + datetime.timedelta(microseconds=10000) 

      modelInput = {
        "vector": (values, RADIUS),
        "timestamp": timestamp
      }
      
      result = model.run(modelInput)
      anomalyScore = result.inferences["anomalyScore"]

      csvWriter.writerow([anomalyScore])

      if verbose:
        print "[{0}] - Anomaly score: {1}.".format(timestamp, anomalyScore)

  print "Anomaly scores have been written to {0}".format(outputPath)


if __name__ == "__main__":
  dataPath = DEFAULT_DATA_PATH
  outputPath = DEFAULT_OUTPUT_PATH

  if len(sys.argv) > 1:
    dataPath = sys.argv[1]

  if len(sys.argv) > 2:
    outputPath = sys.argv[2]

  runCoordinateAnomaly(dataPath, outputPath)
