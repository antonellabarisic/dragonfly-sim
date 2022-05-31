FROM osrf/ros:melodic-desktop-full

ENV NVIDIA_VISIBLE_DEVICES \
    ${NVIDIA_VISIBLE_DEVICES:-all}
ENV NVIDIA_DRIVER_CAPABILITIES \
    ${NVIDIA_DRIVER_CAPABILITIES:+$NVIDIA_DRIVER_CAPABILITIES,}graphics

ENV DEBIAN_FRONTEND noninteractive
ENV WORKSPACE=/workspace

RUN apt-get -qq update && \
    apt-get -qq upgrade && \
    apt-get -qq install apt-utils build-essential vim python-catkin-tools

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Install Dependencies
RUN apt-get -qq install python-dev python-opencv python-wxgtk3.0 \
    python-pip python-matplotlib python-pygame python-lxml python-yaml \
    ros-melodic-mavros ros-melodic-mavros-extras libgazebo9-dev rsync \
    ros-melodic-octomap-ros libgoogle-glog-dev

# Install MavProxy
RUN pip install MAVProxy

# Clear apt cache to save on space
RUN rm -rf /var/lib/apt/lists/*

# Setup Geographic dataset
RUN mkdir -p $WORKSPACE/data && \
    cd $WORKSPACE/data && \
    wget https://raw.githubusercontent.com/mavlink/mavros/master/mavros/scripts/install_geographiclib_datasets.sh && \
    chmod 700 ./install_geographiclib_datasets.sh && \
    ./install_geographiclib_datasets.sh

# Install simulation
RUN cd $WORKSPACE && git clone https://github.com/larics/ardupilot.git

RUN cd $WORKSPACE/ardupilot && git checkout 5e4a5398dbe5c23acda5df0a81b655d1dfc01e5b
RUN cd $WORKSPACE/ardupilot && git submodule update --init --recursive

# RUN .$WORKSPACE/ardupilot/Tools/environment_install/install-prereqs-ubuntu.sh -y

# Add hummingbird springs as default location (https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html)
RUN echo "HUMMINGBIRD=35.824822,-106.6577015,2036,0" >> $WORKSPACE/ardupilot/Tools/autotest/locations.txt
RUN echo "ARROYO_DEL_OSO=35.138824,-106.556401,1643,0" >> $WORKSPACE/ardupilot/Tools/autotest/locations.txt
RUN echo "BALLOON_FIESTA=35.195006,-106.596133,1528,0" >> $WORKSPACE/ardupilot/Tools/autotest/locations.txt
RUN echo "SALT_SPRINGS=38.498443,-112.8528725,230,0" >> $WORKSPACE/ardupilot/Tools/autotest/locations.txt

# Install pexpect for ardupilot build
RUN pip install pexpect

# Build ardupilot binaries
RUN cd $WORKSPACE/ardupilot && modules/waf/waf-light configure --board sitl
RUN cd $WORKSPACE/ardupilot && modules/waf/waf-light build --target bin/arducopter

# RUN cd $WORKSPACE/ardupilot_gazebo && \
#     mkdir build && cd build && cmake .. && make -j4 && make install

RUN mkdir $WORKSPACE/gazebo

COPY ./gazebo $WORKSPACE/gazebo

RUN cd $WORKSPACE/gazebo/src && \
    git clone https://github.com/antonellabarisic/ardupilot_gazebo.git && \
    cd ardupilot_gazebo && \
    git checkout larics-master-dev

RUN cd $WORKSPACE/gazebo/src && \
    git clone https://github.com/larics/rotors_simulator && \
    cd rotors_simulator && \
    git checkout larics_melodic_master

RUN cd $WORKSPACE/gazebo/src && \
    git clone https://github.com/larics/mav_comm && \
    cd mav_comm && \
    git checkout larics_master


# RUN cd $WORKSPACE/gazebo/src && \
#     git clone https://github.com/ethz-asl/rotors_simulator && \
#     git clone https://github.com/ethz-asl/mav_comm.git && \
#     git clone https://github.com/catkin/catkin_simple.git
RUN ls
RUN source /opt/ros/melodic/setup.bash && \
    cd $WORKSPACE/gazebo && \
    catkin build

RUN echo "source /opt/ros/melodic/setup.bash" >> /root/.bashrc
RUN echo "source /workspace/gazebo/devel/setup.bash" >> /root/.bashrc
RUN echo "alias re-source='source ~/.bashrc'" >> /root/.bashrc

RUN echo "export GAZEBO_MODEL_PATH=/workspace/gazebo/src/ardupilot_gazebo/models:/workspace/gazebo/src/ardupilot_gazebo/models_gazebo:/workspace/gazebo/src/dragonfly_sim/models:$GAZEBO_MODEL_PATH" >> /root/.bashrc
RUN echo "export GAZEBO_PLUGIN_PATH=/workspace/gazebo/build/ardupilot_gazebo:$GAZEBO_PLUGIN_PATH" >> /root/.bashrc

COPY ./templates $WORKSPACE/templates

# Setup Entrypoint
COPY ./docker/entrypoint.sh /
COPY ./docker/entrypoint.py /
COPY ./docker/entrypoint_kopterworx.py /
COPY ./docker/entrypoint_kopterworx_kopterworx.py /



ENTRYPOINT ["/entrypoint_kopterworx_kopterworx.py"]