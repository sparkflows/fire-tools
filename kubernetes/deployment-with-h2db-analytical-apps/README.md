# Analytical Apps on AWS EKS

## Overview

Follow the steps below to run analytical apps using Jupyter Notebooks in an AWS EKS cluster.

We need to grant permissions to the sparkflows in AWS EKS cluster which is done using the following manifests:

## Step 1: Create the service account

This creates a user account with a name say `sparkflows-admin`, and adds the role which was used to create the EKS in the annotation which is used by the deployment pods. When any pod runs using the `sparkflows-admin` service account, then it will be have all set of permissions to different AWS resources as, the role mentioned as the value of the annotation `eks.amazonaws.com/role-arn`. 

Use the below command to create the service account.
```
kubectl apply -f serviceaccount.yaml
```


**Ensure to replace the role-arn with the role-arn used to create the AWS EKS Cluster.**

## Step 2: Create a Role for the service account

This creates a job role, that defines and grants the set of permissions required for Sparkflows through the service account - `sparkflows-admin`, to execute, watch, delete Jobs triggered through the Jupyter Notebook based analytical applications.

Use the below command to create the role

```
kubectl apply -f job-role.yaml
```

## Step 3: Bind the role to Service account

This binds the `job-creator` ClusterRole, using the job-binding resource with it's subject as `sparkflows-admin`.

```
kubectl apply -f job-binding.yaml
```


