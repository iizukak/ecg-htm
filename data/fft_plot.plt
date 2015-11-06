set datafile separator ","

set pm3d map
set xlabel "Frequency"
set ylabel "Time Step"

splot "healthy_person1_fft_converted.csv" matrix

