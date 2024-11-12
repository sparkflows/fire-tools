# Sample Notebook Apps using SDK

This repository contains a set of example notebooks that demonstrate the use of the `fire_notebook` SDK for managing outputs, progress tracking, and visualizations. Each notebook showcases different aspects of how the SDK can be integrated into data analysis workflows, from failure handling to exploratory data analysis (EDA) and modeling.

## Getting Started

### Requirements

To run the notebook and integrate with the Fire Notebook SDK, ensure the following dependencies are installed:

- Python 3.8+
- pandas
- pyspark
- plotly

Download the following dependencies to be able to use the `fire_notebook` SDK:

```bash
pip install pandas pyspark plotly
```

### Downloading SDK

To run these notebooks, make sure you have the `fire_notebook` SDK installed. You can install it via pip:

```bash
pip install https://sparkflows-release.s3.amazonaws.com/fire/jupyter-docker/firenotebookwheel/fire_notebook-3.1.0-py3-none-any.whl
```
### Importing SDK
To import the SDK, use the following line:
```
from fire_notebook.output.workflowcontext import RestWorkflowContext
```


## Documentation

The Documentation for building Analytical Apps on Jupyter Notebooks is available here : https://docs.sparkflows.io/en/latest/jupyter-guide/analytical-apps/index.html#


## Table of Contents

1. [Sample Failure Progress](#1-sample-failure-progress)
2. [Churn Modeling and Profiling](#2-churn-modeling-and-profiling)
3. [Customer Churn Exploratory Data Analysis](#3-customer-churn-exploratory-data-analysis)
4. [Campaign Analytics](#4-campaign-analytics)
5. [IoT Energy Solution](#5-iot-energy-solution)
6. [Demand Analysis](#6-demand-analysis)
7. [MySQL Connection Details](#7-mysql-connection-details)
8. [Telco Churn Analysis](#8-telco-churn-analysis)
9. [Progress Failure](#9-progress-failure)

---

### 1. Sample Failure Progress

**Description**: This notebook is a basic demonstration of the `fire_notebook` SDK, showing how to:
- Output a string message during execution.
- Display progress percentage.
- Handle failure scenarios by providing a failure message.

**Key Features**:
- Example of `outStr()`.
- Progress tracking with `outputProgress()`.
- Failure message handling `outFailure()`.

---

### 2. Churn Modeling and Profiling

**Description**: This notebook allows users to choose between profiling and modeling operations on a customer churn dataset. Based on the user’s selection, the notebook app performs the corresponding operations.

**Key Features**:
- Interactive choice between profiling and modeling.
- Conditional logic for performing different tasks using the `fire_notebook` SDK.

---

### 3. Customer Churn Exploratory Data Analysis

**Description**: This notebook performs extensive exploratory data analysis (EDA) on a customer churn dataset. It includes visualizations created using the `outPlotly()` function from the `fire_notebook` SDK, and it demonstrates how to:
- Provide progress updates during execution with `outputProgress()`.
- Display running and success messages at the start and end of execution.

**Key Features**:
- EDA on customer churn data.
- Plotting with `outPlotly()`.
- Progress percentage updates and status messages.

---

### 4. Campaign Analytics

**Description**: This notebook performs EDA on a retail campaign analytics dataset. It also includes visualizations, with charts created using the `outPlotly()` function of the `fire_notebook` SDK.

**Key Features**:
- EDA on retail campaign data.
- Visualization with `outPlotly()` from the `fire_notebook` SDK.

---

### 5. IoT Energy Solution

**Description**: This notebook focuses on EDA for an IoT energy dataset. It utilizes `outPlotly()` from the `fire_notebook` SDK to generate visualizations, demonstrating its ability to handle large-scale IoT data.

**Key Features**:
- EDA on IoT energy data.
- Chart plotting with `outPlotly()`.

[Link to app folder](./IOT-Energy_Solution)

---

### 6. Demand Analysis

**Description**: This notebook demonstrates how to leverage the fire_notebook SDK while performing demand forecasting on sales data. It includes features for outputting progress, status messages, and visualizations throughout the analysis process. It serves as an example of how the SDK can be integrated into more complex analytical workflows.

**Key Features**:

- Real-time progress updates with `outputProgress()`.
- Status messages to indicate execution stages with `outStr()`.
- Interactive visualizations using `outPlotly()`.

---

### 7. MySQL Connection Details

**Description**: This repository folder contains a Jupyter notebook titled notebook_connections.ipynb that demonstrates how to leverage the fire_notebook SDK to securely retrieve MySQL connection details. This approach allows for concealing sensitive connection information and credentials from application users, while still enabling seamless interaction with MySQL databases.

**Key Features**:
- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outPandasDataframe()`: To showcase the contents of a Pandas DataFrame as a table in Fire UI
- `outHTML()`: To display HTML code in Fire UI
- `outSuccess()`: To display the SUCCESSFUL execution status of the job
- `getConnectionDetails()`: Retrieves MySQL connection details

---

### 8. Telco Churn Analysis

**Description**: This repository contains a Jupyter notebook titled telco_churn_analysis.ipynb that demonstrates customer churn analysis using various Python data analysis libraries. Additionally, the notebook integrates with the Fire Notebook SDK to accept parameters and produce outputs in Fire UI.

**Key Features**:
- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outPandasDataframe()`: To output a pandas data frame to Fire UI
- `outSuccess()`: To indicate the execution status of SUCCESS for the job

---

### 9. Progress Failure

**Description**: This repository folder contains a Jupyter notebook titled sample_failure_progress.ipynb that demonstrates the usage of the fire_notebook SDK on how to show failures in progress and execution.

**Key Features**:
- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outFailure()`: To indicate the execution status of FAILURE of the job

---


