#!/bin/bash

# ./collect_all.sh ./model-repo

python3 collect_cao2020.py $1
python3 collect_cao2023.py $1
python3 collect_domeier2014.py $1
python3 collect_golonka.py $1
python3 collect_matthews2016_mantle_ref.py $1
python3 collect_matthews2016_pmag_ref.py $1
python3 collect_merdith2021.py $1
python3 collect_muller2016.py $1
python3 collect_muller2019.py $1
python3 collect_muller2022.py $1
python3 collect_paleomap.py $1
python3 collect_pehrsson2015.py $1
python3 collect_rodinia.py $1
python3 collect_seton2012.py $1
python3 collect_torsvikcocks2017.py $1
python3 collect_clennett2020_m2019.py $1
python3 collect_clennett2020_s2013.py $1
python3 collect_zahirovic2022.py $1
python3 collect_shephard2013.py $1
python3 collect_young2018.py $1