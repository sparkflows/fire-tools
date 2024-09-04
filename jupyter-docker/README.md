## Create Analytical Apps using Jupyter Notebooks

Fire Insights provides a workbench for creating the frontend of Analytical Apps. The backend can be Jupyter Notebook. The Jupyter Notebook would receive input parameters from the Analytical App, process it and output the results to be displayed in the App for the user.

This document describes the steps to create a Docker image which would execute the Jupyter Notebook.

In order to process the parameters and to send output results to the App a library is made available as a wheel file.


### fire_notebook-3.1.0-py3-none-any.whl

The `fire_notebook-3.1.0-py3-none-any.whl` file is a Python wheel package that facilitates the integration of the Fire Insights API with Jupyter Notebooks. This package allows for seamless data transmission and interaction between Sparkflows and Jupyter, enabling users to leverage the Fire Insights API for enhanced data analysis and workflow management within their notebooks. 

Download the latest `fire_notebook-3.1.0-py3-none-any.whl` wheel file available at : https://docs.sparkflows.io/en/latest/release-notes/binaries.html

Then, install the package using the downloaded wheel file, with the following command:

```
pip install path/to/fire_notebook-3.1.0-py3-none-any.whl
```

Or, you can directly install using the wheel file from S3: 

```
pip install https://sparkflows-release.s3.amazonaws.com/fire/jupyter-docker/firenotebookwheel/fire_notebook-3.1.0-py3-none-any.whl
```

### Sample Notebooks in the `notebooks` directory

There are four sample Jupyter Notebooks in the notebooks folder to test some of the various functionalites:

* fire_failure_notebook_functions.ipynb
* fire_html_plotly_notebook_functions.ipynb
* fire_notebook_functions.ipynb

* ChurnAnalysisAndPrediction.ipynb

### Sample Datasets in the `datasets` directory

The datasets folder contains the churn dataset that is used by the sample notebook ``ChurnAnalysisAndPrediction.ipynb``, which performs some data preprocessing, data visualization, modelling and uses RandomForestClassifier to train the model and returns a model accuracy report.


## Docker File Details

#### Dockerfile

The Dockerfile sets up an environment for running Jupyter Notebooks with the necessary dependencies. 

* It starts from an Ubuntu 20.04 base image, installs essential packages, and sets up Python 3.8.10.
* It installs various Python packages listed in requirements.txt, requirements2.txt, and requirements3.txt.
* It also installs additional packages like pmdarima, bs4, awscli, kfp, kubernetes, numpy, notebook, and plotly.
* The fire_notebook-3.1.0-py3-none-any.whl package is also installed to facilitate integration with the Fire Insights API.
* The Dockerfile configures the environment, copies necessary files, and sets up an entry point script for container initialization.

#### entrypoint.sh

1. The entrypoint.sh file first specifies that the scripts must be executed in the `/bin/sh` shell.
2. It then prints and checks whether the `python` command is pointing to the intended version (3.8).
3. Then it checks for python packages installed and filters the output to show packages with 'notebook' in the name to check if jupyter notebook is installed.
4. And finally it starts the jupyter notebook server.


## Building Docker Image Instructions

1. **Download Project Files:**
   - Ensure all files and folders in your project directory are downloaded.

2. **Verify Required Files:**
   - Ensure the following files are present in your project directory:
     - `requirements.txt`, `requirements2.txt`, `requirements3.txt`
     - `fire_notebook-3.1.0-py3-none-any.whl` file
     - `Dockerfile`
     - `entrypoint.sh`

3. **Prepare Datasets:**
   - Create a `datasets` folder in your project directory.
   - Add the datasets you want to work with to this folder.

4. **Prepare Notebooks:**
   - Create a `notebooks` folder in your project directory.
   - Add your Jupyter notebooks that will interact with the datasets and Fire Insights to this folder.

5. **Build and Push Docker Image:**
   - Use the Docker commands below to build your Docker image and push it to Docker Hub, making it accessible for pulling.


    ```
    docker build -t username/repo:tagname
    docker push username/repo:tagname
    ```
    
    Ensure that you replace `username/repo` and `tagname` with the actual names. Take note of the image name, which will be used in the next steps when creating a Jupyter connection in Fire Insights.



