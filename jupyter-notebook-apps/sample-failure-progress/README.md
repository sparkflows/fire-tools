# Failure Progress

This repository folder contains a Jupyter notebook titled sample_failure_progress.ipynb that demonstrates the usage of the fire_notebook SDK on how to show failures in progress and execution.

## Overview

The notebook uses the following SDK functions:

- `outStr()`: To output text to Fire UI
- `outputProgress()`: To share the progress of the Notebook run as a percentage with the analytical app
- `outFailure()`: To indicate the execution status of FAILURE of the job


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