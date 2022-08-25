
FROM ros:noetic-ros-base

SHELL [ "/bin/bash" , "-c" ]

RUN apt-get update && sudo apt-get install -y ros-noetic-map-server

WORKDIR /opt/ros/noetic/share/map_server/maps

WORKDIR /opt/ros/noetic/share/map_server/launch

COPY  ./launch_files/ /opt/ros/noetic/share/map_server/launch

RUN source /opt/ros/noetic/setup.bash 

