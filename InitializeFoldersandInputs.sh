#!/bin/bash

mkdir input
mkdir output
mkdir events
mkdir output_analysis
mkdir output_analysis/fig


cd InputCreation

python3 CreateCarInitDataset.py
python3 CreatePickleEventi.py 
python3 CreatePickleZoneDistance.py
python3 CreateValidZones.py

