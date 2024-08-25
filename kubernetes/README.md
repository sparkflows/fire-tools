# Sparkflows Deployment on Kubernetes

Below are the steps to deploy Sparkflows on Kubernetes.

## Docker image

Use the docker image sparkflows/fire:py_3.2.1_3.2.81-rc1

### Ports

Expose the port 8080 for http and 8443 for https.

### Step 1 : Create a Persistent Volume

Use the following script for creating the Persistent Volume

https://github.com/sparkflows/fire-tools/blob/main/kubernetes/fire-pv.yaml

### Step 2: Create Sparkflows Service/Deployment

Create deployment/service using kubectl. Update image url of deployment.yaml file as per the latest version available. The below yaml file creates a service and deployment for Sparkflows with resource limit of 16GB ram and 4vCPU. You can configure the resources limit, as per your requirement.

https://github.com/sparkflows/fire-tools/blob/main/kubernetes/deployment.yaml

### Step 3 : Check Deployment

Step 3 : Check Deployment

On successful deployment, check the status of the pods and services using the following commands:

kubectl get po -A | grep sparkflows-app

## Step 4 : Access Sparkflows

Use the external IP of the service to access Sparkflows. The external IP can be found using the following command:

kubectl get svc sparkflows-app

You can now use the <external-IP>:targetPort to access Sparkflows in the browser.


### Ingress

Use the ingress url of the service pointing to the port 8080/8443 to access the service.

### Deployment Steps

NOTE: This is not recommended for production deployments.

1. Use the configuration defined in the `fire-pv.yaml` file to setup the persistent volume. We'll be using this volume to mount on the sparkflows pod.

2. Once you have the persistent volumes deployed, you can use the `deployment.yaml` and `service.yaml` configuration to deploy Sparkflows with the above volume mounted.

```bash
 $ kubectl apply -f deployment.yaml
 $ kubectl apply -f service.yaml
```

3. Verify if the pod is running. This might take 2-3 minutes depending on the network speed. The sparkflows image size is ~ 7GB.

```bash
$ kubectl get po -A | grep sparkflows-app

default    sparkflows-app-6499d496cb-qvk2q      1/1     Running     0     14m

```

4. The above service configuration will deploy using LoadBalancer. You can also use NodePort for quick testing using the below command.

```bash
kubectl create service nodeport sparkflows-svc --tcp=5050:8080
```

Here 8080 is the target port, while 5050 is the exposed port.

You can open the browser and navigate to the http://<dsn.loadbalancer.sparkflows>:<exposed-port>/ to view the login page
