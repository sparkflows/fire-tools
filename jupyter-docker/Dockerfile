FROM ubuntu:20.04
MAINTAINER sparkflows <jayant@sparkflows.io>

ENV APP_HOME /usr/local
ENV USERNAME=sparkflows

RUN apt-get update

RUN apt-get install -y ca-certificates wget sudo && update-ca-certificates

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get --assume-yes install software-properties-common
RUN add-apt-repository ppa:ts.sch.gr/ppa
RUN apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
RUN echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections
RUN apt-get install -y --force-yes openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
RUN export JAVA_HOME

COPY requirements.txt ${APP_HOME}
COPY requirements2.txt ${APP_HOME}
COPY requirements3.txt ${APP_HOME}

RUN apt-get update \
&& sudo apt install -q -y vim build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev \
&& mkdir -p /home/${USERNAME} \
&& adduser --disabled-password --gecos '' ${USERNAME} \
&& adduser ${USERNAME} sudo \
&& echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
&& chown -R ${USERNAME} /home/${USERNAME} \
&& wget https://www.python.org/ftp/python/3.8.10/Python-3.8.10.tgz \
&& tar xzf Python-3.8.10.tgz \
&& cd  Python-3.8.10 && \
./configure --enable-optimizations  && make altinstall

#RUN sudo update-alternatives  --set python /usr/bin/python3.8
#RUN cd /usr/bin && sudo ln -s python3.8 /usr/bin/python
COPY fire_notebook-3.1.0-py3-none-any.whl ${APP_HOME}
RUN sudo apt-get install -y python3-pip
RUN cd ${APP_HOME} && \
    #python3.8 -m venv venv && \
    #source venv/bin/activate && \
    pip install pip --upgrade && \
    pip install six==1.15.0 && \
    pip install -r requirements.txt && \
    pip install -r requirements2.txt && \
    pip install -r requirements3.txt && \
    pip install pmdarima && \
    pip install bs4 && \
    pip install awscli && \
    pip install kfp==1.8.1 && \
    pip install kubernetes==18.20.0 && \
    pip install numpy==1.21 && \
    pip install notebook==6.5.6 && \
    pip install ${APP_HOME}/fire_notebook-3.1.0-py3-none-any.whl && \
    pip install plotly==5.24.0

RUN cd /usr/bin && sudo ln -s python3.8 /usr/bin/python

#RUN cd ${APP_HOME} && \
    #python3.8 -m venv venv && \
    #source venv/bin/activate && \
#    pip install plotly

COPY notebooks ${APP_HOME}
COPY datasets ${APP_HOME}

# Expose port
USER root
WORKDIR ${APP_HOME}
# add provision to mount directories too - todo

ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
