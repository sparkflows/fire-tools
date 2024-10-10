# IOT Energy Solutions Data Exploration

This repository contains a Jupyter notebook titled **03-IOT-EDA_RestWorkflowContext_Example** that analyzes IOT energy data using various Python data analysis libraries. Additionally, the notebook integrates with the **Fire Notebook SDK** to manage the outputs.

## Overview

The notebook demonstrates how to perform exploratory data analysis (EDA) on a IOT energy solution dataset, leveraging the **Fire Notebook SDK** for notebook output management.

## Features

- **Data Loading & Preprocessing**: Ingests and cleans IOT energy data.
- **Debug and development Options**: The Jupyter notebook App can be run in either debug mode, when development is on the local machine or run on the SDK. In debug mode, development flag needs to be set to local (i.e. Development = local). When this flag is set, the visualizations will be displayed on the notebook along with the debug logs.
- **Exploratory Data Analysis (EDA)**: Provides key insights into various energy metrics and correlations using visualizations and statistical summaries.
- **Fire Notebook SDK**: Demonstrates how to integrate and manage outputs and usage of the SDK.
- **Insights Extraction**: Delivers time series analysis of energy consumption and energy generation for different devices.

## Requirements
To run the notebook and utilize the **Fire Notebook SDK**, you will need the following:

- Python 3.8+
- pandas
- pyspark
- plotly
- Fire Notebook SDK

You can install the required packages using:

```bash
pip install pandas pyspark plotly
```

You can install the fire notebook sdk using:

```bash
pip install https://sparkflows-release.s3.amazonaws.com/fire/jupyter-docker/firenotebookwheel/fire_notebook-3.1.0-py3-none-any.whl
```
You can follow the documentation on how to create notebooks and use the fire notebook SDK here: 
https://docs.sparkflows.io/en/latest/jupyter-guide/analytical-apps/index.html
