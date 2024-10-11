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
