FROM continuumio/miniconda3:4.5.4

RUN pip install -e git+https://github.com/jeremyarr/jenkins_badges.git@5dadb44d1df3dfa27cb1a1ec75c939de962a009e#egg=jenkins_badges

ADD server.py /server.py
