## Create Analytical Apps using Jupyter Notebooks

Fire Insights provides a workbench for creating the frontend of Analytical Apps. The backend can be Jupyter Notebook. The Jupyter Notebook would receive input parameters from the Analytical App, process it and output the results to be displayed in the App for the user.

This document describes the steps to create a Docker image which would execute the Jupyter Notebook.

In order to process and parameters and to send output results to the App a library is made available as a wheel file.

fire_notebook-3.1.0-py3-none-any.whl

### fire_notebook-3.1.0-py3-none-any.whl

The `fire_notebook-3.1.0-py3-none-any.whl` file is a Python wheel package that facilitates the integration of the Fire Insights API with Jupyter Notebooks. This package allows for seamless data transmission and interaction between Sparkflows and Jupyter, enabling users to leverage the Fire Insights API for enhanced data analysis and workflow management within their notebooks. To install the package, use the following command:

```
pip install path/to/fire_notebook-3.1.0-py3-none-any.whl
```

### Sample Notebooks in the `notebooks` directory

There are four sample Jupyter Notebooks in the notebooks folder to test some of the various functionalites:

* fire_failure_notebook_functions.ipynb
* fire_html_plotly_notebook_functions.ipynb
* fire_notebook_functions.ipynb

* ChurnAnalysisAndPrediction.ipynb


## Create Docker Image with the Jupyter Notebooks

#### Dockerfile

The Dockerfile sets up an environment for running Jupyter Notebooks with the necessary dependencies. 

* It starts from an Ubuntu 20.04 base image, installs essential packages, and sets up Python 3.8.10.
* It installs various Python packages listed in requirements.txt, requirements2.txt, and requirements3.txt, along with additional packages like pmdarima, bs4, awscli, kfp, kubernetes, numpy, notebook, and plotly.
* The fire_notebook-3.1.0-py3-none-any.whl package is also installed to facilitate integration with the Fire Insights API.
* The Dockerfile configures the environment, copies necessary files, and sets up an entry point script for container initialization.

Below are the Docker commands used to build the image and push it to Docker Hub, making it accessible for pulling:

```
docker build -t username/repo:tagname
docker push username/repo:tagname
```
