# Application Setup Guide using Helm

## Overview

This document provides step-by-step instructions to deploy the `fire` application and connect it to a MySQL instance in a kubernetes cluster.

The process involves:

1. Deploying MySQL in the default namespace.
2. Setting up secrets for database access.
3. Deploying the `fire` application in the `sparkflows` namespace using Helm as the secrets are made to be available only in the `sparkflows` namespace.

---

## Prerequisites

Before starting the setup, ensure you have:

- A running Kubernetes cluster.
- `kubectl` and `helm` installed.
- The necessary Helm chart for `fire` and `MySQL` which can be found here: https://github.com/sparkflows/fire-tools/tree/main/kubernetes/deployment-with-mysql/chart.
- A `secrets.yaml` file with the database credentials, which can be found here: https://github.com/sparkflows/fire-tools/blob/main/kubernetes/deployment-with-mysql/config/secrets.yaml

---

## Step-by-Step Setup Instructions

### 1. Create the `sparkflows` Namespace

First, ensure the `sparkflows` namespace exists. If it does not exist, create it:
```
kubectl create namespace sparkflows
```

### 2. Deploy MySQL in the Default Namespace

Deploy MySQL in the `default` namespace using the provided Helm chart.
```
helm install mysql ./chart/mysql --namespace default
```

Verify that the MySQL deployment is up and running:
```
kubectl get pods --namespace default
```

### 3. Apply the Database Secrets in `sparkflows` Namespace

Ensure that the `secrets.yaml` contains the appropriate MySQL connection details, such as the MySQL host (in the `default` namespace), username, password, and port.

1. Base64 encode the ClusterIP of the MySQL pod and put it as the `DB_HOST` in the `secrets.yaml`.
```
echo -n 'ClusterIP' | base64
```

2. Next, apply the `secrets.yaml` file, which contains the credentials and connection details for the MySQL database. This step is crucial before installing the `fire` application because the `fire` application depends on the secrets to connect to the MySQL database.
```
kubectl apply -f ./config/secrets.yaml --namespace sparkflows
```

### 4. Deploy the `fire-test` Application in `sparkflows` Namespace

Now, deploy the `fire-test` application using Helm:
```
helm install fire ./chart/fire --namespace sparkflows
```

Ensure the application is up and running by checking the status of the pods:
```
kubectl get pods --namespace sparkflows
```

### 5. Verify the Application Connectivity to MySQL

After the `fire` application starts, verify it can connect to MySQL by inspecting the pod logs and ensuring there are no connectivity issues:
```
kubectl logs <fire-test-pod-name> --namespace sparkflows
```

---
## Troubleshooting

### Readiness or Liveness Probe Fails

If the readiness or liveness probe fails, you may need to adjust the timeouts in the Helm chart values. Increase the `initialDelaySeconds` and `timeoutSeconds` in the `livenessProbe` and `readinessProbe` configurations in the `values.yaml`.

### Connectivity Issues with MySQL

If the `fire` application cannot connect to MySQL, check the following:
- Check the `DB_HOST` in the `secrets.yaml`.
- Verify that MySQL is running and accessible on port `3306`.
