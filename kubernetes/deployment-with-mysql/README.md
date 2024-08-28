# Sparkflows Deployment on Kubernetes with MySQL

Below are the steps to deploy Sparkflows on Kubernetes. In this deployment, we will be using MySQL as the database for Fire Insights server.

## Docker image

The Docker images for Sparkflows are listed here : https://hub.docker.com/r/sparkflows/fire/tags

The latest docker image available is : sparkflows/fire:py_3.2.1_3.2.81-rc42

## Step 1: Launch MySQL Client
Assuming MySQL is running in the namespace demo, create an interactive shell using the below command:

The command below launches a MySQL client pod in the Kubernetes cluster, connecting to a MySQL server running at mysql.demo.svc.cluster.local.
```
kubectl run -it --rm --image=mysql:8.0 --restart=Never mysql-client -- mysql -h mysql.demo.svc.cluster.local -p<root_password>
```
## Step 2: Setup MySQL for Sparkflows

The MySQL commands create a new database `firedb`, a new user `fire`, and grant the new user all privileges on the `firedb` database.

```
create database firedb;
CREATE user 'fire'@'%' IDENTIFIED BY 'fire';
GRANT ALL PRIVILEGES ON firedb.* TO 'fire'@'%' WITH GRANT OPTION;
```
## Step 3: Create Sparkflows Deployment/Service

Create deployment/service using kubectl. Update image url of fire-deployment.yaml file as per the latest version available. The list of latest versions can be found at:

https://docs.sparkflows.io/en/latest/release-notes/binaries.html

```
kubectl apply -f fire-deployment.yaml
```

## Step 4: Check Deployment

On successful deployment, check the status of the pods and services.

Fetch the node where the service was deployed:

```
kubectl get pods -n demo --selector="app=fire" --output=wide

NAME                    READY   STATUS    RESTARTS   AGE   IP           NODE     NOMINATED NODE   READINESS GATES
fire-5dc7cc9d88-q5szw   1/1     Running   0          44m   10.42.0.55   n1.k8s   <none>           <none>
```

## Step 5: Access Sparkflows

Get the port of the node, where the service is exposed:

```
kubectl get svc -n demo

NAME                                      TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
fire                                      NodePort       10.43.87.85     <none>        8080:30318/TCP               45m
```

Get the public IP of the node n1.k8s and access the Fire insights web console at ``http://<public-ip-node>:30318``

**You can setup a custom Load Balancer to access the above service.**



