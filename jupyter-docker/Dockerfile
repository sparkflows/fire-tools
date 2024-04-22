# Docker demo image, as used on try.jupyter.org and tmpnb.org

FROM jupyter/all-spark-notebook:c7fb6660d096

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root
RUN apt-get update \
 && apt-get -y dist-upgrade --no-install-recommends \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# BEGININCLUDE jupyter/datascience-notebook
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# FROM jupyter/scipy-notebook

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

USER root

# R pre-requisites
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-dejavu \
    tzdata \
    gfortran \
    gcc && apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# ENDINCLUDE jupyter/datascience-notebook


# Install system libraries first as root
USER root

# The Glorious Glasgow Haskell Compiler
RUN apt-get update && \
    apt-get install -y --no-install-recommends software-properties-common && \
    add-apt-repository -y ppa:hvr/ghc && \
    apt-get update && \
    apt-get install -y cabal-install-1.24 ghc-8.0.2 happy-1.19.5 alex-3.1.7 && \
    apt-get clean

# IHaskell dependencies
RUN apt-get install -y --no-install-recommends zlib1g-dev libzmq3-dev libtinfo-dev libcairo2-dev libpango1.0-dev && apt-get clean

USER $NB_USER


# Extra Kernels
RUN echo $NB_USER
RUN pip install papermill
RUN pip install pandas==1.2.4
RUN pip install numpy==1.21.4
RUN pip install seaborn==0.11.1
RUN pip install scikit-learn==0.24.0
RUN pip install plotly==5.5.0
RUN pip install matplotlib==3.4.2
COPY fire_notebook-3.1.0-py3-none-any.whl /home/$NB_USER/
RUN pip install fire_notebook-3.1.0-py3-none-any.whl
RUN pip install --no-cache-dir bash_kernel && \
    python -m bash_kernel.install --sys-prefix


# Add local content, starting with notebooks and datasets which are the largest
# so that later, smaller file changes do not cause a complete recopy during
# build
COPY notebooks/ /home/$NB_USER/
COPY datasets/ /home/$NB_USER/datasets/

# Switch back to root for permission fixes, conversions, and trust. Make sure
# trust is done as $NB_USER so that the signing secret winds up in the $NB_USER
# profile, not root's
USER root


# Finally, add the site specific tmpnb.org / try.jupyter.org configuration.
# These should probably be split off into a separate docker image so that others
# can reuse the very expensive build of all the above with their own site
# customization.

# Add the templates
COPY resources/templates/ /srv/templates/
RUN chmod a+rX /srv/templates

USER $NB_USER

# Install our custom.js
COPY resources/custom.js /home/$NB_USER/.jupyter/custom/

# Append tmpnb specific options to the base config
COPY resources/jupyter_notebook_config.partial.py /tmp/
