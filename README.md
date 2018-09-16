# SmartPlugTools
Read and report TP Link smart plug device.

MAIN helpful python script retrieving info from TP Link device.
https://github.com/softScheck/tplink-smartplug

Time text report from HS110 device:
python tplink_smartplug.py -t 192.168.1.75 -c time | sed smart-stuff filter

Energy text report from HS110 device:
python tplink_smartplug.py -t 192.168.1.75 -c energy | sed smart-stuff filter

Filter BEFORE “power:”
sed -n -e 's/^.*power"://p' example.txt

Graph generating with GnuPlot
Install GnuPlot from software manager.
Usage ex.
gnuplot -e "set terminal png size 400,300; set output 'xyz.png'; plot [-4:4] exp(-x**2 / 2)"

Calling GnuPlot from python
https://stackoverflow.com/questions/2161932/calling-gnuplot-from-python

