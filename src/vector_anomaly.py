"""
A simple client to create a CLA anomaly detection model for coordinate data.
"""

import csv
import datetime
import sys
import numpy
import pprint

from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.encoders.adaptivescalar import AdaptiveScalarEncoder

import model_params.model_params_generated as model_params



DEFAULT_DATA_PATH = "data/healthy_person1_fft_converted.csv"
DEFAULT_OUTPUT_PATH = "data/anomaly_scores.csv"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

def addScalarEncoders(params, vector_length):
  '''
  ase = AdaptiveScalarEncoder(21, n=109, clipInput=True)
  params["modelParams"]["sensorParams"]["encoders"].update({
          'vector': dict(
            length = vector_length,
            encoder = ase,
            name = 'vector',
            fieldname = 'vector',
            type= 'VectorEncoder')})
  '''

  for i in range(vector_length):
    sensor_name = "f" + str(i)
    params["modelParams"]["sensorParams"]["encoders"].update({ 
        sensor_name: {
          'clipInput': True,
          'fieldname': sensor_name,
          'n': 491,
          'name': sensor_name,
          'type': 'AdaptiveScalarEncoder',
          'w': 21}
    })
  return params
    

def createModel(verbose, vector_length):
  params = model_params.MODEL_PARAMS

  # loop and add scalarencoders of n-dimension
  params = addScalarEncoders(params, vector_length)

  if verbose:
    print "Model parameters:"
    pprint.pprint(params)
  model = ModelFactory.create(params)
  model.enableInference({"predictedField": "f50"})

  return model


def runCoordinateAnomaly(dataPath, outputPath,
                         verbose=True):


  with open (dataPath) as fin:
    reader = csv.reader(fin)
    csvWriter = csv.writer(open(outputPath,"wb"))
    '''
    csvWriter.writerow(["timestamp",
                       "anomaly_score",])
    '''

    r = reader.next()
    r = reader.next()
    r = reader.next()
    r = reader.next()
    fft_length = len(r) - 1
    model = createModel(verbose, fft_length)

    # it's dummy value. use valid value
    timestamp = datetime.datetime.strptime("2015-10-17 21:05:57.033917", DATE_FORMAT)
    for i, record in enumerate(reader, start=1):
      '''
      timestamp = datetime.datetime.fromtimestamp(int(record[1]) / 1e3)
      '''
      values = list(record[1:])
      values = map(lambda x: float(x), values)
      timestamp = timestamp + datetime.timedelta(microseconds=10000) 

      modelInput = {
        "timestamp": timestamp
      }
      for i in range(fft_length):
        sensor_name = "f" + str(i)
        modelInput.update({
          sensor_name: values[i]
        })
      
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
