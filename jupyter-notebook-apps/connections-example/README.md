# MySQL - Get Connection Details

This repository folder contains a Jupyter notebook titled notebook_connections.ipynb that demonstrates how to leverage the fire_notebook SDK to securely retrieve MySQL connection details. This approach allows for concealing sensitive connection information and credentials from application users, while still enabling seamless interaction with MySQL databases.

## Overview

The notebook uses the following SDK functions:

- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outPandasDataframe()`: To showcase the contents of a Pandas DataFrame as a table in Fire UI
- `outHTML()`: To display HTML code in Fire UI
- `outSuccess()`: To display the SUCCESSFUL execution status of the job
- `getConnectionDetails()`: Retrieves MySQL connection details


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
