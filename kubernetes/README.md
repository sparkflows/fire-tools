# Sparkflows Deployment on Kubernetes

Below are the steps to deploy Sparkflows on Kubernetes.

## Docker image

Use the docker image sparkflows/fire:py_3.2.1_3.2.81-rc1

### Ports

Expose the port 8080 for http and 8443 for https.

## Step 1 : Create a Persistent Volume

Use the configuration defined in the `pv.yaml` file to setup the persistent volume. We'll be using this volume to mount on the sparkflows pod. The size we have set it up is 10GB. This storage will be mounted on the Sparkflows container, at the path where the H2 database is being stored. In the below, the host path is set to /data/fire

* https://github.com/sparkflows/fire-tools/blob/main/kubernetes/pv.yaml

Use the below command ro create the persistent volumeand claim:

```bash
kubectl apply -f pv.yaml
```

## Step 2: Create Sparkflows Service/Deployment

Create deployment/service using kubectl. Update image url of deployment.yaml file as per the latest version available. The below yaml file creates a service and deployment for Sparkflows with resources of 8GB memory and 2vCPUs with a limit of 16GB memory and 4vCPU. You can configure the resources limit, as per your requirement.

* https://github.com/sparkflows/fire-tools/blob/main/kubernetes/deployment.yaml
* https://github.com/sparkflows/fire-tools/blob/main/kubernetes/service.yaml

```bash
 kubectl apply -f deployment.yaml
 kubectl apply -f service.yaml
```

## Step 3 : Check Deployment

On successful deployment, check the status of the pods and services using the following commands:

```bash
kubectl get po -A | grep sparkflows-app

default    sparkflows-app-6499d496cb-qvk2q      1/1     Running     0     14m

```

## Step 4 : Access Sparkflows

The above service configuration will deploy using LoadBalancer. Use the external IP of the service to access Sparkflows. The external IP can be found using the following command:

```bash
kubectl get svc sparkflows-app
```

You can now navigate to ``http://<external-IP>:targetPort`` to access Sparkflows in the browser, the targetPort being 8080.

#### Quick Testing using NodePort:
You can also use NodePort for quick testing using the below command.

```bash
kubectl create service nodeport sparkflows-svc --tcp=5050:8080
```
Here 8080 is the target port, while 5050 is the exposed port.
NodePort service command maps port 5050 on the Node to port 8080 inside the pod where the application is running and you can access the application by navigating to ``http://<node-IP>:5050`` in your browser.


#### Pre-Configured Accounts
Two user accounts come preconfigured with Sparkflows, also make sure to update app.postMessageURL as per Sparkflows absolute URL running and should be accessible.

* admin/admin
* test/test

You may change these usernames and passwords in Sparkflows.


## Step 5 : Update/Upgrade Sparkflows

In order to update any configuration in the deployment.yaml, like image version or container resources limits/requests you need to first delete the current deployment using the below command.

```bash
kubectl delete -f deployment.yaml
```

Once you’ve deleted the deployment, re-create the service. We need to do this, because two instances can’t use the same H2 database as it’s a file based DB.

```bash
kubectl apply -f deployment.yaml
```



