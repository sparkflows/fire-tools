# Customer Churn Exploratory Data Analysis

This repository contains a Jupyter notebook for **Customer Churn Exploratory Data Analysis (EDA)** using the **Fire Notebook SDK**. The notebook helps in analyzing customer churn data, integrating Fire Notebook SDK for producing outputs with Python.

## Overview

The goal of this project is to perform an exploratory analysis of customer churn data, extracting valuable insights through Python data processing libraries and using the **Fire Notebook SDK**.

The application takes in the parameters:
- Distributor
- Sector
- Category
- Sub-Category

The below screenshot of the application UI shows the input parameters being selected which are then sent to the notebook to be processed.

<img width="1246" alt="image" src="https://github.com/user-attachments/assets/84c25996-a00a-4495-8c24-4ea360a0f1f4">


## Features

- **Data Loading and Preprocessing**: Loads customer churn data from a dataset and preprocesses it for analysis.
- **Exploratory Data Analysis**: Generates visualizations and statistical summaries of the data.
- **Fire Notebook SDK Integration**: Demonstrates how to integrate and manage outputs and usage of the SDK.
- **Key Insights**: Identifies important features affecting customer churn and helps build a foundation for future model development.

## Requirements

To run the notebook and integrate with the Fire Notebook SDK, ensure the following dependencies are installed:

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
