#!/bin/bash
set -e

source /opt/ros/melodic/setup.bash
source /workspace/gazebo/devel/setup.bash

export GAZEBO_MODEL_PATH=/workspace/gazebo/src/ardupilot_gazebo/models:/workspace/gazebo/src/ardupilot_gazebo/models_gazebo:/workspace/gazebo/src/dragonfly_sim/models:$GAZEBO_MODEL_PATH
export GAZEBO_PLUGIN_PATH=/workspace/gazebo/build/ardupilot_gazebo:$GAZEBO_PLUGIN_PATH

exec "$@"
