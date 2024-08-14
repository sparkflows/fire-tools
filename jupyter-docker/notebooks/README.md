## Sample Notebooks

#### 1. jupyter_lab_3.ipynb
1. This notebook is used to test notebook connection and get the connection details.

#### 2. ChurnAnalysisAndPrediction.ipynb
This is a sample notebook can be used to test the functionality of the Jupyter Notebook connection: 
1. We start by initiating the connection using RestWorkflowContext.
2. We then load the data from the `churn_data.csv` file.
3. Profiling function returns the statistics summary of the data.
4. Data Preprocessing returns size and columns in the dataset and checks for missing values.
5. Data Visualization: Plots a histogram to see total_day_calls distribution. It also shows the correlation between the features using a heatmap.
6. If the option is selected as Modelling, model_training function is called. This function replaces True/False strings to integers and splits the data into training and testing sets (80%-20%). It then uses RandomForestClassifier to train the model and returns the model accuracy report. 

