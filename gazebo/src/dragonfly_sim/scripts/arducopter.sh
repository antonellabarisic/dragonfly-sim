#!/bin/bash

if [[ -z "$1" || -z "$2" || -z "$3" ]]
then
    echo "Usage: ./arducopter.sh <arducopter instance> <temp directory> <param_file> <location>"
    exit 1
else
    instance=$1
    temp_directory=$2
    param_file=$3
    location=$4
fi

cd /workspace
mkdir -p temp/$temp_directory
./ardupilot/Tools/autotest/sim_vehicle.py -L $location -v ArduCopter -f gazebo-iris -I $instance --add-param-file $param_file --use-dir temp/$temp_directory -m --streamrate=50