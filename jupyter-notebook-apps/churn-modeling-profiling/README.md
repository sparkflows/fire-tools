# Churn Modeling and Profiling
This repository contains a Jupyter notebook titled ChurnModelingAndProfiling.ipynb that demonstrates how to model and profile customer churn using various Python data analysis libraries. Additionally, the notebook integrates with the Fire Notebook SDK to manage the workflow and outputs.

## Overview
The notebook provides a complete workflow for analyzing customer churn data, offering options to either profile the data or run churn prediction models. It leverages the Fire Notebook SDK to manage outputs, track progress, and handle workflow states efficiently.

## Features
- **Data Loading & Preprocessing**: Ingests and cleans customer churn data.
- **Exploratory Data Analysis (EDA)**: Visualizes data trends, customer segmentation, and key metrics affecting churn using interactive plots.
- **Churn Modeling**: Implements churn prediction models to forecast customer behavior.
- **Fire Notebook SDK**: Utilizes the SDK to manage outputs and shows usage of how to track progress, handle failures, and generate outputs.
- **Profiling & Insights**: Provides profiling reports and key insights based on churn data.

## Requirements
To run the notebook and utilize the Fire Notebook SDK, you will need the following dependencies:

- Python 3.8+
- pandas
- pyspark
- plotly
- Fire Notebook SDK

You can install the required Python packages using:

```bash
pip install pandas pyspark plotly
```

You can install the fire notebook sdk using:

```bash
pip install https://sparkflows-release.s3.amazonaws.com/fire/jupyter-docker/firenotebookwheel/fire_notebook-3.1.0-py3-none-any.whl
```

You can follow the documentation on how to create notebooks and use the fire notebook SDK here: 
https://docs.sparkflows.io/en/latest/jupyter-guide/analytical-apps/index.html

