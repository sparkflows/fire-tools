## Sample Notebooks

### 1. ChurnAnalysisAndPrediction.ipynb
This is a sample notebook can be used to test the functionality of the  notebook functions: 
#### 1. Start by initiating the connection using RestWorkflowContext.

By default webServerURL and jobID passed to notebook from apps as parameters.
```
webserverURL = "http://localhost:8080/messageFromSparkJob"
jobId = "123456789"
from fire_notebook.output.workflowcontext import RestWorkflowContext
restworkflowcontext = RestWorkflowContext(webserverURL=webserverURL, jobId=jobId)
```

In notebook below condition can be added to support in development env:
```
If development == ”local”:
	restworkflowcontext = RestWorkflowContext(debug=False)

else:
  	import sys
parameters_list = sys.argv
restworkflowcontext = RestWorkflowContext(parameters=parameters_list)
```
OR 
```
from fire_notebook.output.workflowcontext import RestWorkflowContext
import sys
parameters_list = sys.argv
if len(sys.argv) > 1:
   restworkflowcontext = RestWorkflowContext(parameters=parameters_list)
else:
   restworkflowcontext = RestWorkflowContext(debug=False)
```
Above code snippet allows the developer to test the notebook locally before it is deployed through apps.

#### 2. Different Notebook functions

2.1> Getting Other Parameter values

Below is the code snippet used in notebook to get the passed parameters value from apps to notebook.

```
#To get the parameters value
parameter_value = restworkflowcontext.getParameters(parameter_name="key", default="Value")
print("parameter_value for key is: "+parameter_value)
```
In Sparklows during app execution user can select the Profiling or Modeling value for `option` field for this notebook.

```
#"Profiling" OR "Modeling"
option = restworkflowcontext.getParmeters(parameter_name="option", default="Profiling")
```

2.2> Displaying the Progress
 
 Displaying the execution progress in apps from notebook functions.
 ```
#Output Progress Message: To share the progress of the Notebook run as a percentage with the analytical app
percentage_progress = "50"
restworkflowcontext.outputProgress(id=9, title="Progress", progress=percentage_progress)

 ```
In above function can be used in notebbok to send the progess status back to apps.

2.3> Display the HTML content: Output as HTML

To display HTML content in Apps, use the following code.

```
htmlstr1 = "<h3>You can view HTML code in notebooks.</h3>"
restworkflowcontext.outHTML(9, title="Example HTML", text = htmlstr1)
```

2.4> Display the dataframe as table.

To display the dataframe as table in apps.

```
restworkflowcontext.outPandasDataframe(9, "Names", df)

#To display 3 rows
restworkflowcontext.outDataFrame(9, "Names", df, 3)
```

2.5> Text, Success and Failure Messgaes

To display text messsage
```
restworkflowcontext.outStr(9, "Test String", text="text")
```

To display success message
```
message = "Job Execution Completed."
restworkflowcontext.outSuccess(9, title="Success", text=message)
```

To display failure message

```
message = "Sending the failure message."
restworkflowcontext.outFailure(id=9, title="Failure", text=message)
```

#### 3. Summary of the notebook
load the data from the `churn_data.csv` file.
Profiling function returns the statistics summary of the data.
Data Preprocessing returns size and columns in the dataset and checks for missing values.
Data Visualization: Plots a histogram to see total_day_calls distribution. It also shows the correlation between the features using a heatmap.
If the option is selected as Modelling, model_training function is called. This function replaces True/False strings to integers and splits the data into training and testing sets (80%-20%). It then uses RandomForestClassifier to train the model and returns the model accuracy report. 

### 2. fire_notebook_functions.ipynb

#### 1. To get connection details.

```
#To get the connection details
connection_details = restworkflowcontext.getConnectionDetails(conn_name="mysql", default="host,port,database,username,password")
print(connection_details)

if connection_details is not None and connection_details != "host,port,database,username,password":
    # Access data from the parsed JSON
    print("Connection Name:", connection_details['connectionName'])
    print("URL:", connection_details['url'])
    print("Username:", connection_details['username'])
    print("Password:", connection_details['password'])
    print("DriverClass:", connection_details['driverClass'])
    mysqlurl = connection_details['url']
    restworkflowcontext.outStr(id=9, title="URL:", text=mysqlurl)
    message = "Successfully Retreved the Connection Details!"
    restworkflowcontext.outStr(id=9, title="Message", text=message)
```

First step is to create the connection in Sparkflows and use the name of the connection to get the details in notebook.


Also in App create the field `CONNECTION_NAME` with values and pass it to notebook as parameter.

```
connection_name_value = restworkflowcontext.getParmeters(parameter_name="CONNECTION_NAME", default="mysql")

connection_details = restworkflowcontext.getConnectionDetails(conn_name=connection_name_value, default="host,port,database,username,password")
```

connection_details gets the details of the connection as  json with all the fields like url, username, password, dbname etc.

#### 2. To get user details.

Below is the code snippet used in notebook to get the current user name of running apps with attached notebook.

```
#To get UserDetails of app execution

user_details = restworkflowcontext.getUserDetailsOfAppExecute()
print(user_details)
if user_details is not None:
   print("username:", user_details['username'])
   username = user_details['username']
   restworkflowcontext.outStr(id=9, title="Current User Name: ", text=username)

```

#### 3. fire_html_plotly_notebook_functions.ipynb

Example notebook functions to send the html, plotly, text, success and progress messages back to apps.

#### 4. fire_failure_notebook_functions.ipynb

Example notebook to show the progress and failure messages back to app.

When failure message sent to app, the current app execution status will be updated to `FAILURE`

