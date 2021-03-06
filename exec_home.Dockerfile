# ** Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved.
# **     contributor: Pradipta Ghosh, Quynh Nguyen, Bhaskar Krishnamachari
# **     Read license file in main directory for more details

# Instructions copied from - https://hub.docker.com/_/python/
FROM ubuntu:16.04

# Install required libraries
RUN apt-get update
RUN apt-get -y install build-essential libssl-dev libffi-dev python-dev
RUN apt-get -yqq install python python-pip python-dev python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN apt-get update && apt-get install -y openssh-server
RUN apt-get -yqq update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y mongodb
RUN apt-get install -yqq bzip2 wget sshpass screen
RUN apt-get install -y net-tools
RUN apt-get install -y vim
RUN apt-get install g++ make openmpi-bin libopenmpi-dev -y
RUN apt-get install sudo -y
RUN apt-get install iproute2 -y


# Install required python libraries
ADD profilers/execution_profiler_mulhome/requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt


# Authentication
RUN echo 'root:PASSWORD' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Prepare MongoDB
RUN mkdir -p /mongodb/data
RUN mkdir -p /mongodb/log

ADD profilers/execution_profiler_mulhome/central_mongod /central_mongod
RUN chmod +x /central_mongod


RUN mkdir -p /centralized_scheduler/profiler_files
RUN mkdir -p /centralized_scheduler/generated_files
RUN mkdir -p /centralized_scheduler/profiler_files_processed



# IF YOU WANNA DEPLOY A DIFFERENT APPLICATION JUST CHANGE THIS LINE
ADD app_specific_files/network_monitoring/scripts/ /centralized_scheduler/
COPY app_specific_files/network_monitoring/sample_input /centralized_scheduler/sample_input
RUN mkdir -p /home/darpa/apps/data


ADD app_specific_files/network_monitoring/configuration.txt /centralized_scheduler/DAG.txt

ADD profilers/execution_profiler_mulhome/start_home.sh /centralized_scheduler/start.sh
ADD mulhome_scripts/keep_alive.py /centralized_scheduler/keep_alive.py
ADD profilers/execution_profiler_mulhome/profiler_home.py /centralized_scheduler/profiler_home.py
ADD jupiter_config.ini /centralized_scheduler/jupiter_config.ini


WORKDIR /centralized_scheduler/
RUN ls
# Prepare scheduling files
RUN chmod +x /centralized_scheduler/start.sh


# tell the port number the container should expose
EXPOSE 22 27017 57021 8888

CMD ["./start.sh"]
