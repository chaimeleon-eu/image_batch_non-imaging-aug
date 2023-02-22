## Base image:
FROM nvcr.io/nvidia/pytorch:21.05-py3

############## Things done by the root user ##############
USER root
# Installation of tools and requirements:
COPY ./requirements.txt .
COPY ./ ./


RUN pip install -r requirements.txt

# create the user (and group) "chaimeleon"
RUN groupadd -g 1000 chaimeleon && \
    useradd --create-home --shell /bin/bash --uid 1000 --gid 1000 chaimeleon
# Default password "chaimeleon" for chaimeleon user.
RUN echo "chaimeleon:chaimeleon" | chpasswd

############### Now change to normal user ################
USER chaimeleon:chaimeleon

# create the directories where some volumes will be mounted
RUN mkdir -p /home/chaimeleon/datasets && \
    mkdir -p /home/chaimeleon/persistent-home && \
    mkdir -p /home/chaimeleon/persistent-shared-folder

# Copy of the application files into the container:
ENTRYPOINT ["python3","/workspace/main.py"]

WORKDIR /home/chaimeleon

## test it on local machine
# Base image:
#FROM nvcr.io/nvidia/pytorch:21.05-py3
#
## Installation of tools and requirements:
#COPY ./requirements.txt .
#COPY ./ ./
#
#RUN pip install -r requirements.txt
#
#
## Copy of the application files into the container:
#CMD ["python3","./main.py"]
#ENTRYPOINT ["python3"]

