# Instructions copied from - https://hub.docker.com/_/python/
FROM ubuntu:16.04

# Install required libraries
RUN apt-get update
RUN apt-get -y install build-essential libssl-dev libffi-dev python-dev
RUN apt-get -yqq install python python-pip python-dev python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN apt-get install -y openssh-server sshpass nano virtualenv supervisor
RUN apt-get install -y vim

# Install required python libraries
ADD heft/requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt
RUN pip2 install -r requirements.txt


# Authentication
RUN echo 'root:PASSWORD' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Prepare heft files
RUN mkdir -p heft
ADD heft/start.sh /heft/start.sh
ADD heft/keep_alive.py /heft/keep_alive.py
ADD heft/master.py  /heft/master.py
ADD heft/heft_dup.py /heft/heft_dup.py
ADD heft/create_input.py /heft/create_input.py
ADD heft/read_input_heft.py /heft/read_input_heft.py
ADD heft/write_input_heft.py /heft/write_input_heft.py
ADD jupiter_config.ini /heft/jupiter_config.ini

#ADD input_0.tgff /heft/input_0.tgff

RUN mkdir -p /heft/output
RUN chmod +x /heft/start.sh
ADD task_specific_files/network_monitoring_app/configuration.txt  /heft/dag.txt
ADD task_specific_files/network_monitoring_app/scripts/config.json /heft/config.json

WORKDIR /heft/


# tell the port number the container should expose
EXPOSE 22 8888

CMD ["./start.sh"]