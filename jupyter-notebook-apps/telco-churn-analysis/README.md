# Telco Churn Analysis

This repository contains a Jupyter notebook titled telco_churn_analysis.ipynb that demonstrates customer churn analysis using various Python data analysis libraries. Additionally, the notebook integrates with the Fire Notebook SDK to accept parameters and produce outputs in Fire UI.


## Overview

The Telco Churn Analysis notebook provides backend application code for analyzing customer churn behavior. It includes data preprocessing, filtering, statistical analysis, correlation matrix calculation, and data visualization techniques. The Fire Notebook SDK is used to accept input parameters, manage outputs, and track execution progress.

The application takes in the following parameters:

- `arg_state`: Filter customers based on state.
- `arg_intl_plan`: Filter customers based on their international plan subscription.
- `arg_voice_mail_plan`: Filter customers based on their voicemail plan subscription.

## Features

- **Data Loading & Preprocessing**: Loads the Telco churn dataset and preprocesses it by filtering based on user input.
- **Exploratory Data Analysis (EDA)**: Provides summary statistics, correlation matrix, and visualizations of customer churn behavior.
- **Customer Churn Grouping**: Aggregates churn-related metrics and visualizes the churned vs non-churned customers.
- **Fire Notebook SDK**: Demonstrates integration with the Fire Notebook SDK to manage outputs, input parameters, and track workflow progress.

### SDK Functions Used:

- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outPandasDataframe()`: To output a pandas data frame to Fire UI
- `outSuccess()`: To indicate the execution status of SUCCESS for the job


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
