set datafile separator ","
set yrange[0:1200]

plot \
"healthy_person1_converted.csv" using 3 with lines, \
"healthy_person2_converted.csv" using 3 with lines, \
"healthy_person3_converted.csv" using 3 with lines, \
"healthy_person4_converted.csv" using 3 with lines, \
"disease_person1_converted.csv" using 3 with lines, \
"disease_person2_converted.csv" using 3 with lines, \
"disease_person3_converted.csv" using 3 with lines
