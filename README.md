# ECG + HTM

ECG Anomaly Detection System using HTM

## Abstruct

In this projects, We build Electrocardiogram(ECG)
anomaly detection system using HTM(NuPIC).
This system will detect Palpitation, Arrhythmia and Heart Rate anomaly.

## System Structure and Usage

There are about three parts of the projects.

* Data Collector
* FFT Converter
* Anomaly Detector

### Data Collector

It's not difficult to make your own ECG device.
If you are not interested in collecting data by yourself,
You can skip this part and use data in `data` directory.

We use

* [Arduino Pro mini](https://www.sparkfun.com/products/11114)
* [Sparkfun Ad8232](https://www.sparkfun.com/products/12650)

![device](https://cloud.githubusercontent.com/assets/478824/11051785/5fb18f74-8795-11e5-940c-7164d8b0ca75.jpg)


Sparkfun's [tutorial](https://learn.sparkfun.com/tutorials/ad8232-heart-rate-monitor-hookup-guide) is very friendly.
You can also use Sparkfun's [Github Repository](https://github.com/sparkfun/AD8232_Heart_Rate_Monitor) to get simple visualization of ECG Data. Visualization output is like this [video](https://www.youtube.com/watch?v=yTcbTTxECTU).

Next, Collect ECG Data through the script.

```
$ python src/take_data.py > data/foobar.csv
```

Collected Data have this format.

```ecg.csv
2015-10-17 21:05:10.078937,483
2015-10-17 21:05:10.094542,481
2015-10-17 21:05:10.094833,480
2015-10-17 21:05:10.094949,485
2015-10-17 21:05:10.095044,492
2015-10-17 21:05:10.110693,501
```

If you want to visualize collected data, You can use Gnuplot.

```
$ gnuplot
set datafile separator ","
plot "< head -1000 data/foobar.csv" using 2 with line
```

![2015-11-09 21 48 35](https://cloud.githubusercontent.com/assets/478824/11034054/ba0744ec-872b-11e5-8e49-d97acbe44966.png)


### FFT Converter

Before detecting anomalous part of the ECG data, 
We use a signal processing technique, FFT(Fast Fourier Transform).
FFT can be used to extract charactaristics of data sequence.
`Numpy` library contain FFT, and we use that.

See example for using FFT Converter with ECG data collected by `take_data.py`.
You can also use the preset data of the repository.
FFT converter can use like this.

```
$ python src/fft_converter.py --target healthy_person1
```

```output.csv
2015-10-17 21:05:12.685818,11.808565811567473,...,10.957521665215634
2015-10-17 21:05:12.701433,11.808734646395951,...,7.7589930598122354
...
2015-10-17 21:05:57.033917,11.821344935267192,...,8.5655396209023618
```

You can use `--target` option to specify the target file's name.
Dont's forget to remove `.csv` string from file name.


FFT Converted data are can be visualized using Gnuplot.

![2015-11-07 18 54 14](https://cloud.githubusercontent.com/assets/478824/11034302/ea8045ae-872d-11e5-98dd-4ec855fc76ab.png)

Non uniform parts are corredpond to the anomalous of ECG data.

### Anomaly Detection

We use anomaly detection using `vector_anomaly.py` Script.
You shoud use FFT Converted data.

```
$ python src/vector_anomaly.py 
```

This is the visualization of the output.

![d2378b575a8f02188069ef80a08ae6fd 1](https://cloud.githubusercontent.com/assets/478824/11034523/85169d4c-872f-11e5-8ed4-55964ef5c7f0.png)

## Data

This repository include some helathy and abnormal ECG data.
These data are in `data` directory.

### Nomral ECG data

* `data/healthy_person1.csv`
* `data/healthy_person2.csv`
* `data/healthy_person3.csv`
* `data/healthy_person4.csv`

### Abnormal ECG data

* `data/disease_person1.csv`
	* This data contain big anomalous part.
* `data/disease_person2.csv`
 	* This data contain small anomalous part.
* `data/disease_person3.csv`
  	* This data is chronically abnormal in QRS wave.




