# Databricks Analytical Applications

This folder contains all analytical applications related to **Databricks Notebooks**. The structure is designed to keep the project organized and maintain consistency across various components.

## Folder Structure

Each project will follow this standardized folder structure:

```
/project-name
    ├── apps/
    ├── datasets/
    └── notebooks/
```

### 1. `apps/`
This folder contains the source code in JSON format for the analytical application(s). These application(s) are used to interact with Databricks notebooks, perform data processing, i.e mainly servings as user interfaces for end-users.

### 2. `datasets/`
This folder stores all the datasets used by the notebooks. It should mainly include the raw data and any template data that are required for analysis or model training.

### 3. `notebooks/`
The `notebooks/` folder contains all Databricks notebooks (`.ipynb` or `.py` files) that are part of the project. These notebooks include the core logic for data processing, analysis, machine learning models, and visualizations.

---

## Requirements

To run the notebook and integrate with the Fire Notebook SDK, ensure the following dependencies are installed:

- Python 3.8+
- pandas
- pyspark
- plotly

## Downloading SDK

To run these notebooks, make sure you have the `fire_notebook` SDK installed in the databricks cluster.

### Importing SDK
To import the SDK, use the following line:
```
from fire_notebook.output.workflowcontext import RestWorkflowContext
```

## Documentation

The Documentation links for building Analytical Apps on Jupyter Notebooks is available here: 
- https://docs.sparkflows.io/en/latest/databricks/index.html
- https://docs.sparkflows.io/en/latest/databricks/user-guide/integrating-with-databricks-notebook.html

# Table of Contents

1. [Customer Churn Analysis](#1-customer-churn-analysis)
2. [Campaign Analytics](#2-campaign-analytics)
3. [IoT Energy Solution](#3-iot-energy-solution)
4. [Demand Forecasting](#4-demand-forecasting)
5. [Telco Churn Analysis](#5-telco-churn-analysis)

---

### 1. Customer Churn Analysis

**Description**: This notebook performs extensive exploratory data analysis (EDA) on a customer churn dataset. It includes visualizations created using the `outPlotly()` function from the `fire_notebook` SDK, and it demonstrates how to:
- Provide progress updates during execution with `outputProgress()`.
- Display running and success messages at the start and end of execution.

**Key Features**:
- EDA on customer churn data.
- Plotting with `outPlotly()`.
- Progress percentage updates and status messages.

[Link to app folder](./customer-churn)

---

### 2. Campaign Analytics

**Description**: This notebook performs EDA on a retail campaign analytics dataset. It also includes visualizations, with charts created using the `outPlotly()` function of the `fire_notebook` SDK.

**Key Features**:
- EDA on retail campaign data.
- Visualization with `outPlotly()` from the `fire_notebook` SDK.

[Link to app folder](./campaign-analytics)

---

### 3. IoT Energy Solution

**Description**: This notebook focuses on EDA for an IoT energy dataset. It utilizes `outPlotly()` from the `fire_notebook` SDK to generate visualizations, demonstrating its ability to handle large-scale IoT data.

**Key Features**:
- EDA on IoT energy data.
- Chart plotting with `outPlotly()`.

[Link to app folder](./iot-energy-solutions)

---

### 4. Demand Forecasting

**Description**: This notebook demonstrates how to leverage the fire_notebook SDK while performing demand forecasting on sales data. It includes features for outputting progress, status messages, and visualizations throughout the analysis process. It serves as an example of how the SDK can be integrated into more complex analytical workflows.

**Key Features**:

- Real-time progress updates with `outputProgress()`.
- Status messages to indicate execution stages with `outStr()`.
- Interactive visualizations using `outPlotly()`.

[Link to app folder](./demand-forecasting)

---

### 5. Telco Churn Analysis

**Description**: This repository contains a Jupyter notebook titled telco_churn_analysis.ipynb that demonstrates customer churn analysis using various Python data analysis libraries. Additionally, the notebook integrates with the Fire Notebook SDK to accept parameters and produce outputs in Fire UI.

**Key Features**:
- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outPandasDataframe()`: To output a pandas data frame to Fire UI
- `outSuccess()`: To indicate the execution status of SUCCESS for the job

[Link to app folder](./Telco-Churn)

















