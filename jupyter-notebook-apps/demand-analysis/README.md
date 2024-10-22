# Demand Analysis

This repository contains a Jupyter notebook titled demand_analysis.ipynb that demonstrates how to perform some demand analysis using various Python data analysis libraries. Additionally, the notebook integrates with the Fire Notebook SDK for accepting parameters and producing outputs in Fire UI.


## Overview

The notebook provides an example on how to create a notebook for an application which performs some demand analysis. It includes data preprocessing, visualization, and time series analysis techniques. The Fire Notebook SDK is used to accept input parameters, manage outputs and also track progress of execution.

The application takes in the following parameters:
- shape
- unique_values
- data_types
- head
- tail
- missing_values
- quantiles

## Features
- **Data Loading & Preprocessing**: Ingests and cleans time series demand data.
- **Exploratory Data Analysis (EDA)**: Visualizes trends, seasonality, and key metrics affecting demand using interactive plots.
- **Fire Notebook SDK**: Demonstrates how to integrate and manage outputs and other usage and features of the SDK.

### Some SDK Functions Used:

- Real-time progress updates with `outputProgress()`.
- Status messages to indicate execution stages with `outStr()`.
- Interactive visualizations using `outPlotly()`.

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

