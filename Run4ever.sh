#!/bin/bash
while true; do
	touch /tmp/DranpumpData/RestartIndicator
	python test.py -t 192.168.1.18 -c energy | tee /tmp/ful_log.txt
done