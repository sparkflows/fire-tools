# IOT Energy Solutions Data Exploration

This repository contains a Databricks notebook titled **IoTEnergySolutionsEDA** that analyzes IOT energy data using various Python data analysis libraries. Additionally, the notebook integrates with the **Fire Notebook SDK** to manage the outputs.

## Overview

The notebook demonstrates how to perform exploratory data analysis (EDA) on a IOT energy solution dataset, leveraging the **Fire Notebook SDK** for notebook output management.

## Features

- **Data Loading & Preprocessing**: Ingests and cleans IOT energy data.
- **Debug and development Options**: The Databricks notebook App can be run in either debug mode, when development is on the local machine or run on the SDK. In the debug mode, the visualizations will be displayed on the notebook along with the debug logs.
- **Exploratory Data Analysis (EDA)**: Provides key insights into various energy metrics and correlations using visualizations and statistical summaries.
- **Fire Notebook SDK**: Demonstrates how to integrate and manage outputs and usage of the SDK.
- **Insights Extraction**: Delivers time series analysis of energy consumption and energy generation for different devices.

## Analytical App Screenshots

- Introduction

  <img width="468" alt="image" src="https://github.com/user-attachments/assets/2bd6177c-0f7b-42bf-9b64-2a9bf64e83a6">

- Line graph for energy consumption/generation

  <img width="468" alt="image" src="https://github.com/user-attachments/assets/49055eb2-9f2e-43b2-8a8f-8a070acafd94">

- Histogram for selected column

  <img width="468" alt="image" src="https://github.com/user-attachments/assets/35a02538-a064-4ffc-afde-d8ea92fb73ca">

- Boxplot for selected column
  
  <img width="468" alt="image" src="https://github.com/user-attachments/assets/c61895e9-d3aa-415d-bb24-e9c659372fc8">


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
